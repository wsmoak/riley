# Riley

Ellie's best friend.  A Python package of useful code for working with the
PDF and CSV export files from the [Ellie.ai](https://www.ellie.ai/)
data modeling system.

## Usage

```
python -m riley report --account wendy --model Store-Purchase --date 2024-01-14
```

```
python -m riley -h
usage: riley [-h] [-a ACCOUNT] [-m MODEL] [-d DATE] {report}

positional arguments:
  {report}              report: produce a pdf report of the model, entities,
                        and attributes.

optional arguments:
  -h, --help            show this help message and exit
  -a ACCOUNT, --account ACCOUNT
                        your Ellie.ai account name, the prefix of the export
                        files
  -m MODEL, --model MODEL
                        the name of your Ellie model, with dashes instead of
                        spaces, to construct the filenames
  -d DATE, --date DATE  the date in YYYY-MM-DD format, to construct the
                        filenames
```