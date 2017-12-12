from pygments.token import Token, Text, Comment, Operator, Keyword, Name, \
    String, Number, Punctuation, Literal, Error, Whitespace, \
    string_to_tokentype, STANDARD_TYPES

# new token types
Bracket = Punctuation.Bracket
Bracketed = Text.Bracketed

Prefix = Punctuation.Prefix
Prefixed = Text.Prefixed

# Quoted = String.Symbol #Literal.Quoted
# Template = Comment.Preproc.Template
# Atom = Name  #Name.Atom    # XXX to be replaced by filter

# semantic
# Prefixed = Token.Zil.Prefixed
# Bracketed = Token.Zil.Bracketed

STANDARD_TYPES.update({
    Bracket.Form: 'zf',
    Bracket.List: 'zl',
    Bracket.Vector: 'za',
    Bracket.Uvector: 'zu',
    Bracket.Template: 'zt',

    Prefix.Variable.Local: 'zv',
    Prefix.Variable.Global: 'zg',
    Prefix.Segment: 'zs',
    Prefix.Comment: 'zc',
    Prefix.Quote: 'zq',
    Prefix.Macro: 'zm',
    Prefix.Hash: 'zh',
})
