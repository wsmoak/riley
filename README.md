# Riley

Ellie's best friend.  A Python package of useful code for working with the
PDF and CSV export files from the [Ellie.ai](https://www.ellie.ai/)
data modeling system.

## Installation

Clone the repository, change into the directory, and then `pip install -e .`

This installs the package in editable mode, which allows you to modify the code without re-installing.

## Usage

```
python -m riley report --model Store-Purchase_CM --date 2024-01-14_14-35
```

Note that if the minute ticked over while you were exporting the files, you may need to rename them so the timestamps match.

```
python -m riley sort --model Store-Purchase
```

If you have renamed the files to remove the date and time, omit the --date argument.

The 'Notes' field on each attribute should be a pipe delimited list of items.  If an item is prefixed by 'Note: ' or 'Examples: ' then it will appear in the report.

```
usage: riley [-h] [-a ACCOUNT] [-m MODEL] [-d DATE] {report,sort}

positional arguments:
  {report,sort}         report: produce a pdf report of the model, entities, and attributes. sort: sort the
                        csv files so git diff is useful

options:
  -h, --help            show this help message and exit
  -m MODEL, --model MODEL
                        the name of your Ellie model, with dashes instead of spaces, to construct the
                        filenames
  -d DATE, --date DATE  the date in YYYY-MM-DD_HH-MM format, to construct the filenames. Optional in case you
                        rename the files without the date.
```