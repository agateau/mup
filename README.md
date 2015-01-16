# MUP: a Markup Previewer

MUP is a markup previewer. It supports multiple markup formats. You can use it
to read markup text, but it is also useful when writing markup text to check
how your work looks, thanks to its refresh-as-you-save feature.

![MUP in action](http://agateau.com/hotlink/mup.png)

## Features

- Supports multiple markup formats, easy to extend
- Automatically refreshes itself when the document is modified, tries to retain
  the position in the document after refreshing
- Skips metadata headers, such as those used by static blog generators like
  Jekyll
- Supports gzipped documents, useful to read documentation shipped with Debian
  packages
- Comes with a wrapper for man pages

## Supported Formats

MUP supports Markdown and reStructuredText using Python modules.

It also supports the following formats using external converters:

- Markdown via Pandoc
- GitHub Flavored Markdown via Kramdown
- CommonMark
- Gruber Markdown
- Ronn
- Man pages via groff
- Asciidoc

External converters are command line tools which are invoked by MUP to convert
input files. To be used as an external converter, the tool must accept markup
on stdin and produces HTML on stdout.

# Usage

Start MUP like this:

    mup markup_file

To read a man page with mup:

    mupman ls

Or:

    mupman 5 crontab

## Editing files

You can edit the current file by clicking the "Edit" button. This will open
it in your preferred editor.

To configure which editor should be used, edit `~/.config/mup/mup.yaml` and add
the following content:

    editor: name-of-your-editor

Note: for now you cannot define arguments for the editor. If you need arguments
you will have to write a wrapper shell script.

## Defining a new Converter

To declare the `foo2html` command as a converter for .foo or .foobar files,
create a `foo.yaml` file in `/usr/share/mup/converters` or in
`~/.local/share/mup/converters` with the following content:

    name: Foo
    cmd: foo2html
    matches: ["*.foo", "*.foobar"]

If MUP can find the `foo2html` binary, it will use it whenever it tries to open
a .foo file.

Other optional keys:

- `args`: Arguments to pass to the command
- `full`: Set to true if the command creates a complete HTML document, not just
  an HTML snippet (defaults to false)

# Requirements

Mandatory Python modules:

- PyQt4
- yaml
- pyxdg

Optional Python modules (for internal converters):

- markdown
- docutils

Optional tools (for external converters):

- pandoc
- ronn
- groff, for man pages
- asciidoc

## Installation

Run `python setup.py install` as root.

## Contributing

MUP is managed using the [lightweight project management policy][lpmp].

Get the code from `https://github.com/agateau/mup` then file pull requests
against the `dev` branch.

[lpmp]: http://agateau.com/2014/lightweight-project-management

## Author

Aurélien Gâteau

## License

BSD
