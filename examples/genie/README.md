# Genie

A Python program which prints the Genome data read from a FASTA file.

Genie is a genome explorer that reads, parses and prints data from FASTA (format) files.\r\n The data from these files describe genome sequences and are available for many species at [Ensembl](http://useast.ensembl.org/info/data/ftp/index.html)

## Requirements

- Python3
- IMPORTANT: Please note you can download correlation data tables,
supported by Ensembl, via the highly customisable BioMart and
EnsMart data mining tools. See http://www.ensembl.org/biomart/martview or
http://www.ebi.ac.uk/biomart/ for more information.


## Build  and run

- Read [The Handout](https://github.com/armitag8/CSCA20F19/raw/master/examples/genie/handout.pdf)
- Download all files and folders in this folder (into the same folder)
- Download some sample data (from [Ensembl](http://useast.ensembl.org/info/data/ftp/index.html), probably), for example: ftp://ftp.ensembl.org/pub/release-98/fasta/homo_sapiens/cds/
- Make sure the file you downloaded is in the same folder as `genie.py` and that the `FILENAME` variable there matches the filename of what you downloaded.
- Double-click `genie.py`


## About FASTA
### FASTA CDS dumps

These files hold the coding sequences corresponding to Ensembl gene 
predictions. CDS does not contain UTR or intronic sequence.


### FASTA File Names

The files are consistently named following this pattern:
```
<species>.<assembly>.<sequence type>.<status>.fa.gz
```
Where each of the `<variables>` mean:
- `<species>:` The systematic name of the species.
- `<assembly>`: The assembly build name.
- `<sequence type>`: cds for CDS sequences
- `<status>`
  * 'cds.all' The super-set of all transcripts coding sequences resulting from
     Ensembl gene predictions (see more below).

#### EXAMPLES  
**Note**: Most species do not have sequences for each different `<status>`

- Human:
  - CDS sequences for all transcripts: `Homo_sapiens.NCBI37.cds.all.fa.gz`

### FASTA Sequence Header Lines

The FASTA sequence header lines are designed to be consistent across
all types of Ensembl FASTA sequences.  This gives enough information
for the sequence to be identified outside the context of the FASTA file.

#### General format

```
>ID SEQTYPE:STATUS LOCATION GENE
```

#### Example of an Ensembl CDS header

```
>ENST00000525148 cds chromosome:GRCh37:11:66188562:66193526:1 gene:ENSG00000174576 gene_biotype:protein_coding transcript_biotype:nonsense_mediated_decay
 ^               ^    ^     ^                                       ^                    ^                           ^       
 ID              |    |  LOCATION                         GENE: gene stable ID        GENE: gene biotype        TRANSCRIPT: transcript biotype
                 |  STATUS
              SEQTYPE
```

