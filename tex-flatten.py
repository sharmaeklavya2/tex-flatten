#!/usr/bin/env python3

"""Takes as input a multi-file TeX project and returns a single equivalent TeX file
after removing comments and replacing calls to \\input."""

from __future__ import print_function
import sys
import argparse
import re


COMMENT_RE = r'(?<!\\)%[^\n]*\n'
INPUT_RE = r'\\(input){([^}]+)}'
DEFAULT_IGNORE_ENVS = ['comment', 'error']


try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


def warn(*args):
    print('tex-flatten: WARNING:', *args, file=sys.stderr)


def debug(*args):
    print('tex-flatten:', *args, file=sys.stderr)


def remove_comments(s, ifpath, ignore_envs):
    s = re.sub('% tex-flatten:ignore-(begin|end)', r'\\\1{tex-flatten-force-ignore}', s)
    s = re.sub(COMMENT_RE, '%\n', s, flags=re.MULTILINE)
    ignore_env_re = r'\\(begin|end){(' + '|'.join(ignore_envs) + ')}'
    parts = []
    stack = []
    last_pos = 0
    for match in re.finditer(ignore_env_re, s):
        if match.group(1) == 'begin':
            if not stack:
                parts.append(s[last_pos: match.start()])
            stack.append(match.group(2))
        elif stack:
            if stack[-1] != match.group(2):
                warn(r"\begin and \end don't match in " + ifpath)
            stack.pop()
            if not stack:
                last_pos = match.end()
        else:
            warn(r"extra \end in " + ifpath)
    if stack:
        warn(r"\end not found in " + ifpath)
    else:
        parts.append(s[last_pos:])
    return ''.join(parts)


def recursive_read(fpath, ignore_envs, parts):
    with open(fpath) as fp:
        s = fp.read()
    s = remove_comments(s, fpath, ignore_envs)
    last_pos = 0
    for match in re.finditer(INPUT_RE, s):
        fpath2 = match.group(2)
        if '.' not in fpath2:
            fpath2 += '.tex'
        parts.append(s[last_pos: match.start()])
        recursive_read(fpath2, ignore_envs, parts)
        last_pos = match.end()
    parts.append(s[last_pos:])


def replace_bib(s, bbl_path, read_file):
    s = re.sub(r'\\bibliographystyle{[^}]+}', '', s)
    if read_file:
        with open(bbl_path) as fp:
            repl = fp.read()
    else:
        repl = r'\input{' + bbl_path + '}'
    return re.sub(r'\\bibliography{[^}]+}', (lambda match: repl), s, count=1)


def clean(s):
    return re.sub(r'\n{3,}', '\n\n', s, flags=re.MULTILINE)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ifpath')
    parser.add_argument('-o', '--output', help='path to output file')
    parser.add_argument('--ignore', dest='ignore_envs', action='append',
        help='environments to ignore')
    bblGroup = parser.add_mutually_exclusive_group()
    bblGroup.add_argument('--bbl-to-read',
        help='path to bbl file. Read its contents and put in tex file.')
    bblGroup.add_argument('--bbl-to-link',
        help='path to bbl file. \\input it in tex file.')
    parser.add_argument('--no-clean', dest='clean', action='store_false', default=True,
        help='do not remove consecutive empty lines')
    args = parser.parse_args()

    args.ignore_envs = args.ignore_envs or DEFAULT_IGNORE_ENVS
    args.ignore_envs.append('tex-flatten-force-ignore')
    args.ignore_envs = tuple(args.ignore_envs)

    parts = []
    recursive_read(args.ifpath, args.ignore_envs, parts)
    s = ''.join(parts)

    bbl_path = args.bbl_to_read or args.bbl_to_link
    if bbl_path is not None:
        s = replace_bib(s, bbl_path, args.bbl_to_read is not None)
    if args.clean:
        s = clean(s)
    if args.output is None:
        print(s)
    else:
        with open(args.output, 'w') as ofp:
            ofp.write(s)


if __name__ == '__main__':
    main()
