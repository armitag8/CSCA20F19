#!/usr/bin/env python3

import sys
from pathlib import Path
from csv import DictReader as reader, DictWriter as writer

# default primary key join
UNIQUE_ID_MARKS = "UTorID"
UNIQUE_ID_CANVAS = "SIS Login ID"

# For analytics output
ANALYTICS_DIRECTORY = "analytics"
FIGURE_FILE_FORMAT = ".svg"
STATS_FILE_FORMAT = ".csv"
HISTOGRAM_GRANULARITY = 20  # number of bins


def read_ids_from(id_filename: str):
    """Read one string per line from id_filename. Use to load list of UIDs."""
    ids = []
    try:
        with open(id_filename) as id_file:
            for line in id_file:
                ids.append(line.strip())
    except FileNotFoundError:
        print("Cannot find file: " + id_filename, file=sys.stderr)
        sys.exit(3)
    return ids


def output_merged_marks(file_handle: "FILE", merged_marks: "OrderedDict"):
    """Write all of the merged_marks out in a CSV format to file_handle."""
    csv_writer = writer(file_handle, merged_marks[0].keys())
    csv_writer.writeheader()
    csv_writer.writerows(merged_marks)


def mark(unique_id_map: tuple, canvas_filename: str, mark_file: "FILE",
         exclude: list = [], join: dict = {}, override: bool = False):
    """
    Merge columns (those specified in join) from the mark_file into a
    single file of the format of canvas_filename, where:
        - the unique_id_map:
            - maps a field in this row to one in matching one in mark_file
            - does not contain a value in the exclude list
        - if override:
            - merge if the mark_file has data for that cell
          otherwise:
            - only merge if no data exists in the canvas file for that cell
    """
    def _join_entries(uid: str, input_row: dict, join_columns: list, canvas_data: list):
        for canvas_column, marksheet_column in join_columns:
            if marksheet_column not in input_row:
                continue
            new_mark = input_row[marksheet_column].strip().rstrip("%")
            found = False
            for canvas_entry in canvas_data:
                entry_uid = canvas_entry[unique_id_map[0]].strip().lower()
                if uid == entry_uid:
                    if override or not canvas_entry[canvas_column].strip():
                        canvas_entry[canvas_column] = new_mark
                    found = True
                    break
            if not found:
                print("Not updated: " + uid, file=sys.stderr)

    def read_canvas(file_name: str):
        with open(file_name) as canvas_file:
            return [line for line in reader(canvas_file)]

    uid_canvas, uid_marks = unique_id_map

    # get original data from canvas
    canvas_data = [e for e in read_canvas(canvas_filename) if uid_canvas in e]
    original = read_canvas(canvas_filename)

    # check there are students in canvas_file
    if len(canvas_data) == 0:
        print("No students to be updated in canvas file.", file=sys.stderr)
        return []

    # check for matching columns to be joined from
    marks = [row for row in reader(mark_file) if uid_marks in row]
    update_columns = [(k, v) for k, v in join.items() if v in marks[0]]
    for column in join.values():
        if column not in marks[0]:
            print("Column {} not found in file {}"
                  .format(column, mark_file.name), file=sys.stderr)

    # check there are still columns to be updated
    if len(update_columns) == 0:
        print("No matching columns in canvas file.", file=sys.stderr)
        return []

    # join new data into canvas_data
    for row in marks:
        unique_id = row[uid_marks].strip().lower()
        if unique_id and unique_id not in exclude:
            _join_entries(unique_id, row, update_columns, canvas_data)

    # return only entries with changes
    return [e for e in canvas_data if e not in original]


def run_analytics(data: list, *columns: str) -> dict:
    """
    Given grade data, for each of the columns, return functions to output:
        - some simple statistics to a given filename
        - a graph of students' grade distribution to a given filename
    """
    try:
        import matplotlib.pyplot as plt
        import pandas as pd
    except ModuleNotFoundError as e:
        print(e, file=sys.stderr)
        sys.exit(4)

    data_frame = pd.DataFrame.from_dict(data)
    data_frame[list(columns)] = data_frame[list(columns)].apply(pd.to_numeric)

    analytics = {}

    for column in columns:
        if column not in data_frame:
            print("Column not found for analytics: " + column, file=sys.stderr)
            continue

        # simple statistics
        def statistics(filename: str):
            return data_frame[column].describe().to_csv(filename, header=False)

        # grade distribution histogram
        def graph(filename: str):
            data_frame.hist(column=column, bins=HISTOGRAM_GRANULARITY)
            plt.xlabel("Percentage Grade")
            plt.ylabel("Number of Students")
            plt.savefig(filename)

        analytics[column] = statistics, graph

    return analytics


