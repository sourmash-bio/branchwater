use std::collections::HashMap;
use std::path::{Path, PathBuf};

use clap::Parser;
use color_eyre::{eyre::Result, eyre::WrapErr};
use needletail::{parse_fastx_file, parse_fastx_stdin, Sequence};
use reqwest_middleware::ClientBuilder;
use reqwest_retry::{policies::ExponentialBackoff, RetryTransientMiddleware};
use serde_json::json;
use tracing::info;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

use sourmash::encodings::HashFunctions;
use sourmash::prelude::*;
use sourmash::signature::Signature;
use sourmash::sketch::minhash::{max_hash_for_scaled, KmerMinHashBTree};
use sourmash::sketch::Sketch;

// Original comment from ripgrep and why using jemalloc with musl is recommended:
// https://github.com/BurntSushi/ripgrep/commit/03bf37ff4a29361c47843369f7d3dc5689b8fdac

// Since Rust no longer uses jemalloc by default, ripgrep will, by default,
// use the system allocator. On Linux, this would normally be glibc's
// allocator, which is pretty good. In particular, ripgrep does not have a
// particularly allocation heavy workload, so there really isn't much
// difference (for ripgrep's purposes) between glibc's allocator and
// jemalloc.
//
// However, when ripgrep is built with musl, this means ripgrep will use musl's
// allocator, which appears to be substantially worse. (musl's goal is not to
// have the fastest version of everything. Its goal is to be small and
// amenable to static compilation.) Even though ripgrep isn't particularly allocation
// heavy, musl's allocator appears to slow down ripgrep quite a bit.  Therefore,
// when building with musl, we use jemalloc.
//
// We don't unconditionally use jemalloc because it can be nice to use the
// system's default allocator by default. Moreover, jemalloc seems to increase
// compilation times by a bit.
#[cfg(target_env = "musl")]
#[global_allocator]
static ALLOC: jemallocator::Jemalloc = jemallocator::Jemalloc;

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Cli {
    /// Input file. Can be:
    ///   - sequences (FASTA/Q, compressed or not)
    ///   - an existing signature (use with --sig)
    ///   - a single dash ("-") for reading from stdin
    #[clap(value_parser, verbatim_doc_comment)]
    sequences: PathBuf,

    /// Save results to this file. Default: stdout
    #[clap(value_parser, short, long)]
    output: Option<PathBuf>,

    /// Server to query. Default: https://api.branchwater.sourmash.bio
    #[clap(short, long, default_value = "https://api.branchwater.sourmash.bio")]
    server: String,

    /// Metadata server to query. Default: https://branchwater.sourmash.bio
    #[clap(short, long, default_value = "https://branchwater.jgi.doe.gov")]
    metadata_server: String,

    /// Input file is already a signature
    #[clap(long = "sig")]
    is_sig: bool,

    /// Return full results (containment plus matching dataset ID metadata)
    #[clap(long = "full")]
    full: bool,

    /// How many times to retry requests to the server (default: 3)
    #[clap(long = "retry", default_value = "3")]
    retry: u32,
}

