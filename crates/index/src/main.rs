use camino::Utf8Path as Path;
use camino::Utf8PathBuf as PathBuf;
use clap::{Parser, Subcommand};
use tracing::info;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

use sourmash::collection::Collection;
use sourmash::index::revindex::{prepare_query, RevIndex, RevIndexOps};
use sourmash::manifest::Manifest;
use sourmash::prelude::*;
use sourmash::signature::{Signature, SigsTrait};
use sourmash::storage::{FSStorage, InnerStorage, ZipStorage};

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Cli {
    #[clap(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    Index {
        /// Location of the input data.
        /// Either a zip file or a path to a directory containing signatures.
        location: PathBuf,

        /// Manifest for sigs to be loaded from storage
        #[clap(short, long)]
        manifest: Option<PathBuf>,

        /// ksize
        #[clap(short, long, default_value = "31")]
        ksize: u8,

        /// scaled
        #[clap(short, long, default_value = "1000")]
        scaled: usize,

        /// The path for output
        #[clap(short, long)]
        output: PathBuf,

        /// Index using colors
        #[clap(long = "colors")]
        colors: bool,
    },
    Update {
        /// Location of the input data.
        /// Either a zip file or a path to a directory containing signatures.
        location: PathBuf,

        /// Manifest for sigs to be loaded from storage
        #[clap(short, long)]
        manifest: Option<PathBuf>,

        /// ksize
        #[clap(short, long, default_value = "31")]
        ksize: u8,

        /// scaled
        #[clap(short, long, default_value = "1000")]
        scaled: usize,

        /// The path for output
        #[clap(short, long)]
        output: PathBuf,
    },
    /* TODO: need the repair_cf variant, not available in rocksdb-rust yet
        Repair {
            /// The path for DB to repair
            #[clap(parse(from_os_str))]
            index: PathBuf,

            /// Repair using colors
            #[clap(long = "colors")]
            colors: bool,
        },
    */
    Manifest {
        /// File with list of paths to signatures
        pathlist: PathBuf,

        /// ksize
        #[clap(short, long)]
        ksize: Option<u8>,

        /// Path for future FSStorage.
        ///
        /// Will be removed from a record internal location in manifest.
        #[clap(short, long)]
        basepath: Option<PathBuf>,

        /// The path for output
        #[clap(short, long)]
        output: Option<PathBuf>,
    },
    Metadata {
        /// Save metadata manifest to this file
        #[clap(short, long)]
        output: Option<PathBuf>,

        /// Return only accessions
        #[clap(long = "acc-only")]
        acc_only: bool,

        /// Index to extract metadata from
        index: PathBuf,
    },
    Check {
        /// The path for output
        output: PathBuf,

        /// avoid deserializing data, and without stats
        #[clap(long = "quick")]
        quick: bool,
    },
    Convert {
        /// The path for the input DB
        input: PathBuf,

        /// The path for the output DB
        output: PathBuf,
    },
    Search {
        /// Query signature
        query_path: PathBuf,

        /// Path to rocksdb index dir
        index: PathBuf,

        /// ksize
        #[clap(short = 'k', long = "ksize", default_value = "31")]
        ksize: u8,

        /// scaled
        #[clap(short = 's', long = "scaled", default_value = "1000")]
        scaled: usize,

        /// threshold_bp
        #[clap(short = 't', long = "threshold_bp", default_value = "50000")]
        threshold_bp: usize,

        /// minimum containment to report
        #[clap(short = 'c', long = "containment", default_value = "0.2")]
        containment: f64,

        /// The path for output
        #[clap(short = 'o', long = "output")]
        output: Option<PathBuf>,
    },
    Gather {
        /// Query signature
        query_path: PathBuf,

        /// Path to rocksdb index dir
        index: PathBuf,

        /// ksize
        #[clap(short = 'k', long = "ksize", default_value = "31")]
        ksize: u8,

        /// scaled
        #[clap(short = 's', long = "scaled", default_value = "1000")]
        scaled: usize,

        /// threshold_bp
        #[clap(short = 't', long = "threshold_bp", default_value = "50000")]
        threshold_bp: usize,

        /// The path for output
        #[clap(short = 'o', long = "output")]
        output: Option<PathBuf>,
    },
}

