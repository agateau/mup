#!/usr/bin/env python3
import argparse
import re
import subprocess
import sys


CMD = ['groff',
    '-P', '-r', # No hr at the end of the page
    '-K', 'utf-8',
    '-mandoc', '-Thtml']

NAME_RE = r'([-_.a-zA-Z0-9]+)'
SECTION_RE = r'\((\d+[px]?)\)'

SECTION_LETTER_RX = re.compile(r'[a-z]+$')

INSTALLED_LINK = '<a href="{}">{}({})</a>'

NOT_INSTALLED_LINK = '<a style="border-bottom: 1px dotted red; cursor: not-allowed" title="Not installed">{}({})</a>'

# Keys: (name, section) => path
g_man_page_cache = {}
def find_man_page(name, section):
    global g_man_page_cache
    try:
        return g_man_page_cache[(name, section)]
    except KeyError:
        pass

    num_section = SECTION_LETTER_RX.sub('', section)
    cmd = ['man', '--where', num_section]
    cmd.append(name)
    try:
        path = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).strip().decode('utf-8')
    except subprocess.CalledProcessError:
        path = None
    g_man_page_cache[(name, section)] = path
    return path


def process_links(html, find_man_page_fcn):
    def repl(match):
        name = match.group(1)
        section = match.group(2)
        path = find_man_page_fcn(name, section)
        if path:
            return INSTALLED_LINK.format(path, name, section)
        else:
            return NOT_INSTALLED_LINK.format(name, section)
    return re.sub(r'<[bi]>' + NAME_RE + '</[bi]>' + SECTION_RE,
        repl, html)


def convert(inputfp, find_man_page_fcn=find_man_page):
    popen = subprocess.Popen(CMD, stdin=inputfp,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = popen.communicate()
    stdout = stdout.decode('utf-8')

    # Turn '&minus' back into '-' so that options (-f, --quiet...) are easier to
    # search
    stdout = stdout.replace('&minus;', '-')
    return process_links(stdout, find_man_page_fcn=find_man_page_fcn)


def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    out = convert(sys.stdin)
    print(out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
# vi: ts=4 sw=4 et