if __name__ == "__main__":
    import getopt

    def usage():
        print("Usage: " + Path(__file__).name +
              " [OPTIONS] canvas_file [marks_file ...]")
        print("Options:")
        print("\t -h, --help")
        print("\t -i unique_id_canvas:unique_id_marksheet, " +
              "--id=unique_id_canvas:unique_id_marksheet")
        print("\t -e UTorIDs_file, --exclude=UTorIDs_file")
        print("\t -o output_file, --output=output_file")
        print("\t -c col1canvas:col1marks,col2canvas:col2marks, " +
              "--columns=col1canvas:col1marks,col2canvas:col2marks")
        print("\t -a, --analyze")
        print("\t -f, --force")
        print("\t -z, --zero-fill")
        sys.exit(2)

    # parse command line args
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:e:o:c:afz",
                                   ["help", "id=", "exclude=", "output=",
                                    "columns=", "analyze", "force", "zero-fill"])
    except getopt.GetoptError as err:
        print(err)
        usage()

    # extract positional parameters
    if args == []:
        print("Canvas file must be supplied.")
        usage()
    else:
        canvas_file = args[0]
        input_files = args[1:]

    # default parameters
    columns = {}
    exclude_ids = []
    output_filename = None
    analyze = False
    force = False
    zero_fill = False
    unique_id = UNIQUE_ID_CANVAS, UNIQUE_ID_MARKS

    # extract optional parameters
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-i", "--id"):
            unique_id = tuple(a.strip() for a in arg.split(":"))
        elif opt in ("-e", "--exclude"):
            exclude_ids = read_ids_from(arg)
        elif opt in ("-o", "--output"):
            output_filename = arg
        elif opt in ("-c", "--columns"):
            columns = {k.strip(): v.strip() for k, v in
                       map(lambda c: c.strip().split(":"), arg.split(","))}
        elif opt in ("-a", "--analyze"):
            analyze = True
        elif opt in ("-f", "--force"):
            force = True
        elif opt in ("-z", "--zero-fill"):
            zero_fill = True

    # TODO: automate finding these
    if columns == {}:
        print("Specify columns on which to join or analyze.", file=sys.stderr)
        usage()

    if len(unique_id) != 2:
        print("Unique ID map must have exactly 2 values.", file=sys.stderr)
        usage()

    def merge(file_handle: "FILE" = sys.stdin) -> list:
        return mark(unique_id, canvas_file, file_handle,
                    exclude=exclude_ids,
                    join=columns,
                    override=force)

    # update marks with input from command-line argument files
    if input_files != []:
        output = []
        for input_file in input_files:
            with open(input_file) as input_file_handle:
                output.extend(merge(input_file_handle))
    else:  # or from stdin
        output = merge()

    if output == []:
        print("No marks output generated", file=sys.stderr)
        sys.exit(0)

    # post-process marks data
    if zero_fill:
        for row in output:
            for column in columns:
                if not row[column].strip():
                    row[column] = 0

    # output updated grade data
    if output_filename:
        with open(output_filename, "w") as out:
            output_merged_marks(out, output)
    else:
        output_merged_marks(sys.stdout, output)

    # do analysis
    if analyze:
        analytics = run_analytics(output, *columns.keys())

        directory = Path(ANALYTICS_DIRECTORY)
        if not directory.exists():
            directory.mkdir()

        path_stem = Path(output_filename).stem + "_" if output_filename else ""
        for column, functions in analytics.items():
            output_path = directory.joinpath(path_stem + column)
            output_statistics, make_figure = functions
            make_figure(output_path.with_suffix(FIGURE_FILE_FORMAT))
            output_statistics(output_path.with_suffix(STATS_FILE_FORMAT))
