### MHTMLconverter

This package intends to provide tools to convert markdown or html files including images to a single MHTML self-content file.

Tested on Windows. Should work elsewhere...

### html2mtml

Converts html files (either local or remote) to mhtml, including referenced images.

```
>> python -m mhtmlconverter.cli.html2mhtml -i index.html -o my_output.mhtml

>> python -m mhtmlconverter.cli.html2mhtml -i http://github.com # default output is output.mhtml
```

### md2mtml

Converts markdown files (either local or remote) to mhtml, including referenced images.

```
>> python -m mhtmlconverter.cli.md2mhtml -i README.md -o my_output.mhtml

```

### mhtml2html

Converts mhtml file (either local or remote) to local html with referenced images in a _resource dir.

By default the html file is created in the same dir as the mhtml file (and so is the resources_dir)

If the path to the html file is different, by default, the resources_dir is in the same dir

If the resource dir is different, the references in the html file are rewritten according to
this location

```
>> python -m mhtmlconverter.cli.mhtml2html -i index.mhtml -o index.html -r resources_dir

```

### html2mtml, md2mtml, mhtml2html

Those scripts should work...

```
    >>> html2mtml --help
    >>> md2mtml --help
    >>> mhtml2html --help

```