fn gather<P: AsRef<Path>>(
    queries_file: P,
    index: P,
    selection: Selection,
    threshold_bp: usize,
    _output: Option<P>,
) -> Result<(), Box<dyn std::error::Error>> {
    let query_sig = Signature::from_path(queries_file.as_ref())?
        .swap_remove(0)
        .select(&selection)?;

    let query = prepare_query(query_sig, &selection).expect("Couldn't find a compatible MinHash");

    let threshold = threshold_bp / query.scaled() as usize;

    let db = RevIndex::open(index.as_ref(), true, None)?;
    info!("Loaded DB");

    info!("Building counter");
    let (counter, query_colors, hash_to_color) = db.prepare_gather_counters(&query);
    // TODO: truncate on threshold?
    info!("Counter built");

    let matches = db.gather(
        counter,
        query_colors,
        hash_to_color,
        threshold,
        &query,
        Some(selection),
    )?;

    info!("matches: {}", matches.len());
    for match_ in matches {
        println!(
            "{} {} {}",
            match_.name(),
            match_.intersect_bp(),
            match_.f_match()
        )
    }

    Ok(())
}

fn search<P: AsRef<Path>>(
    queries_file: P,
    index: P,
    selection: Selection,
    threshold_bp: usize,
    minimum_containment: f64,
    _output: Option<P>,
) -> Result<(), Box<dyn std::error::Error>> {
    let query_sig = Signature::from_path(queries_file.as_ref())?
        .swap_remove(0)
        .select(&selection)?;

    let mut query = None;
    if let Some(q) = prepare_query(query_sig, &selection) {
        query = Some(q);
    }
    let query = query.expect("Couldn't find a compatible MinHash");
    let query_size = query.size() as f64;

    let threshold = threshold_bp / query.scaled() as usize;

    let db = RevIndex::open(index.as_ref(), true, None)?;
    info!("Loaded DB");

    info!("Building counter");
    let counter = db.counter_for_query(&query);
    info!("Counter built");

    let matches = db.matches_from_counter(counter, threshold);

    //info!("matches: {}", matches.len());
    println!("SRA ID,containment");
    matches
        .into_iter()
        .filter_map(|(path, size)| {
            let containment = size as f64 / query_size;
            if containment >= minimum_containment {
                println!(
                    "{},{}",
                    path.split("/").last().unwrap().split(".").next().unwrap(),
                    containment
                );
                Some(())
            } else {
                None
            }
        })
        .count();

    Ok(())
}

fn index<P: AsRef<Path>>(
    location: P,
    manifest: Option<P>,
    selection: Selection,
    output: P,
    colors: bool,
) -> Result<(), Box<dyn std::error::Error>> {
    let manifest = if let Some(m) = manifest {
        let rdr = std::fs::OpenOptions::new().read(true).open(m.as_ref())?;
        Some(Manifest::from_reader(rdr)?)
    } else {
        None
    };

    let collection = if matches!(location.as_ref().extension(), Some("zip")) {
        if let Some(m) = manifest {
            let storage = ZipStorage::from_file(location)?;
            Collection::new(m, InnerStorage::new(storage))
        } else {
            Collection::from_zipfile(location)?
        }
    } else {
        let manifest = manifest.ok_or_else(|| "Need a manifest")?;
        assert!(location.as_ref().exists());
        assert!(location.as_ref().is_dir());
        let storage = FSStorage::builder()
            .fullpath(location.as_ref().into())
            .subdir("".into())
            .build();
        Collection::new(manifest, InnerStorage::new(storage))
    };

    RevIndex::create(
        output.as_ref(),
        collection.select(&selection)?.try_into()?,
        colors,
    )?;

    Ok(())
}

