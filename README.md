# open-mary-python

A simple Python runner for doing phoneme translation with the Open Mary online API

## Usage

Run the python script `translate.py` from the project directory. Here's a paste of the help message for the script:

```
usage: translate.py [-h] [-d] [-i INTERVAL] [-f FORMAT] [-x EXT]
                    in_path out_path locale

positional arguments:
  in_path               path to input
  out_path              path to output
  locale                target locale ('en_US' - (US) English, 'fr' - French,
                        or 'de' - German)

optional arguments:
  -h, --help            show this help message and exit
  -d, --dir             input and output correspond to directories
  -i INTERVAL, --interval INTERVAL
                        interval (seconds) between translation of files (only
                        applicable to directories)
  -f FORMAT, --format FORMAT
                        format of output ('txt' or 'xml')
  -x EXT, --ext EXT     file extension for output files (only applicable to
                        directories)
```
