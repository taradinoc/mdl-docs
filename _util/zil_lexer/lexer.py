from __future__ import absolute_import

from collections import namedtuple
import re

from pygments.lexer import RegexLexer, include, bygroups, words, default, \
    using, this
from .tokens import *

# from . import builtins as zb

# helper structures
class TopLevelExpr(object):
    name = 'expr'

    def overrides_color(self, outer_expr):
        return False

    def has_inner_color(self):
        return False

    def name_inner(self, inner_state):
        return inner_state

    def color_ttype(self, ttype):
        return ttype


class ExprBase(object):
    def __init__(self, name, ttype, override):
        self.name = name
        self.ttype = ttype
        self.override = override

    def overrides_color(self, outer_expr):
        return self.override or not outer_expr.has_inner_color()

    def has_inner_color(self):
        return False

    def name_inner(self, inner_state):
        raise NotImplementedError

    def color_ttype(self, ttype):
        return self.ttype


class PrefixedExpr(ExprBase):
    def __init__(self, prefix, name, ttype, override=False):
        super(PrefixedExpr, self).__init__(name, ttype, override)
        self.prefix = prefix

    def has_inner_color(self):
        return True

    def name_inner(self, inner_state):
        return '%s-prefixed-%s' % (self.name, inner_state)


class BracketedExpr(ExprBase):
    def __init__(self, prefix, suffix, name, ttype, inner=False, override=False):
        super(BracketedExpr, self).__init__(name, ttype, override)
        self.prefix = prefix
        self.suffix = suffix
        self.inner = inner

    def has_inner_color(self):
        return self.inner

    def name_inner(self, inner_state):
        return '%s-bracketed-%s' % (self.name, inner_state)


TOP_LEVEL_EXPR = TopLevelExpr()

EXPR_TYPES = [
    TOP_LEVEL_EXPR,

    PrefixedExpr(r';', 'comment', Comment, override=True),
    PrefixedExpr(r',', 'gval', Name.Variable.Global),
    PrefixedExpr(r'!,', 'gval-segment', Punctuation.Segment),
    PrefixedExpr(r'\.', 'lval', Name.Variable),
    PrefixedExpr(r'!\.', 'lval-segment', Punctuation.Segment),
    PrefixedExpr(r"'", 'quote', Quoted),
    PrefixedExpr(r'%%?', 'macro', Punctuation.Macro, override=True),

    BracketedExpr(r'\(', r'\)', 'list', Punctuation.List),
    BracketedExpr(r'\[', r'\]', 'vector', Punctuation.Vector),
    BracketedExpr(r'!\[', r'!?\]', 'uvector', Punctuation.Vector),
    BracketedExpr(r'<', r'>', 'form', Punctuation.Form),
    BracketedExpr(r'!<', r'!?>', 'segment', Punctuation.Segment),
    BracketedExpr(r'\{', r'\}', 'template', Template, inner=True, override=True),
]

delimiters = r' \t-\r,#\':;%()\[\]<>\{\}"'
non_atom_char = r'[%s]' % delimiters
atom_head = r'(?:\\.|[^!\.%s])' % delimiters
atom_tail = r'(?:\\.|[^%s])' % delimiters
valid_atom = r'%s%s*' % (atom_head, atom_tail)
opening_bracket = r'!?[\[\{\(\<]'
closing_bracket = r'!?[\]\}\)\>]'


def reprable_call(name):
    class _cls(object):
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

        def __repr__(self):
            args = list(map(repr, self.args)) + [
                '%s=%r' % (k, v)
                for k, v in self.kwargs.iteritems()
            ]
            parts = [
                name,
                '(',
                ', '.join(args),
                ')',
            ]
            return ''.join(parts)
    return _cls


def reprable_val(name):
    class _cls(object):
        def __repr__(self):
            return name
    return _cls()


class raw_str(str):
    def __repr__(self):
        if "'" not in self:
            return "r'" + str(self) + "'"
        elif '"' not in self:
            return 'r"' + str(self) + '"'
        else:
            return repr(str(self))

def dump_tokens():
    from pprint import pprint
    from inspect import getcallargs
    kwargs = {k: reprable_call(k) if callable(v) else reprable_val(k)
              for k, v in getcallargs(make_tokens).iteritems()}
    kwargs['this'] = reprable_val('this')
    kwargs['_s'] = raw_str
    with open('/tmp/tokens.py', 'wt') as f:
        pprint(make_tokens(**kwargs), stream=f)


class ColorOnlyWrapper(object):
    @staticmethod
    def wrap(_stype, ttype):
        return ttype

    enter = wrap
    exit = wrap