fn metadata<P: AsRef<Path>>(
    index: P,
    output: Option<P>,
    acc_only: bool,
) -> Result<(), Box<dyn std::error::Error>> {
    use std::fs::File;
    use std::io::{BufWriter, Write};

    let db = RevIndex::open(index.as_ref(), false, None)?;

    let manifest = db.collection().manifest();

    let mut out: Box<dyn Write + Send> = match output {
        Some(path) => Box::new(BufWriter::new(File::create(path.as_ref()).unwrap())),
        None => Box::new(std::io::stdout()),
    };

    if acc_only {
        let accs: Vec<String> = manifest.iter().map(|r| r.name().into()).collect();
        let accs = accs.join("\n");
        writeln!(out, "{}", accs)?;
    } else {
        manifest.to_writer(out)?;
    }

    Ok(())
}

fn update<P: AsRef<Path>>(
    location: P,
    manifest: Option<P>,
    selection: Selection,
    output: P,
) -> Result<(), Box<dyn std::error::Error>> {
    let manifest = if let Some(m) = manifest {
        let rdr = std::fs::OpenOptions::new().read(true).open(m.as_ref())?;
        Some(Manifest::from_reader(rdr)?)
    } else {
        None
    };

    let collection = if matches!(location.as_ref().extension(), Some("zip")) {
        if let Some(m) = manifest {
            let storage = ZipStorage::from_file(location)?;
            Collection::new(m, InnerStorage::new(storage))
        } else {
            Collection::from_zipfile(location)?
        }
    } else {
        let manifest = manifest.ok_or_else(|| "Need a manifest")?;
        assert!(location.as_ref().exists());
        assert!(location.as_ref().is_dir());
        let storage = FSStorage::builder()
            .fullpath(location.as_ref().into())
            .subdir("".into())
            .build();
        Collection::new(manifest, InnerStorage::new(storage))
    };

    let db = RevIndex::open(output.as_ref(), false, None)?;
    db.update(collection.select(&selection)?.try_into()?)?;

    Ok(())
}

fn convert<P: AsRef<Path>>(_input: P, _output: P) -> Result<(), Box<dyn std::error::Error>> {
    todo!()
    /*
    info!("Opening input DB");
    let db = RevIndex::open(input.as_ref(), true);

    info!("Creating output DB");
    let output_db = RevIndex::create(output.as_ref(), true);

    info!("Converting input DB");
    db.convert(output_db)?;

    info!("Finished conversion");
    Ok(())
    */
}

fn manifest<P: AsRef<Path>>(
    pathlist: P,
    output: Option<P>,
    selection: Option<Selection>,
    basepath: Option<P>,
) -> Result<(), Box<dyn std::error::Error>> {
    use std::fs::File;
    use std::io::{BufRead, BufReader, BufWriter, Write};

    let paths: Vec<PathBuf> = BufReader::new(File::open(pathlist.as_ref())?)
        .lines()
        .map(|line| {
            let mut path = PathBuf::new();
            path.push(line.unwrap());
            path
        })
        .collect();

    let manifest: Manifest = paths.as_slice().into();

    let manifest = if let Some(selection) = selection {
        manifest.select(&selection)?
    } else {
        manifest
    };

    let manifest = if let Some(basepath) = basepath {
        let path: &str = basepath.as_ref().as_str();
        manifest
            .iter()
            .map(|r| {
                let mut record = r.clone();
                record.set_internal_location(
                    r.internal_location()
                        .strip_prefix(path)
                        .expect("Error stripping")
                        .into(),
                );
                record
            })
            .collect::<Vec<_>>()
            .into()
    } else {
        manifest
    };

    let out: Box<dyn Write + Send> = match output {
        Some(path) => Box::new(BufWriter::new(File::create(path.as_ref()).unwrap())),
        None => Box::new(std::io::stdout()),
    };

    manifest.to_writer(out)?;

    Ok(())
}

