#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT UTILITOR
#
# This file was automatically generated by Grako.
#
#    https://pypi.python.org/pypi/grako/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.


from __future__ import print_function, division, absolute_import, unicode_literals
from grako.parsing import graken, Parser
from grako.util import re, RE_FLAGS


__version__ = (2015, 6, 2, 19, 56, 12, 1)

__all__ = [
    'AstParser',
    'AstSemantics',
    'main'
]


class AstParser(Parser):
    def __init__(self, whitespace=None, nameguard=None, **kwargs):
        super(AstParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=None,
            eol_comments_re=None,
            ignorecase=None,
            **kwargs
        )

    @graken()
    def _node_(self):
        self._token('(')
        self._pattern(r'[^()]+')
        self.ast['name'] = self.last_node

        def block1():
            self._node_()
            self.ast.setlist('children', self.last_node)
        self._closure(block1)
        self._token(')')

        self.ast._define(
            ['name'],
            ['children']
        )


class AstSemantics(object):
    def node(self, ast):
        return ast


def main(filename, startrule, trace=False, whitespace=None, nameguard=None):
    import json
    with open(filename) as f:
        text = f.read()
    parser = AstParser(parseinfo=False)
    ast = parser.parse(
        text,
        startrule,
        filename=filename,
        trace=trace,
        whitespace=whitespace,
        nameguard=nameguard)
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(ast, indent=2))
    print()

if __name__ == '__main__':
    import argparse
    import string
    import sys

    class ListRules(argparse.Action):
        def __call__(self, parser, namespace, values, option_string):
            print('Rules:')
            for r in AstParser.rule_list():
                print(r)
            print()
            sys.exit(0)

    parser = argparse.ArgumentParser(description="Simple parser for Ast.")
    parser.add_argument('-l', '--list', action=ListRules, nargs=0,
                        help="list all rules and exit")
    parser.add_argument('-n', '--no-nameguard', action='store_true',
                        dest='no_nameguard',
                        help="disable the 'nameguard' feature")
    parser.add_argument('-t', '--trace', action='store_true',
                        help="output trace information")
    parser.add_argument('-w', '--whitespace', type=str, default=string.whitespace,
                        help="whitespace specification")
    parser.add_argument('file', metavar="FILE", help="the input file to parse")
    parser.add_argument('startrule', metavar="STARTRULE",
                        help="the start rule for parsing")
    args = parser.parse_args()

    main(
        args.file,
        args.startrule,
        trace=args.trace,
        whitespace=args.whitespace,
        nameguard=not args.no_nameguard
    )