class SemanticOnlyWrapper(object):
    @staticmethod
    def wrap(stype, _ttype):
        def callback(lexer, match):
            yield match.start(), _s_start(stype), ''
            yield match.end(), _s_end(stype), ''
        return callback

    @staticmethod
    def start(stype, _ttype):
        def callback(lexer, match):
            yield match.start(), _s_start(stype), match.group()
        return callback

    @staticmethod
    def end(stype, _ttype):
        def callback(lexer, match):
            yield match.start(), _s_end(stype), match.group()
        return callback


def make_tokens(using=using, bygroups=bygroups, default=default, this=this,
                _s=str):    #XXX , meta=ColorOnlyWrapper()):

    todo = {}

    def nest_state(outer_expr, inner_expr):
        if outer_expr == inner_expr:
            return inner_expr.name
        name = outer_expr.name_inner(inner_expr.name)
        todo[name] = outer_expr, inner_expr
        return name

    def get_colorizer(outer_expr, inner_expr):
        return inner_expr if inner_expr.overrides_color(outer_expr) else outer_expr

    def gen_expr_state(outer_expr, inner_expr):
        colorizer = get_colorizer(outer_expr, inner_expr)
        color = colorizer.color_ttype

        # whitespace
        yield _s(r'\s+'), Text

        if isinstance(inner_expr, BracketedExpr):
            # nested brackets
            bracket_ttype = color(inner_expr.ttype)
            yield _s(inner_expr.prefix), bracket_ttype, '#push'
            yield _s(inner_expr.suffix), bracket_ttype, '#pop'
            # mismatched closing bracket
            yield _s(r'(?=%s)' % closing_bracket), Error, '#pop'
            # other
            yield default(nest_state(outer_expr, TOP_LEVEL_EXPR))
            return

        # atom or number
        yield _s(valid_atom), using(this, state=colorizer.name_inner('atomlike')), '#pop'

        # hash prefix
        yield _s(r'#\s*0*2\s+[01]+(?=%s|\Z)' % non_atom_char), color(Number.Bin), '#pop'
        yield _s(r'(#\s*%s)\s+' % valid_atom), color(Name.Class)

        # strings, symbols and characters
        yield _s(r'"'), color(String.Double), ('#pop', colorizer.name_inner('string'))
        yield _s(r'(![\\"])(\s)'), bygroups(color(String.Char), Whitespace), '#pop'
        yield _s(r'![\\"].'), color(String.Char), '#pop'

        # FALSE
        yield _s(r'<\s*>'), color(Keyword.Constant), '#pop'

        # prefixed/bracketed expressions
        for e in EXPR_TYPES:
            if not isinstance(e, TopLevelExpr):
                inner_colorizer = get_colorizer(colorizer, e)
                yield _s(e.prefix), inner_colorizer.color_ttype(e.ttype), ('#pop', nest_state(inner_colorizer, e))

        if isinstance(outer_expr, BracketedExpr):
            # expected closing bracket
            yield _s(outer_expr.suffix), color(outer_expr.ttype), '#pop'

        # mismatched closing bracket
        yield _s(closing_bracket), Error, '#pop'
        # unrecognized bangs
        yield _s(r'!.?'), Error

    def make_extra_states(expr):

        def gen_atomlike_state():
            # numbers
            # yield r'-?\d+\.(\d+)([eE][-+]?\d+)', expr.color_ttype(Number.Float)
            yield _s(r'-?\d+\.?\Z'), expr.color_ttype(Number.Integer), '#pop'
            yield _s(r'\*[0-7]+\*\Z'), expr.color_ttype(Number.Oct), '#pop'

            # atoms
            yield _s(r'.*'), expr.color_ttype(Atom), '#pop'

        def gen_string_state():
            yield _s(r'\\.'), expr.color_ttype(String.Escape)
            yield _s(r'"'), expr.color_ttype(String.Double), '#pop'
            yield _s(r'[^\\"]+'), expr.color_ttype(String.Double)

        return {
            expr.name_inner('atomlike'): list(gen_atomlike_state()),
            expr.name_inner('string'): list(gen_string_state()),
        }

    # make_tokens!
    result = {'root': [
        # unmatched closing bracket
        (_s(closing_bracket), Error),

        default('expr'),
    ]}

    for e in EXPR_TYPES:
        todo[e.name] = (TOP_LEVEL_EXPR, e)
        result.update(make_extra_states(e))

    while todo:
        k, v = todo.popitem()
        if k not in result:
            result[k] = list(gen_expr_state(*v))

    return result

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

    # TODO: delet dis
    tokens = ({
        'root': [
            include('expr'),
        ],

        'bad-closing-bracket': [
            (closing_bracket, Error, '#pop'),
        ],

        'bad-bang': [
            (r'!.?', Error),
        ],

        'expr': [
            # whitespaces - usually not relevant
            (r'\s+', Text),

            # atom or number
            (valid_atom, using(this, state='atomlike')),

            # strings, symbols and characters
            (r'"', String.Double, 'string'),
            (r'(![\\"])(\s)', bygroups(String.Char, Whitespace)),
            (r'![\\"]', String.Char),

            # prefixed expressions
            # prefixed_expr(r';', 'comment', Comment, override=True),
            (r';', Comment, 'comment-prefixed-expr'),
            # prefixed_expr(r',', 'gval', Name.Variable.Global),
            # prefixed_expr(r'\.', 'lval', Name.Variable),
            # prefixed_expr(r'!\.', 'lval-segment', Punctuation.Segment),
            # prefixed_expr(r"'", 'quote', Literal.Quoted),
            # prefixed_expr(r'%%?', 'macro', Comment, override=True),

            # bracketed expressions
            # bracketed_expr(r'\(', r'\)', 'list', Punctuation.Bracket.List),
            (r'\(', Bracket.Round, 'list-bracketed-expr'),
            # bracketed_expr(r'\[', r'\]', 'vector', Punctuation.Vector),
            # bracketed_expr(r'!\[', r'!?\]', 'uvector', Punctuation.Vector.Uniform),
            # bracketed_expr(r'<', r'>', 'form', Punctuation.Form),
            # bracketed_expr(r'!<', r'!\?>', 'segment', Punctuation.Segment),
            # bracketed_expr(r'\{', r'\}', 'template', Comment, inner=True, override=True),

            # unrecognized bangs
            include('bad-bang'),
        ],
        'atomlike': [
            # numbers
            #(r'-?\d+\.(\d+)([eE][-+]?\d+)', Number.Float),
            (r'-?\d+\.?\Z', Number.Integer, '#pop'),
            (r'\*[0-7]+\*\Z', Number.Oct, '#pop'),
            (r'#\s*2\s+[01]+\Z', Number.Bin, '#pop'),

            # atoms
            # TODO: check against builtin lists
            (r'.*', Name.Atom, '#pop'),
        ],
        'string': [
            (r'\\.', String.Escape),
            (r'"', String.Double, '#pop'),
            (r'[^\\"]+', String.Double),
        ],

        'comment-prefixed-expr': [
            # the comments
            # commented form (entire expr folliwng)
            #TODO: (r';\s*\(', Comment, 'commented-list'),

            # whitespaces - usually not relevant
            (r'\s+', Text),

            # atom or number
            (valid_atom, using(this, state='comment-prefixed-atomlike'), '#pop'),

            # strings, symbols and characters
            (r'"(\\\\|\\"|[^"])*"', Comment, '#pop'),
            (r'![\\"]', Comment, '#pop'),

            # prefixed expressions
            # prefixed_expr(',', 'gval', Name.Variable.Global),
            (r';', Comment, 'comment-prefixed-expr'),
            # prefixed_expr(';', 'comment', Comment, override=True),
            # prefixed_expr('.', 'lval', Name.Variable),
            # prefixed_expr("'", 'quote', Literal.Quoted),
            # prefixed_expr('%%?', 'macro', Comment, override=True),

            # bracketed expressions
            # bracketed_expr('(', ')', 'list', Punctuation.List),
            (r'\(', Comment, 'comment-prefixed-list'),
            # bracketed_expr('[', ']', 'vector', Punctuation.Vector),
            # bracketed_expr('![', '!?]', 'uvector', Punctuation.Vector),
            # bracketed_expr('<', '>', 'form', Punctuation.Form),
            # bracketed_expr('!<', '!?>', 'segment', Punctuation.Segment),
            # bracketed_expr('{', '}', 'template', Comment, inner=True, override=True),
        ],
        'comment-prefixed-atomlike': [
            # numbers
            #(r'-?\d+\.(\d+)([eE][-+]?\d+)', Number.Float),
            (r'-?\d+\.?\Z', Comment, '#pop'),
            (r'\*[0-7]+\*\Z', Comment, '#pop'),
            # (r'#\s*2\s+[01]+\Z', Comment, '#pop'),

            # atoms
            # TODO: check against builtin lists
            (r'.*', Comment, '#pop'),
        ],

        'list-bracketed-expr': [
            (r'\(', Bracket.Round, '#push'),
            (r'\)', Bracket.Round, '#pop'),
            include('bad-closing-bracket'),
            default('expr'),
        ],
        'comment-prefixed-list': [
            (r'\(', Comment, '#push'),
            (r'\)', Comment, '#pop'),
            include('bad-closing-bracket'),
            default('comment-prefixed-expr'),
        ],
    })

    #XXX EXPERIMENTAL
    dump_tokens()
    tokens = make_tokens()

    # with open('tokens.generated.py', 'wt') as f:
    #     pprint(tokens, stream=f)
