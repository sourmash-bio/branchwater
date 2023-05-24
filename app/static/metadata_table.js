const metadata_table = [
  {
    "HarmonizedName": "organism",
    "NCBI_provided_description": "Scientific name of the organism that was sequenced (as found in the NCBI Taxonomy Browser)",
    "percentage": "100"
  },
  {
    "HarmonizedName": "altitude",
    "NCBI_provided_description": "The altitude of the sample is the vertical distance between Earth's surface above Sea Level and the sampled position in the air.",
    "percentage": "5.439249936"
  },
  {
    "HarmonizedName": "depth",
    "NCBI_provided_description": "Depth is defined as the vertical distance below surface, e.g. for sediment or soil samples depth is measured from sediment or soil surface, respectivly. Depth can be reported as an interval for subsurface samples.",
    "percentage": "12.51890858"
  },
  {
    "HarmonizedName": "env_biome",
    "NCBI_provided_description": "not_provided",
    "percentage": "33.52413163"
  },
  {
    "HarmonizedName": "env_broad_scale",
    "NCBI_provided_description": "Add terms that identify the major environment type(s) where your sample was collected. Recommend subclasses of biome [ENVO:00000428]. Multiple terms can be separated by one or more pipes e.g.: \u00a0mangrove biome [ENVO:01000181]|estuarine biome [ENVO:01000020]",
    "percentage": "7.08836373"
  },
  {
    "HarmonizedName": "env_feature",
    "NCBI_provided_description": "not_provided",
    "percentage": "33.41724463"
  },
  {
    "HarmonizedName": "env_local_scale",
    "NCBI_provided_description": "Add terms that identify environmental entities having causal influences upon the entity at time of sampling, multiple terms can be separated by pipes, e.g.: \u00a0shoreline [ENVO:00000486]|intertidal zone [ENVO:00000316]",
    "percentage": "6.976624711"
  },
  {
    "HarmonizedName": "env_material",
    "NCBI_provided_description": "not_provided",
    "percentage": "30.97739532"
  },
  {
    "HarmonizedName": "env_medium",
    "NCBI_provided_description": "Add terms that identify the material displaced by the entity at time of sampling. Recommend subclasses of environmental material [ENVO:00010483]. Multiple terms can be separated by pipes e.g.: estuarine water [ENVO:01000301]|estuarine mud [ENVO:00002160]",
    "percentage": "7.058823529"
  },
  {
    "HarmonizedName": "env_package",
    "NCBI_provided_description": "MIGS/MIMS/MIENS extension for reporting of measurements and observations obtained from one or more of the environments where the sample was obtained. All environmental packages listed here are further defined in separate subtables. By giving the name of the environmental package, a selection of fields can be made from the subtables and can be reported",
    "percentage": "25.06778548"
  },
  {
    "HarmonizedName": "collection_date",
    "NCBI_provided_description": "the date on which the sample was collected; date/time ranges are supported by providing two dates from among the supported value formats, delimited by a forward-slash character; collection times are supported by adding \"T\", then the hour and minute after the date, and must be in Coordinated Universal Time (UTC), otherwise known as \"Zulu Time\" (Z); supported formats include \"DD-Mmm-YYYY\", \"Mmm-YYYY\", \"YYYY\" or ISO 8601 standard \"YYYY-mm-dd\", \"YYYY-mm\", \"YYYY-mm-ddThh:mm:ss\"; e.g., 30-Oct-1990, Oct-1990, 1990, 1990-10-30, 1990-10, 21-Oct-1952/15-Feb-1953, 2015-10-11T17:53:03Z; valid non-ISO dates will be automatically transformed to ISO format",
    "percentage": "61.78753889"
  },
  {
    "HarmonizedName": "sample_type",
    "NCBI_provided_description": "Sample type, such as cell culture, mixed culture, tissue sample, whole organism, single cell, metagenomic assembly",
    "percentage": "30.89120073"
  },
  {
    "HarmonizedName": "source_material_id",
    "NCBI_provided_description": "unique identifier assigned to a material sample used for extracting nucleic acids, and subsequent sequencing. The identifier can refer either to the original material collected or to any derived sub-samples.",
    "percentage": "4.961754716"
  },
  {
    "HarmonizedName": "bases",
    "NCBI_provided_description": "not_provided",
    "percentage": "99.49596141"
  },
  {
    "HarmonizedName": "bytes",
    "NCBI_provided_description": "not_provided",
    "percentage": "99.92393755"
  },
  {
    "HarmonizedName": "run_file_create_date",
    "NCBI_provided_description": "not_provided",
    "percentage": "99.92251049"
  },
  {
    "HarmonizedName": "run_file_version",
    "NCBI_provided_description": "not_provided",
    "percentage": "99.92251049"
  },
  {
    "HarmonizedName": "primary_search",
    "NCBI_provided_description": "not_provided",
    "percentage": "100"
  },
  {
    "HarmonizedName": "loaddate",
    "NCBI_provided_description": "The date when the data was loaded into SRA",
    "percentage": "100"
  },
  {
    "HarmonizedName": "mbases",
    "NCBI_provided_description": "Number of mega bases in the SRA Runs",
    "percentage": "100"
  },
  {
    "HarmonizedName": "mbytes",
    "NCBI_provided_description": "Number of mega bytes of data in the SRA Run",
    "percentage": "100"
  },
  {
    "HarmonizedName": "releasedate",
    "NCBI_provided_description": "The date on which the data was released",
    "percentage": "100"
  },
  {
    "HarmonizedName": "geo_loc_name_country_calc",
    "NCBI_provided_description": "Name of the country where the sample was collected",
    "percentage": "100"
  },
  {
    "HarmonizedName": "geo_loc_name_country_continent_calc",
    "NCBI_provided_description": "Name of the continent where the sample was collected",
    "percentage": "100"
  },
  {
    "HarmonizedName": "geo_loc_name_sam",
    "NCBI_provided_description": "Full location of collection",
    "percentage": "100"
  },
  {
    "HarmonizedName": "lat_lon",
    "NCBI_provided_description": "The geographical coordinates of the location where the sample was collected. Specify as degrees latitude and longitude in format \"d[d.dddd] N|S d[dd.dddd] W|E\", eg, 38.98 N 77.11 W",
    "percentage": "40.3180923"
  },
  {
    "HarmonizedName": "age",
    "NCBI_provided_description": "age at the time of sampling; relevant scale depends on species and study, e.g. could be seconds for amoebae or centuries for trees",
    "percentage": "8.667694152"
  },
  {
    "HarmonizedName": "body_habitat",
    "NCBI_provided_description": "original body habitat where the sample was obtained from",
    "percentage": "9.164882838"
  },
  {
    "HarmonizedName": "body_product",
    "NCBI_provided_description": "substance produced by the body, e.g. stool, mucus, where the sample was obtained from",
    "percentage": "9.467420156"
  },
  {
    "HarmonizedName": "host",
    "NCBI_provided_description": "The natural (as opposed to laboratory) host to the organism from which the sample was obtained. Use the full taxonomic name, eg, \"Homo sapiens\".",
    "percentage": "31.67736964"
  },
  {
    "HarmonizedName": "host_age",
    "NCBI_provided_description": "Age of host at the time of sampling",
    "percentage": "9.631246967"
  },
  {
    "HarmonizedName": "host_body_habitat",
    "NCBI_provided_description": "original body habitat where the sample was obtained from",
    "percentage": "7.597111625"
  },
  {
    "HarmonizedName": "host_body_product",
    "NCBI_provided_description": "substance produced by the host, e.g. stool, mucus, where the sample was obtained from",
    "percentage": "9.439592431"
  },
  {
    "HarmonizedName": "host_common_name",
    "NCBI_provided_description": "The natural language (non-taxonomic) name of the host organism, e.g., mouse",
    "percentage": "19.35453949"
  },
  {
    "HarmonizedName": "host_sex",
    "NCBI_provided_description": "Gender or physical sex of the host",
    "percentage": "5.932585552"
  },
  {
    "HarmonizedName": "host_subject_id",
    "NCBI_provided_description": "a unique identifier by which each subject can be referred to, de-identified, e.g. #131",
    "percentage": "32.49992865"
  },
  {
    "HarmonizedName": "host_taxid",
    "NCBI_provided_description": "NCBI taxonomy ID of the host, e.g. 9606",
    "percentage": "21.73873334"
  },
  {
    "HarmonizedName": "race",
    "NCBI_provided_description": "not_provided",
    "percentage": "4.543768017"
  },
  {
    "HarmonizedName": "sample_name",
    "NCBI_provided_description": "sample name in source database",
    "percentage": "100"
  },
  {
    "HarmonizedName": "sample_name_sam",
    "NCBI_provided_description": "INSDC sample name",
    "percentage": "100"
  },
  {
    "HarmonizedName": "acc",
    "NCBI_provided_description": "SRA Run accession in the form of SRR######## (ERR or DRR for INSDC partners)",
    "percentage": "100"
  },
  {
    "HarmonizedName": "bioproject",
    "NCBI_provided_description": "BioProject accession in the form of PRJNA######## (PRJEB####### or PRJDB###### for INSDC partners)",
    "percentage": "100"
  },
  {
    "HarmonizedName": "biosample",
    "NCBI_provided_description": "BioSample accession in the form of SAMN######## (SAMEA##### or SAMD##### for INSDC partners)",
    "percentage": "100"
  },
  {
    "HarmonizedName": "biosamplemodel_sam",
    "NCBI_provided_description": "The BioSample package/model that was picked",
    "percentage": "100"
  },
  {
    "HarmonizedName": "collection_date_sam",
    "NCBI_provided_description": "The collection date of the sample",
    "percentage": "100"
  },
  {
    "HarmonizedName": "consent",
    "NCBI_provided_description": "Type of consent need to access the data (i.e. public is available to all, others are for dbGaP)",
    "percentage": "100"
  },
  {
    "HarmonizedName": "datastore_filetype",
    "NCBI_provided_description": "Type of files available to download from SRA",
    "percentage": "100"
  },
  {
    "HarmonizedName": "datastore_provider",
    "NCBI_provided_description": "Locations of where the files are available to download from",
    "percentage": "100"
  },
  {
    "HarmonizedName": "datastore_region",
    "NCBI_provided_description": "Regions of where the data is located",
    "percentage": "100"
  },
  {
    "HarmonizedName": "ena_first_public_run",
    "NCBI_provided_description": "Date when INSDC partner record was public",
    "percentage": "100"
  },
  {
    "HarmonizedName": "ena_last_update_run",
    "NCBI_provided_description": "Date when INSDC partner record was updated",
    "percentage": "100"
  },
  {
    "HarmonizedName": "experiment",
    "NCBI_provided_description": "The accession in the form of SRX######## (ERX or DRX for INSDC partners)",
    "percentage": "100"
  },
  {
    "HarmonizedName": "sample_acc",
    "NCBI_provided_description": "SRA Sample accession in the form of SRS######## (ERS or DRS for INSDC partners)",
    "percentage": "100"
  },
  {
    "HarmonizedName": "sra_study",
    "NCBI_provided_description": "SRA Study accession in the form of SRP######## (ERP or DRP for INSDC partners)",
    "percentage": "100"
  },
  {
    "HarmonizedName": "investigation_type",
    "NCBI_provided_description": "Nucleic Acid Sequence Report is the root element of all MIGS/MIMS compliant reports as standardized by Genomic Standards Consortium. This field is either eukaryote,bacteria,virus,plasmid,organelle, metagenome, miens-survey or miens-culture",
    "percentage": "13.36529954"
  },
  {
    "HarmonizedName": "isolate",
    "NCBI_provided_description": "identification or description of the specific individual from which this sample was obtained",
    "percentage": "10.22847276"
  },
  {
    "HarmonizedName": "project_name",
    "NCBI_provided_description": "A concise name that describes the overall project, for example \"Analysis of sequences collected from Antarctic soil\"",
    "percentage": "15.96198305"
  },
  {
    "HarmonizedName": "assay_type",
    "NCBI_provided_description": "Type of library (i.e. AMPLICON, RNA-Seq, WGS, etc)",
    "percentage": "100"
  },
  {
    "HarmonizedName": "avgspotlen",
    "NCBI_provided_description": "Calculated average read length",
    "percentage": "100"
  },
  {
    "HarmonizedName": "center_name",
    "NCBI_provided_description": "Name of the sequencing center",
    "percentage": "100"
  },
  {
    "HarmonizedName": "insertsize",
    "NCBI_provided_description": "Submitter provided insert size",
    "percentage": "100"
  },
  {
    "HarmonizedName": "instrument",
    "NCBI_provided_description": "Name of the sequencing instrument model",
    "percentage": "100"
  },
  {
    "HarmonizedName": "library_name",
    "NCBI_provided_description": "The name of the library",
    "percentage": "100"
  },
  {
    "HarmonizedName": "librarylayout",
    "NCBI_provided_description": "Whether the data is SINGLE or PAIRED",
    "percentage": "100"
  },
  {
    "HarmonizedName": "libraryselection",
    "NCBI_provided_description": "Library selection methodology (i.e. PCR, RANDOM, etc)",
    "percentage": "100"
  },
  {
    "HarmonizedName": "librarysource",
    "NCBI_provided_description": "Source of the biological data (i.e. GENOMIC, METAGENOMIC, etc)",
    "percentage": "100"
  },
  {
    "HarmonizedName": "platform",
    "NCBI_provided_description": "Name of the sequencing platform (i.e. ILLUMINA)",
    "percentage": "100"
  }
]