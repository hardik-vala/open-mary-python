# open-mary-python

A simple Python runner for doing phoneme translation with the Open Mary online API.

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

For example,

```
python translate.py my_file.ext my_file.xml fr -f xml
```

will translate the file `my_file.ext` under the French locale and save the translation in Open Mary's XML format to  `my_file.xml`.

As another example,

```
python translate.py /path/to/my/input/dir/ /path/to/my/outout/dir/ de -d -i 5 -f txt -x .translation
```

will translate each (non-hidden) file `my_file.ext` in the directory `/path/to/my/input/dir/` to a text file in `/path/to/my/output/dir/my_file.translation` (since directory mode is initiated with `-d`) with the tokens replaced by their phonetic translation (under the German locale in this case), with each phoneme separated by a space (since `txt` is the specified format). The file is also tokenized according to tokens (separated by a single space so word boundaries are lost), sentences (separated by a single CR), and paragraphs (seperated by a double CR). `-i 5` specifies a timeout of 5 seconds in-between file translations in order to prevent overloading the Mary TTS server.
