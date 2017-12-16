"""Directive for drawing Jenga diagrams with GraphViz.

Jenga diagrams visualize a data structure as a narrow stack of blocks,
possibly with arrows connecting to other blocks or stacks.
"""

import os
import re
from textwrap import dedent

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.statemachine import ViewList


SOLID = 'solid'
DASHED = 'dashed'
DOTTED = 'dotted'


class JengaBlock(object):
    # pylint: disable=C0103,C0111
    pattern = re.compile(r'$^')
    has_rownum = True

    border_style = SOLID
    top_border = None
    bottom_border = None

    def __init__(self, m):
        d = m.groupdict()
        if d:
            self.__dict__.update(d)
        else:
            self.content = m.group()

    @property
    def sides(self):
        result = charset('LR')
        if self.top_border:
            result.add('T')
        if self.bottom_border:
            result.add('B')
        return result

    @classmethod
    def try_match(cls, line):
        m = cls.pattern.match(line)
        return cls(m) if m else None

    def render(self, tb, rownum):
        raise NotImplementedError()

    def combine_with_next(self, _next_block):
        return None

    def combine_with_prev(self, _prev_block):
        return None


# pylint: disable=C0103,C0111
class charset(set):
    def __str__(self):
        return ''.join(self)


def _mktag(tag):                            # pylint: disable=E0213
    @staticmethod
    def wrapped_func(*children, **attrs):   # pylint: disable=C0111
        parts = ['<', tag]
        for k, v in attrs.iteritems():
            parts.extend([' ', k, '="', str(v), '"'])
        if tag.upper() in ('HR', 'VR') and not children:
            parts.append(' />')
        else:
            parts.append('>')
            parts.extend(str(c) for c in children)
            parts.extend(['</', tag, '>'])
        return ''.join(parts)
    return wrapped_func


class TableBuilder(object):
    # pylint: disable=R0903,C0111,C0103
    @staticmethod
    def wrap_content(text,
                     special_text_re=re.compile(
                         r'(?P<cap>[A-Z]+)|(?P<em>-*[a-z][-a-z]*)')):
        def do_sub(m):
            d = m.groupdict()
            s = m.group()
            if d['cap']:
                return TableBuilder.format_typename(s)
            if d['em']:
                return TableBuilder.format_param(s)
            return s
        return special_text_re.sub(do_sub, str(text).strip())

    @staticmethod
    def format_typename(text):
        return TableBuilder.FONT(text, face='Consolas Bold')

    @staticmethod
    def format_param(text):
        return TableBuilder.I(text)

    TABLE = _mktag('table')
    HR = _mktag('hr')
    TR = _mktag('tr')
    TD = _mktag('td')
    FONT = _mktag('font')
    I = _mktag('i')


class JFullRow(JengaBlock):
    pattern = re.compile(r'.*')

    def render(self, tb, rownum):
        return tb.TR(
            tb.TD(tb.wrap_content(self.content),
                  colspan=2, width=200, height=20 if self.content else 10,
                  sides=self.sides, port='r%d' % rownum),
        )


class JSplitRow(JengaBlock):
    pattern = re.compile(r'^\s*(?P<left>[^|]*?)\s*\|\s*(?P<right>[^|]*?)\s*$')
    left = None
    right = None

    def render(self, tb, rownum):
        return tb.TR(
            tb.TD(tb.wrap_content(self.left),
                  colspan=1, width=100, sides=self.sides, port='r%dleft' % rownum),
            tb.TD(tb.wrap_content(self.right),
                  colspan=1, width=100, sides=self.sides, port='r%dright' % rownum),
        )


