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


__version__ = (2015, 11, 11, 19, 32, 31, 2)

__all__ = [
    'AstParser',
    'AstSemantics',
    'main'
]


class AstParser(Parser):
    def __init__(self,
                 whitespace=None,
                 nameguard=None,
                 comments_re=None,
                 eol_comments_re=None,
                 ignorecase=None,
                 left_recursion=True,
                 **kwargs):
        super(AstParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            left_recursion=left_recursion,
            **kwargs
        )

    @graken()
    def _identifier_(self):
        self._pattern(r'#\w+')

    @graken()
    def _node_(self):
        self._token('(')
        with self._optional():
            self._identifier_()
            self.ast['id'] = self.last_node
        self._pattern(r'[^()]+')
        self.ast['label'] = self.last_node

        def block2():
            self._node_()
            self.ast.setlist('children', self.last_node)
        self._closure(block2)
        self._token(')')

        self.ast._define(
            ['id', 'label'],
            ['children']
        )

    @graken()
    def _edge_(self):
        self._identifier_()
        self.ast['src'] = self.last_node
        self._token('to')
        self._identifier_()
        self.ast['dst'] = self.last_node
        self._token(';')

        self.ast._define(
            ['src', 'dst'],
            []
        )

    @graken()
    def _ast_(self):
        self._token('(')
        with self._optional():
            self._identifier_()
            self.ast['id'] = self.last_node
        self._pattern(r'[^()]+')
        self.ast['label'] = self.last_node

        def block2():
            self._node_()
            self.ast.setlist('children', self.last_node)
        self._closure(block2)
        self._token(')')


        def block4():
            self._edge_()
            self.ast.setlist('edges', self.last_node)
        self._closure(block4)

        self.ast._define(
            ['id', 'label'],
            ['children', 'edges']
        )


class AstSemantics(object):
    def identifier(self, ast):
        return ast

    def node(self, ast):
        return ast

    def edge(self, ast):
        return ast

    def ast(self, ast):
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
