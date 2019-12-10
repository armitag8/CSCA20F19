# Merge Marks

Takes spreadsheets (exported as CSV files) and merges them into a format that
can be directly uploaded to Canvas (AKA Quercus).

Optionally performs some simple analysis to visualize and describe the mark distribution.

## Requirements

For merging, only the standard Python3 library is required.

For analysis, both `pandas` and `matplotlib` are required:

```bash
pip3 install pandas
pip3 install matplotlib
```

## Usage

```text
Usage: merge_marks.py [OPTIONS] canvas_file [marks_file ...]
Options:
         -h, --help
         -i unique_id_canvas:unique_id_marksheet, --id=unique_id_canvas:unique_id_marksheet
         -e UTorIDs_file, --exclude=UTorIDs_file
         -o output_file, --output=output_file
         -c col1canvas:col1marks,col2canvas:col2marks, --columns=col1canvas:col1marks,col2canvas:col2marks
         -a, --analyze
         -f, --force
         -z, --zero-fill
```

The **simplest** invocation of this script might look like:

```bash
./mark.py --columns='Final Project (256801):Final Grade' canvas_template.csv marks*
```

Which makes the following assumptions:

- The `canvas_template` has all necessary PK columns for its system (see their docs or download one)
- The `canvas_template` has a column named `SIS Login ID` which matches the columns `UTorID`
    in the `marks*` files
- The column in the `marks*` files to be merged is exactly `Final Grade` and corresponds to the
    column in `canvas_template` named `Final Project (256801)`
- The output is destined for `stdout`

A **typical** invocation of this script might look like:

```bash
./mark.py -e exclude.txt \
    -c 'Final Project (256801):Final Grade' \
    -i 'SIS Login ID:UTorID' \
    -e cheaters.txt \
    -o upload_me_to_quercus.csv \
    CSCA20_Quercus.csv \
    CSCA20_Project_Marks_Tut*
```

### Mandatory arguments

At least the `canvas_template` and some input marking files must be supplied, as well as the
`--columns` option.

### Options

- `-h` or `--help`: display usage message
- `-i` or `--id`: map mark sheets' unique ID to Canvas unique ID.
  - ARG: a single colon-separated key-value pair, ex: `unique_id_canvas:unique_id_marksheet` 
- `-e` or `--exclude`: unique IDs to NOT be marked
  - ARG: a file name containing one unique ID per line, ex: `UTorIDs_file.txt`
- `-o` or `--output`: output_file
  - ARG: a file name to contain the output marks CSV, ex: `output.csv`
- `-c` or `--columns`:
  - ARG: comma-separated key-value pairs (each colon-separated)
    - ex: `col1canvas:col1marks,col2canvas:col2marks`
    - Specifies the mapping of column headers in the marks files to column headings in the Canvas file
    - Case sensitive, one pair per mapping
- `-a` or `--analyze`: enable analysis output
  - Note: both `pandas` and `matplotlib` are required
  - Statistics output: `<ANALYTICS_DIRECTORY>/<output_filename>_<column>.<STATS_FILE_FORMAT>`
  - Graph output: `<ANALYTICS_DIRECTORY>/<output_filename>_<column>.<FIGURE_FILE_FORMAT>`
- `-f` or `--force`: overwrite known entries (from `canvas_template.csv` with those from the mark input files, for any columns specified.
- `-z` or `--zero`: fill empty marks with 0

## Input and Output

In standard 'nix tool fashion:

- Reads 0 (from stdin) or more `marks_file`s and merges their data.
- Writes to stdout, unless overridden by supplying an argument to `--output`.

### CSV Format

All CSV Files **must** have header rows. The columns in `canvas_file` to be updated
**must** be mapped to columns in one ore more `mark_file`s, using `--columns`.

Marks in the CSV files may be of any numerical format. Percent signs are stripped.