class JDivider(JengaBlock):
    has_rownum = False
    top_border = True
    bottom_border = True

    pattern = re.compile(r'''(?x)
          (?P<solid>^\s*-+\s*$)
        | (?P<dashed>^\s*-(?:\s+-)+\s*$)
        | (?P<dotted>^\s*\.(?:(?:\s+\.)+|\.+)\s*$)
        ''')

    def __init__(self, m):
        super(JDivider, self).__init__(m)
        self.border_style = next(k for k, v in m.groupdict().iteritems() if v)

    def render(self, tb, rownum):
        if self.border_style == SOLID:
            return tb.HR()

        return tb.TR(
            tb.TD(colspan=2, sides='T', style=self.border_style, height=0,
                  cellpadding=0, cellspacing=0),
        )

    def combine_with_next(self, next_block):
        return self._combine(next_block, 'top_border')

    def combine_with_prev(self, prev_block):
        return self._combine(prev_block, 'bottom_border')

    def _combine(self, other, battr):
        if other.border_style in (self.border_style, None):
            other.border_style = self.border_style
            setattr(other, battr, True)
            return other
        return None


class JEllipsis(JengaBlock):
    has_rownum = False

    pattern = re.compile(r'^\s*/\s+/\s*$')

    def render(self, tb, rownum):
        return tb.TR(
            tb.TD(colspan=2, sides='LR', style=DOTTED, height=20),
        )


JENGA_BLOCKS = [
    JSplitRow,
    JDivider,
    JEllipsis,
    JFullRow,
]


class JengaDiagramDirective(Directive):
    has_content = True
    option_spec = {
        'dump': directives.flag,
    }

    def run(self):

        def parse_blocks():
            blocks = []
            for line in self.content:
                line = line.strip()
                if line.startswith('|') and line.endswith('|'):
                    line = line[1:-1]
                    line = line.strip()
                for btype in JENGA_BLOCKS:
                    b = btype.try_match(line)
                    if b:
                        blocks.append(b)
                        break
                else:
                    raise ValueError('unparsable line: "%s"' % line)
            return blocks

        def combine_blocks(a, b):
            return a.combine_with_next(b) or b.combine_with_prev(a) or None

        def fix_borders(blocks):
            i = len(blocks) - 1
            while i > 0:
                newb = combine_blocks(blocks[i - 1], blocks[i])
                if newb:
                    blocks[i - 1] = newb
                    del blocks[i]
                    if i < len(blocks):
                        # try combining the new blocks[i-1] and blocks[i]
                        continue
                i -= 1
            assert not isinstance(blocks[0], JDivider)
            assert not isinstance(blocks[-1], JDivider)

        def render_lines(blocks):
            tb = TableBuilder()
            lines = []
            # indent = ' ' * 6
            indent = ''
            rownum = 1
            for b in blocks:
                if b.has_rownum:
                    b_rownum = rownum
                    rownum += 1
                else:
                    b_rownum = None
                rendered = b.render(tb, b_rownum)
                lines.extend(indent + l.rstrip() for l in rendered.split('\n'))
            return lines

        def render_graph_directive(lines):
            template = dedent('''\
                .. digraph:: Jenga
                  :align: center

                  node [shape=plaintext];
                  block [label=<
                      <table border="0" cellborder="1" cellspacing="0" cellpadding="4">
                          {rows}
                      </table>
                  >];
                ''')
            outlines = []
            for tl in template.split('\n'):
                tl = tl.rstrip()
                if tl.endswith('{rows}'):
                    indent = tl[:-6]
                    outlines.extend(indent + ll for ll in lines)
                else:
                    outlines.append(tl)
            return outlines

        self.assert_has_content()
        blocks = parse_blocks()
        fix_borders(blocks)
        lines = render_lines(blocks)
        graph_lines = render_graph_directive(lines)

        element = nodes.Element(os.linesep.join(graph_lines))
        self.state.nested_parse(ViewList(graph_lines, source=''),
                                self.content_offset,
                                element)

        if 'dump' in self.options:
            dumplines = ['.. code-block:: rst', '']
            dumplines.extend('  ' + s for s in graph_lines)
            self.state.nested_parse(ViewList(dumplines, source=''),
                                    self.content_offset,
                                    element)

        return element.children
