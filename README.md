### MHTMLconverter

This package intends to provide tools to convert markdown or html files including images to a single MHTML self-content file.

Tested on Windows. Should work elsewhere...

### html2mtml

Converts html files (either local or remote) to mhtml, including referenced images.

```
>> python html2mhtml.py -i index.html -o my_output.mhtml

>>  python html2mhtml.py -i http://github.com # default output is output.mhtml
```

### md2mtml

Converts markdown files (either local or remote) to mhtml, including referenced images.

```
>> python md2mhtml.py -i README.md -o my_output.mhtml

```

### TODO

css are not yet managed :/
