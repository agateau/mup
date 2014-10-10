# What is it?

Mdview is a markdown and rst viewer and browser. You can use it to view
markdown or rst files and create lightweight wiki-like structures.

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

    editor: name-of-your-editor

Note: for now you cannot define arguments for the editor. If you need arguments
you will have to write a wrapper shell script.

# Requirements

- PyQt4
- yaml

Optional, but you want at least one of those:

- markdown
- docutils
- pandoc
