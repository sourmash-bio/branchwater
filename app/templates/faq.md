{% include 'header.html' %}

<link
  href="https://cdn.jsdelivr.net/npm/tabulator-tables@4.9.3/dist/css/tabulator.min.css"
  rel="stylesheet"
/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.0/papaparse.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/tabulator-tables@4.9.3/dist/js/tabulator.min.js"></script>

<div class="container mt-3">

      {% filter markdownify %}
# Frequently Asked Questions - branchwater

**Please check out [the About page!](/about)!**

And, if you have a question that's not answered below, ask it [in the issue tracker!](https://github.com/sourmash-bio/branchwater/issues/new?template=branchwater-web.md)

## When I upload my sample, what is being uploaded?!

A k-mer summary (or sketch) of your sample is calculated
locally, and then uploaded to the branchwater Web site.
This summary is typically only a few megabytes in size, even for
large genomes.

To calculate the sketch locally, branchwater uses in-browser k-mer
sketching, provided by
[the branchwater project](https://github.com/sourmash-bio/branchwater/tree/main/app/static).

This means that branchwater doesn't "see" your reads, or the
complete data set; it only has access to the sketch.<p> For more information on
sketching, as well as an over-abundance of technical details, please
see [the sourmash documentation](https://sourmash.readthedocs.io/).

There is a 5 MB file size limit for branchwater queries.

## Where can I get information on what is in the branchwater database?

The branchwater API server provides a `stats` endpoint that returns summary information (in JSON) about the current database content; you can access it at https://branchwater-api.jgi.doe.gov/metadata/stats.

The following Python code will retrieve the JSON code using the `requests` library:
```python!
import requests
url = "https://branchwater-api.jgi.doe.gov/metadata/stats"
response = requests.get(url)
print(response.json())
```

As of June 2025, branchwater indexes 1,161,119 SRA metagenome data sets at a k-mer size of 21 with a scaled factor of 1000. Please see the [the sourmash FAQ](https://sourmash.readthedocs.io/en/latest/faq.html) for more details on what the k-mer size and scaled factors mean!

The full list of accessions indexed by branchwater can be retrieved using the `accessions` endpoint at 
https://branchwater-api.jgi.doe.gov/metadata/accessions.

## How can I search for multiple samples at the same time?

You can only search for a single sample via the Web interface; if you upload multiple files, only the first one is used in the search and only those results are shown.

You can search multiple samples via the command line or using an HTTP request, however, if you're feeling adventrous!

### Using HTTP

The following Python code uses the [requests library](https://pypi.org/project/requests/) to search branchwater with a k=21 gzip-compressed sourmash sketch, and retrieves the response.

```python!
import requests
url = "https://branchwater-api.jgi.doe.gov/search"
sketch_data = open('sketch.sig.gz', 'rb').read()

response = requests.post(url, data=sketch_data)
print(response.content.decode('utf-8'))
```

To create `sketch.sig.gz`, use `sourmash sig cat <source sketch> -o sketch.sig.gz`. Only the first sketch in each signature file will be used, so you will need to submit each sketch on a separate request.

### Using the branchwater command line client

Follow the steps below to get started with the branchwater client on the command line. Note, you'll need to have the [Rust programming language](https://www.rust-lang.org/) installed.

1. Clone the `branchwater` repo from GitHub at https://github.com/sourmash-bio/branchwater.
2. cd into the `crates/client` subdirectory.
3. Build the client with `cargo build`.
4. Run the client with `cargo run`. You can see the options by running `cargo run -- --help`.

For example, the following command:
```
cargo run query.fa -o out.csv
```
will sketch the contents of `query.fa` into a single signature, query branchwater, and save the results to `out.csv`.

## How do I cite branchwater?

@CTB fix

For now, please cite [the sourmash paper in the Journal of Open Source Software](https://joss.theoj.org/papers/10.21105/joss.06830#):

>Irber et al., (2024). sourmash v4: A multitool to quickly search, compare, and analyze genomic and metagenomic data sets. Journal of Open Source Software, 9(98), 6830, https://doi.org/10.21105/joss.06830

  {% endfilter %}
  </div>

    {% include 'footer.html' %}
  </div>
</div>
