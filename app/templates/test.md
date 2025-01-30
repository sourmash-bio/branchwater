{% include 'header.html' %}

<link
  href="https://cdn.jsdelivr.net/npm/tabulator-tables@4.9.3/dist/css/tabulator.min.css"
  rel="stylesheet"
/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.0/papaparse.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/tabulator-tables@4.9.3/dist/js/tabulator.min.js"></script>

<div class="container mt-3">

      {% filter markdownify %}
# Frequently Asked Questions - chill-filter

**Please check out [the User Guide!](/guide)!**

And, if you have a question that's not answered below, ask it [in the issue tracker!](https://github.com/dib-lab/chill-filter)

## When I upload my sample, what is being uploaded?!

A k-mer summary (or sketch) of your sample is calculated
locally, and then uploaded to the chill-filter Web site.
This summary is typically under a megabyte in size, even for
large shotgun data sets; you can download it from the chill-filter
site if you want to see the actual size.

To calculate the sketch locally, chill-filter uses in-browser k-mer
sketching, provided by
[the branchwater project](https://github.com/sourmash-bio/branchwater/tree/main/app/static).

This means that chill-filter doesn't "see" your reads, or the
complete data set; it only has access to the sketch. And you can
delete your sketch at any time.  <p> For more information on
sketching, as well as an over-abundance of technical details, please
see [the sourmash documentation](https://sourmash.readthedocs.io/).

## Should I subset my data to make things go faster?

We highly recommend analyzing your entire data set - no filtering,
subsetting, or removing reads. chill-filter's speed will not be
affected. But of course you're welcome to try out different
approaches - and we're happy to chat about it in
[the issue tracker!](https://github.com/dib-lab/chill-filter/issues)

## How can I do a combined analysis of several sequencing runs?

For now, you either have to combine all your files into one FASTA/FASTQ
file and sketch that, or use a command line tool to build a combined
sketch. Here's the command line you can use with sourmash:
```
sourmash sketch dna -p k=51,scaled=100000 [ list of files] --name SampleName -o combined.sig.zip
```
although there are other, faster programs you can use (e.g. [manysketch](https://github.com/sourmash-bio/sourmash_plugin_branchwater/tree/main/doc)).

You can then upload the resulting `combined.sig.zip` on the front page for a combined analysis!

## How can I analyze a dozen different samples?

If you want to use the Web site, you'll need to upload each sample separately.
Sorry!

There are ways to analyze hundreds to thousands of samples at the
command line. This requires installing the sourmash software and 
preparing some databases; ask us for details in
[the issue tracker!](https://github.com/dib-lab/chill-filter/issues)

We're working on a REST API so that you can use chill-filter from the
command line without installing the databases locally, too.

## How can I see which specific microbial or plant genomes are in my sample?

You can see matches to specific plant genomes, but not to specific
microbial genomes. You will be able to, eventually! But for now,
you'll have follow up on our sequence composition report yourself.

## What happens with overlaps between matches?

If sequence is shared between two matches, it will be assigned uniquely
to the first match in the list. This is known as "greedy assignment" and
is part of the sourmash gather algorithm.

## What if there's contamination in the database?

We're 100% reliant on the genomes in the reference database, so the
match that's displayed is to the contents of the genome record. If
the genome record is contaminated, then that will be part of the match
statistics.

That having been said, if the contamination is something that is shared
between multiple genomes in the reference collection, the match will
be assigned to the largest match - which often will be the source of
the contamination, not the contaminated genome. See the question above
about overlaps!

## I've downloaded a CSV results file; how do I interpret it??

chill-filter uses `sourmash gather` to calculate the results.

See
[the sourmash gather documentation](https://sourmash.readthedocs.io/en/latest/classifying-signatures.html#appendix-a-how-sourmash-gather-works)
for more information on the algorithm and the results file!

## Can you add a genome to your search database for me?

Please ask in [the issue tracker!](https://github.com/dib-lab/chill-filter/issues)

You can also deploy a copy of this site locally, with custom databases; see
[the chill-filter source code README](https://github.com/dib-lab/chill-filter)
for details.

## How do I cite chill-filter?

For now, please cite [the sourmash paper in the Journal of Open Source Software](https://joss.theoj.org/papers/10.21105/joss.06830#):

>Irber et al., (2024). sourmash v4: A multitool to quickly search, compare, and analyze genomic and metagenomic data sets. Journal of Open Source Software, 9(98), 6830, https://doi.org/10.21105/joss.06830

## How do you pay for this?

We're skipping our normal avocado toast brunch order in order to support this
site. We hope you appreciate our sacrifice!

## What kind of resources are needed to run a chill-filter server?

chill-filter.sourmash.bio is running on a Digital Ocean Basic Droplet,
with 4 GB of RAM, 2 CPUs, and 80 GB of SSD space.
      
  {% endfilter %}
  </div>

    {% include 'footer.html' %}
  </div>
</div>