#[tokio::main]
async fn main() -> Result<()> {
    tracing_subscriber::registry()
        .with(tracing_subscriber::EnvFilter::new(
            std::env::var("RUST_LOG").unwrap_or_else(|_| "branchwater=debug".into()),
        ))
        .with(tracing_subscriber::fmt::layer().json())
        .init();

    color_eyre::install()?;

    let Cli {
        sequences,
        output,
        is_sig,
        server,
        metadata_server,
        full,
        retry,
    } = Cli::parse();

    info!("Preparing signature");
    let (sig, query_name): (Signature, String) = if !is_sig {
        let max_hash = max_hash_for_scaled(1000);
        let mh = KmerMinHashBTree::builder()
            .num(0)
            .max_hash(max_hash)
            .ksize(21)
            .build();
        let mut sig = Signature::builder()
            .name(Some("branchwater query".into()))
            .signatures(vec![Sketch::LargeMinHash(mh)])
            .hash_function("DNA")
            .build();

        let (mut parser, mut query_name) = if sequences.as_path() == Path::new("-") {
            (parse_fastx_stdin()?, None)
        } else {
            (
                parse_fastx_file(&sequences)?,
                Some(sequences.to_string_lossy().to_string()),
            )
        };

        while let Some(record) = parser.next() {
            let record = record?;
            let seq = record.normalize(false);
            sig.add_sequence(&seq, true)?; // TODO: expose force?
            if query_name.is_none() {
                query_name = Some(String::from_utf8_lossy(record.id()).to_string());
            }
        }

        (sig, query_name.expect("Couldn't determine query name"))
    } else {
        let mut reader = std::io::BufReader::new(std::fs::File::open(&sequences)?);
        let mut sigs = Signature::load_signatures(
            &mut reader,
            Some(21),
            Some(HashFunctions::Murmur64Dna),
            Some(1000),
        )?;

        let mut sig = sigs.swap_remove(0);
        // remove abundance
        let count = sig
            .iter_mut()
            .map(|s| {
                if let Sketch::MinHash(mh) = s {
                    mh.disable_abundance()
                }
            })
            .count();
        debug_assert_eq!(count, 1);

        (sig, sequences.to_string_lossy().to_string())
    };

    let output: Box<dyn std::io::Write> = match output {
        Some(path) => Box::new(std::io::BufWriter::new(
            std::fs::File::create(path).unwrap(),
        )),
        None => Box::new(std::io::stdout()),
    };

    let retry_policy = ExponentialBackoff::builder().build_with_max_retries(retry);
    let client = ClientBuilder::new(
        reqwest::Client::builder()
            .timeout(std::time::Duration::from_secs(3600))
            .build()?,
    )
    .with(RetryTransientMiddleware::new_with_policy(retry_policy))
    .build();

    let res = if full {
        info!("Sending request to {}", metadata_server);

        let sig_data: HashMap<&str, String> = [("signatures", json!(sig).to_string())].into();
        client.post(metadata_server).json(&sig_data).send().await?
    } else {
        info!("Sending request to {}", server);
        let mut sig_data = vec![];
        {
            let mut output = niffler::get_writer(
                Box::new(&mut sig_data),
                niffler::compression::Format::Gzip,
                niffler::compression::Level::Nine,
            )
            .wrap_err_with(|| "Error preparing signature")?;

            sig.to_writer(&mut output)
                .wrap_err_with(|| "Error preparing signature")?;
        }

        client
            .post(format!("{}/search", server))
            .body(sig_data)
            .send()
            .await?
    };

    info!("Writing matches to output");
    if full {
        //let raw_results: serde_json::Value = serde_json::from_slice(&res.bytes()?)?;
        let raw_results: serde_json::Value = res.json().await?;
        let records = raw_results.as_array().unwrap();
        let headers = records[0].as_object().unwrap().keys();

        let mut wtr = csv::Writer::from_writer(output);
        wtr.write_record(headers)?;

        for record in records {
            let values = record.as_object().unwrap().values();
            wtr.write_record(values.map(|v| {
                if v.is_string() {
                    v.as_str().unwrap().into()
                } else {
                    v.to_string()
                }
            }))?;
        }
    } else {
        let data = res.bytes().await?;

        let mut wtr = csv::Writer::from_writer(output);
        let mut rdr = csv::Reader::from_reader(&data[..]);

        let mut headers = rdr.headers()?.clone();
        headers.push_field("query");

        wtr.write_record(&headers)?;

        for result in rdr.records() {
            let mut record = result?;
            record.push_field(query_name.as_str());
            wtr.write_record(&record)?;
        }
    }

    info!("Finished!");
    Ok(())
}

#[test]
fn verify_cli() {
    use clap::CommandFactory;
    Cli::command().debug_assert()
}
