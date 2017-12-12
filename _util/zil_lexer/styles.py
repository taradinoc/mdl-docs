from pygments.style import Style
from sphinx.pygments_styles import SphinxStyle

from .tokens import (
    Punctuation, Name, Keyword, String, Comment, Number, Text,
    Prefix, Bracket, Prefixed, Bracketed,
)

class ZilDocStyle(Style):
    styles = dict(SphinxStyle.styles)
    styles.update({
        # Generic.Output: '#333',
        # Comment: 'italic #408090',
        Prefix.Comment: 'italic #408090',
        Prefixed.Comment: 'italic #408090',

        Number: '#208050',
        String.Char: '#208050',

        Prefix.Hash: 'underline italic #208050',
        Prefixed.Hash: 'underline italic #208050',

        Prefix.Variable.Global: 'bold #FA8072',
        Prefixed.Variable.Global: '#FA8072',
        Prefix.Variable.Local: 'bold #9ACD32',
        Prefixed.Variable.Local: '#9ACD32',

        Prefix.Segment: '#EE82EE',
        Prefixed.Segment: '#EE82EE',
        Prefix.Macro: '#FF4500',
        Prefixed.Macro: '#FF4500',
        Prefix.Quote: 'bold italic #4070A0',
        Prefixed.Quote: 'italic #4070A0',

        Bracket.List: 'bold #B8860B',
        Bracket.Form: 'bold #8B008B',
    })
