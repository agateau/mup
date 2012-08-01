# What is it?

Mdview is a markdown viewer and browser. You can use it to view markdown files
and create lightweight wiki-like structures.

Markdown is a simple markup language. See http://daringfireball.net/markdown/

# Usage

Start mdview like this:

    mdview file.md

You can edit the file by clicking the "Edit" button. This will open your
preferred editor.

You can create linked pages by adding links to other files which end with
".md".

## Configuring the editor

To configure which editor should be used, edit `~/.config/mdview.conf` and add
the following content:

    [general]
    editor=name-of-your-editor

Note: for now you cannot define arguments for the editor. If you need arguments
you will have to write a wrapper shell script.

# Requirements

- PyQt4

# Other pages

- [Another page](subpage1.md)
- [A page which does not exist](not_there.md)
