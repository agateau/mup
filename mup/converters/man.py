#!/usr/bin/env python3
import argparse
import re
import subprocess
import sys


CMD = ['groff', '-K', 'utf-8', '-mandoc', '-Thtml']


# Keys: (name, section) => path
g_man_page_cache = {}
def find_man_page(name, section):
    global g_man_page_cache
    try:
        return g_man_page_cache[(name, section)]
    except KeyError:
        pass

    cmd = ['man', '--where', section]
    cmd.append(name)
    try:
        path = subprocess.check_output(cmd).strip()
    except subprocess.CalledProcessError:
        path = None
    g_man_page_cache[(name, section)] = path
    return path


def process_links(html, find_man_page_fcn):
    def repl(match):
        name = match.group(1)
        section = match.group(2)
        path = find_man_page_fcn(name, section)
        if path is None:
            return match.group(0)
        return '<a href="{}">{}({})</a>'.format(path, name, section)
    return re.sub(r'<b>([-_.a-zA-Z0-9]+)</b>\((\d+)\)',
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
