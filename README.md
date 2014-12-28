# What is it?

MUP is a markup reader. You can use it to read text written in multiple markup
formats. MUP supports many Markdown flavors, reStructuredText and can easily be
extended to support other formats.

# Usage

Start MUP like this:

    mup file.md

You can edit the file by clicking the "Edit" button. This will open your
preferred editor.

## Configuring the editor

To configure which editor should be used, edit `~/.config/mup.conf` and add
the following content:

    editor: name-of-your-editor

Note: for now you cannot define arguments for the editor. If you need arguments
you will have to write a wrapper shell script.

# Requirements

- PyQt4
- yaml

Optional, but you want at least one:

- markdown
- docutils
- pandoc
