# What is it?

MUP is a Markup previewer. You can use it to read text written in multiple
markup formats.

## Features

- Supports multiple markup formats, easy to extend
- Automatically refreshes itself when the document is modified, tries to retain
  the position in the document after refreshing
- Skips metadata headers, such as those used by static blog generators like Jekyll
- Supports gzipped documents, useful to read documentation shipped with Debian
  packages

## Supported Formats

MUP supports Markdown and reStructuredText using Python modules.

MUP also comes with an external process converter, which lets you use any
standalone binary as a converter as long as it accepts markup on stdin and
produces HTML on stdout.

By default, MUP comes with the following external converters:

- Markdown via Pandoc
- GitHub Flavored Markdown (Kramdown)
- CommonMark
- Gruber Markdown
- Ronn

# Usage

Start MUP like this:

    mup file.md

You can edit the file by clicking the "Edit" button. This will open your
preferred editor.

## Configuring the Editor

To configure which editor should be used, edit `~/.config/mup/mup.conf` and add
the following content:

    editor: name-of-your-editor

Note: for now you cannot define arguments for the editor. If you need arguments
you will have to write a wrapper shell script.

## Defining a new Converter

To declare the `foo2html` command as a converter for .foo or .foobar files,
create a `foo.conf` file in `/usr/share/mup/converters` or in
`~/.local/share/mup/converters` with the following content:

    name: Foo
    cmd: foo2html
    args: --some-arg 3
    matches: ["*.foo", "*.foobar"]

If MUP can find the `foo2html` binary, it should use it whenever it tries to
open a .foo file.

# Requirements

- PyQt4
- yaml
- pyxdg

Optional (for internal converters):

- markdown
- docutils

Optional tools:

- pandoc
- ronn
