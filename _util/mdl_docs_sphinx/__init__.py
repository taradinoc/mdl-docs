from docutils import nodes
from docutils import utils
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from docutils.parsers.rst import states
from docutils.parsers.rst.roles import set_classes
from sphinx.util.docutils import sphinx_domains
from zil_domain import ZilXRefRole


def macro_role(role, rawtext, text, lineno, inliner,
               options={}, content=[]):
    set_classes(options)
    node = nodes.inline(rawtext, ''.join(content) % utils.unescape(text),
                        **options)
    return [node], []

macro_role.content = True


TREF_TO_XREF = {
    'SUBR': 'func',
    'FSUBR': 'func',
    'TYPE': 't',
    'PRIMTYPE': 't',
    # 'ATOM': ...
}

def tref_role(role, rawtext, text, lineno, inliner,
              options={}, content=[]):
    parts = text.split(' ', 1)
    typename = parts[0]

    # set_classes(options)
    # if 'classes' not in options:
    #     options['classes'] = ['typename']

    def wrap_in_role(rolename, text):
        with sphinx_domains(inliner.document.settings.env):
            from docutils.parsers.rst.roles import role
            role_fn, _ = role(rolename,
                              inliner.language,
                              lineno,
                              inliner.reporter)
        assert role_fn is not None, 'No such role "%s"' % rolename
        vec, _ = role_fn(rolename,
                         rawtext=rawtext,
                         text=text,
                         lineno=lineno,
                         inliner=inliner,
                         options=options,
                         content=content)
        return vec

    result = wrap_in_role('t', typename)

    if len(parts) > 1:
        result.append(nodes.inline(rawtext, ' '))
        try:
            result.extend(wrap_in_role(TREF_TO_XREF[typename], parts[1]))
        except KeyError:
            msg = inliner.reporter.error(
                'Invalid type name for "%s" role: "%s".' % (role, typename),
                line=lineno)
            prb = inliner.problematic(rawtext, rawtext, msg)
            return [prb], [msg]

    return result, []


class SectionNumfigFormat:
    # sneaky!
    def __contains__(self, arg):
        # this is called to test our formatting capabilities
        return arg in ('{name}', 'number')

    def format(self, number, name=None):
        dots = number.count('.')
        kind = 'section' if dots else 'chapter'
        # fmt = u'{kind} {number} ({name})' if name else u'{kind} {number}'
        fmt = u'{kind} {number}'
        return fmt.format(kind=kind, number=number, name=name)


class ReplaceClassDirective(Directive):

    required_arguments = 1
    final_argument_whitespace = True
    has_content = True

    def run(self):
        if not isinstance(self.state, states.SubstitutionDef):
            raise self.error(
                'Invalid context: the "%s" directive can only be used within '
                'a substitution definition.' % self.name)
        try:
             class_value = directives.class_option(self.arguments[0])
        except ValueError:
            raise self.error(
                'Invalid class attribute value for "%s" directive: "%s".'
                % (self.name, self.arguments[0]))
        self.assert_has_content()
        text = '\n'.join(self.content)
        element = nodes.Element(text)
        self.state.nested_parse(self.content, self.content_offset,
                                element)
        # element might contain [paragraph] + system_message(s)
        node = None
        messages = []
        for elem in element:
            if not node and isinstance(elem, nodes.paragraph):
                node = elem
            elif isinstance(elem, nodes.system_message):
                elem['backrefs'] = []
                messages.append(elem)
            else:
                return [
                    self.state_machine.reporter.error(
                        'Error in "%s" directive: may contain a single paragraph '
                        'only.' % (self.name), line=self.lineno) ]
        if node:
            newnode = nodes.inline('', '', *node.children, classes=class_value)
            return messages + [newnode]
        return messages


def setup(app):
    app.add_role('macro', macro_role)
    app.add_role('tref', tref_role)
    # app.add_directive('macro', MacroDirective)
    app.add_directive('replace-class', ReplaceClassDirective)