fn check<P: AsRef<Path>>(output: P, quick: bool) -> Result<(), Box<dyn std::error::Error>> {
    use numsep::{separate, Locale};
    use size::Size;

    info!("Opening DB");
    let db = RevIndex::open(output.as_ref(), true, None)?;

    info!("Starting check");
    let stats = db.check(quick);

    let kcount = *stats.kcount();
    let vcount = *stats.vcount();
    let vcounts = stats.vcounts();

    //info!("*** {} ***", cf_name);
    let ksize = Size::from_bytes(kcount);
    let vsize = Size::from_bytes(vcount);
    if !quick {
        info!(
            "total datasets: {}",
            separate(stats.total_datasets(), Locale::English)
        );
    }
    info!(
        "total keys: {}",
        separate(stats.kcount() / 8, Locale::English)
    );

    info!("k: {}", ksize.to_string());
    info!("v: {}", vsize.to_string());

    if !quick && kcount > 0 {
        info!(
            "max v: {}",
            vcounts.percentile(100.0).unwrap().into_iter().count()
        );
        //        info!("mean v: {}", vcounts.mean().unwrap());
        //        info!("stddev: {}", vcounts.stddev().unwrap());
        info!(
            "median v: {}",
            vcounts.percentile(50.0).unwrap().into_iter().count()
        );
        info!(
            "p25 v: {}",
            vcounts.percentile(25.0).unwrap().into_iter().count()
        );
        info!(
            "p75 v: {}",
            vcounts.percentile(75.0).unwrap().into_iter().count()
        );
    }

    info!("Finished check");
    Ok(())
}

/* TODO: need the repair_cf variant, not available in rocksdb-rust yet
fn repair<P: AsRef<Path>>(output: P, colors: bool) {
    info!("Starting repair");
    RevIndex::repair(output.as_ref(), colors);
    info!("Finished repair");
}
*/

fn main() -> Result<(), Box<dyn std::error::Error>> {
    use Commands::*;

    tracing_subscriber::registry()
        .with(tracing_subscriber::EnvFilter::new(
            std::env::var("RUST_LOG")
                .unwrap_or_else(|_| "branchwater=debug".into()),
        ))
        .with(tracing_subscriber::fmt::layer().json())
        .init();

    let opts = Cli::parse();

    match opts.command {
        Index {
            output,
            location,
            manifest,
            ksize,
            scaled,
            colors,
        } => {
            let selection = Selection::builder()
                .ksize(ksize.into())
                .scaled(scaled as u32)
                .build();

            index(location, manifest, selection, output, colors)?
        }
        Update {
            output,
            location,
            manifest,
            ksize,
            scaled,
        } => {
            let selection = Selection::builder()
                .ksize(ksize.into())
                .scaled(scaled as u32)
                .build();

            update(location, manifest, selection, output)?
        }
        Check { output, quick } => check(output, quick)?,
        Convert { input, output } => convert(input, output)?,
        Manifest {
            pathlist,
            output,
            ksize,
            basepath,
        } => {
            let selection = ksize.map(|ksize| Selection::builder().ksize(ksize.into()).build());

            manifest(pathlist, output, selection, basepath)?
        }
        Metadata {
            index,
            acc_only,
            output,
        } => metadata(index, output, acc_only)?,
        Search {
            query_path,
            output,
            index,
            threshold_bp,
            ksize,
            scaled,
            containment,
        } => {
            let selection = Selection::builder()
                .ksize(ksize.into())
                .scaled(scaled as u32)
                .build();

            search(
                query_path,
                index,
                selection,
                threshold_bp,
                containment,
                output,
            )?
        }
        Gather {
            query_path,
            output,
            index,
            threshold_bp,
            ksize,
            scaled,
        } => {
            let selection = Selection::builder()
                .ksize(ksize.into())
                .scaled(scaled as u32)
                .build();

            gather(query_path, index, selection, threshold_bp, output)?
        } /* TODO: need the repair_cf variant, not available in rocksdb-rust yet
                  Repair { index, colors } => repair(index, colors),
          */
    };

    Ok(())
}
