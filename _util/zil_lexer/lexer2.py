from __future__ import absolute_import

from collections import namedtuple
import re

from pygments.lexer import RegexLexer, include, bygroups, words, \
    default, using, this
from .tokens import *   #XXX

# from . import builtins as zb

class ZilLexer(RegexLexer):
    """
    A ZIL lexer.
    """
    name = 'ZIL'
    aliases = ['zil', 'mdl', 'muddle']
    filenames = ['*.zil', '*.mud']
    mimetypes = ['text/x-zil', 'application/x-zil',
                 'text/x-mdl', 'application/x-mdl',
                 'text/x-muddle', 'application/x-muddle']
    flags = re.IGNORECASE | re.MULTILINE | re.DOTALL

    # list of known keywords and builtins
    # MDL_FSUBRS = zb.MDL_FSUBRS
    # MDL_SUBRS = zb.MDL_SUBRS
    # ZIL_FSUBRS = zb.ZIL_FSUBRS
    # ZIL_SUBRS = zb.ZIL_SUBRS
    # ZIL_SPECIAL_OPS = zb.ZIL_SPECIAL_OPS
    # ZIL_OPCODES = zb.ZIL_OPCODES
    # MDL_TYPES = zb.MDL_TYPES
    # ZIL_TYPES = zb.ZIL_TYPES
    # SPECIAL_ATOMS = zb.SPECIAL_ATOMS
    # IFVERSION_ATOMS = zb.IFVERSION_ATOMS
    # ARGSPEC_STRINGS = zb.ARGSPEC_STRINGS

    # valid names for identifiers
    # well, names can only not consist fully of numbers
    # but this should be good enough for now

    delimiters = r' \t-\r,#\':;%()\[\]<>\{\}"'
    non_atom_char = r'[%s]' % delimiters
    atom_head = r'(?:\\.|[^!\.%s])' % delimiters
    atom_tail = r'(?:\\.|[^%s])' % delimiters
    valid_atom = r'%s%s*' % (atom_head, atom_tail)

    integer_re = re.compile(r'-?\d+\.?\Z', flags)
    octal_re = re.compile(r'\*[0-7]+\*\Z', flags)
    # float_re = re.compile(r'-?\d+\.(\d+)([eE][-+]?\d+)', flags)

    def atomlike_callback(self, match,
                          integer_re=integer_re, octal_re=octal_re):
        text = match.group()
        if integer_re.match(text):
            ttype = Number.Integer
        elif octal_re.match(text):
            ttype = Number.Oct
        else:
            ttype = Name
        yield match.start(), ttype, text

    tokens = {
        'root': [
            default('expr'),
        ],
        'expr': [
            include('base-expr'),
            (r'!.', Error),     # unrecognized bang sequence
        ],
        'base-expr': [
            include('whitespace'),
            include('simple-expr'),
            include('bracketed'),
            include('prefixed'),
        ],
        'whitespace': [
            (r'\s+', Whitespace),
        ],
        'simple-expr': [
            # atom or number
            (valid_atom, atomlike_callback),

            # hash prefix
            (r'#\s*0*2\s+[01]+(?=%s|\Z)' % non_atom_char, Number.Bin),
            (r'(#\s*%s)(\s*)' % valid_atom,
             bygroups(Punctuation.Prefix.Hash, Whitespace.Unstyled)),

            # strings, symbols and characters
            (r'(")((?:[^\\"]|\\.)*)(")',
             bygroups(String.Double.Begin, String.Double, String.Double.End)),
            (r'![\\"].', String.Char),

            # FALSE
            (r'<\s*>', Keyword.Constant.False),
        ],
        'bracketed': [
            (r'<', Punctuation.Bracket.Form.Begin, 'form'),
            (r'\(', Punctuation.Bracket.List.Begin, 'list'),
            (r'\{', Punctuation.Bracket.Template.Begin, 'template'),
            (r'\[', Punctuation.Bracket.Vector.Begin, 'vector'),
            (r'!\[', Punctuation.Bracket.Uvector.Begin, 'uvector'),
        ],
        'prefixed': [
            (r'\.', Punctuation.Prefix.Variable.Local),
            (r',', Punctuation.Prefix.Variable.Global),
            (r"!(?=[.,'<])", Punctuation.Prefix.Segment),
            (r';', Punctuation.Prefix.Comment),
            (r"'", Punctuation.Prefix.Quote),
            (r'%', Punctuation.Prefix.Macro),
            (r'%%', Punctuation.Prefix.Macro.Void),
        ],
    }
    _structures = [
        ('form',     r'<',    r'!?>'),
        ('list',     r'!?\(', r'!?\)'),
        ('template', r'!?\{', r'!?\}'),
        ('vector',   r'\[',   r'!?\]'),
        ('uvector',  r'!\[',  r'!?\]'),
    ]
    for name, bra, ket in _structures:
        nc = name.capitalize()
        bra_ttype = string_to_tokentype('Punctuation.Bracket.%s.Begin' % nc)
        ket_ttype = string_to_tokentype('Punctuation.Bracket.%s.End' % nc)
        tokens[name] = [
            (bra, bra_ttype, '#push'),
            (ket, ket_ttype, '#pop'),
            include('base-expr'),
            (r'.+(?=%s|\Z)' % ket, Error),
        ]

    def get_tokens_unprocessed(self, text):

        def strip_token(t):
            return t.parent if t[-1] in ('Begin', 'End') else t

        def rebase_token(token, base, dest):
            assert token[:len(base)] == base
            token = token[len(base):]
            for i in token:
                dest = getattr(dest, i)
            return dest

        def resolve_ttype(outer, inner):
            if inner is Whitespace.Unstyled:
                return inner, inner
            use = inner
            if ((outer in Prefix or outer in Prefixed) and
                inner not in Comment and
                inner not in Prefix.Comment and inner not in Prefix.Macro):
                    use = outer
            stripped = strip_token(use)
            if use in String:
                return stripped, stripped
            elif use in Bracket:
                return stripped, rebase_token(stripped, Bracket, Bracketed)
            elif use in Prefix:
                return use, rebase_token(use, Prefix, Prefixed)
            else:
                return use, use

        def ends_prefix(token):
            return (token not in Prefix and token not in Whitespace and
                    token not in Text and
                    not (token in Bracket and token[-1] == 'Begin'))

        ctx = [(Text, Text)]
        true_ttype = Text
        next_ttype = Text
        for index, token, value in (
                super(ZilLexer, self).get_tokens_unprocessed(text)):
            # print(repr((index, token, value)))
            if (token in Bracket or token in String) and (token[-1] == 'End'):
                next_ttype, true_ttype = ctx.pop() if ctx else (Error, Error)
                this_ttype, _ = resolve_ttype(next_ttype, token)
            elif token in Prefix or (
                (token in Bracket or token in String) and
                token[-1] == 'Begin'):
                    ctx.append((next_ttype, true_ttype))
                    true_ttype = strip_token(token)
                    this_ttype, next_ttype = resolve_ttype(next_ttype, token)
            else:
                this_ttype, _ = resolve_ttype(next_ttype, token)
            # print(repr((index, this_ttype, value)))
            assert this_ttype is not None
            yield index, this_ttype, value
            if ends_prefix(token):
                while true_ttype in Prefix:
                    next_ttype, true_ttype = ctx.pop() if ctx else (Error, Error)
