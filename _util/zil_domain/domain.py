from __future__ import print_function

import re
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx import addnodes
from sphinx.util.console import red
from sphinx.locale import l_, _
from sphinx.roles import XRefRole
from sphinx.domains import Domain, ObjType
from sphinx.directives import ObjectDescription
from sphinx.util.nodes import make_refnode
from sphinx.util.docfields import Field, GroupedField, TypedField

class ZilCurrentPackage(Directive):
    """This directive is just to tell Sphinx that we're documenting stuff
    in some package or pseudo-package.
    """

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}

    def run(self):
        env = self.state.document.settings.env
        env.temp_data['zil:package'] = self.arguments[0].upper()
        return []

param_re_pat = r'''
    (?=[^\s\]\>]*?[a-z])   # must contain lowercase letter
    (?P<name>[^\s\]\>:]+)
    (?: :               # optional colon+type suffix
        (?P<type>[^\s\]\>]+)
    )?'''
optional_param_re = re.compile(r'(?x)\[%s\]' % param_re_pat)
required_param_re = re.compile(r'(?x)%s' % param_re_pat)
literal_param_re = re.compile(r'''(?x)
    (   (?P<string>"(?:\\\"|[^"])")
    |   (?P<open>[\[\(\<])
    |   (?P<close>[\]\)\>])
    |   (?P<other>[^\]\)\>\s]+)
    )''')
sig_parse_res = (
    ('optional', optional_param_re),
    ('required', required_param_re),
    ('literal', literal_param_re),
)


class ParsedSignature(object):
    # TODO: handle DEFINE-style signatures too?
    def __init__(self, sig):
        self.parts = []
        self.name = None
        osig = sig
        sig = sig.strip('<> \t')
        while sig:
            for name, rex in sig_parse_res:
                m = rex.match(sig)
                if not m:
                    continue
                self.parts.append((name, m.group(0), m.groupdict()))
                if not self.name:
                    self.name = m.group(0)
                break
            else:
                # no matches
                raise ValueError('Unable to parse signature: "%s"' % osig)
            sig = sig[m.end():].lstrip()

    def to_nodes(self):
        def unparse_arg(attrs):
            s = attrs['name']
            typ = attrs.get('type')
            if typ:
                s += ':' + typ
            return s

        yield nodes.inline('', '<')

        for i, (name, text, attrs) in enumerate(self.parts):
            if i > 0:
                yield nodes.inline('', ' ')
            if name == 'optional':
                yield nodes.emphasis('', '[' + unparse_arg(attrs) + ']')
            elif name == 'required':
                yield nodes.emphasis('', unparse_arg(attrs))
            elif name == 'literal':
                yield nodes.inline('', text)
            else:
                assert False, 'Unexpected part: %r (%r)' % (name, text)

        yield nodes.inline('', '>')


class ZilFormObj(ObjectDescription):
    """A ZIL object defined with a FORM.
    """

    doc_field_types = [
        TypedField('arguments', label=l_('Arguments'),
                   names=('argument', 'arg', 'parameter', 'param'),
                   typerolename='type', typenames=('paramtype', 'type')),
        Field('returnvalue', label=l_('Returns'), has_arg=False,
              names=('returns', 'return')),
        Field('returntype', label=l_('Return type'), has_arg=False,
              names=('rtype',)),
    ]

    option_spec = {
        'nodoc': directives.flag,
        'noindex': directives.flag,
    }

    def handle_signature(self, sig, signode):
        symbol_name = []
        package = self.env.temp_data.get('zil:package')

        parsed_sig = ParsedSignature(sig)
        opts = dict(self.options)
        opts['language'] = 'none'
        # modify rawsource so we don't try to highlight
        literal = nodes.literal_block('*' + sig, '', *parsed_sig.to_nodes(),
                                      **opts)
        signode.append(literal)

        symbol_name = parsed_sig.name
        if not symbol_name:
            raise Exception("Unknown symbol type for signature %s" % sig)
        # record_use(package, symbol_name, self.objtype)
        objtype = self.objtype
        return objtype.strip(), symbol_name

    def add_target_and_index(self, name, sig, signode):
        # type: (unicode, unicode, addnodes.desc_signature) -> None
        key = name
        typ, name = key
        targetname = '-'.join(key)
        if targetname not in self.state.document.ids:
            signode['names'].append(targetname)
            signode['ids'].append(targetname)
            signode['first'] = (not self.names)
            self.state.document.note_explicit_target(signode)

            objects = self.env.domaindata['zil']['objects']
            key = (self.objtype, name)
            if key in objects:
                self.state_machine.reporter.warning(
                    'duplicate description of %s %s, ' % (self.objtype, name) +
                    'other instance in ' + self.env.doc2path(objects[key][0]),
                    line=self.lineno)
            objects[key] = self.env.docname, targetname
        indextext = self.get_index_text(typ, name)
        if indextext:
            self.indexnode['entries'].append(('single', indextext,
                                              targetname, '', None))

    def get_index_text(self, objectname, name):
        # type: (unicode, unicode) -> unicode
        return name


class ZilXRefRole(XRefRole):
    def process_link(self, env, refnode, has_explicit_title, title, target):
        if not has_explicit_title:
            target = target.lstrip('~')  # only has a meaning for the title
            # if the first character is a tilde, don't display the package
            if title[0:1] == '~':
                atom_path = title[1:].split('!-', 1)
                title = atom_path[0]
        return title, target


class ZilDomain(Domain):
    "ZIL language domain"
    name = 'zil'
    label = 'ZIL/MDL'

    object_types = {
        'package': ObjType(l_('package'), 'pkg'),
        'function': ObjType(l_('function'), 'func'),
        # 'routine': ObjType(l_('routine'), 'routine'),
        # 'macro': ObjType(l_('macro'), 'macro'),
        # 'variable': ObjType(l_('variable'), 'variable'),
        # 'constant': ObjType(l_('constant'), 'constant'),
        # 'table': ObjType(l_('table'), 'table'),
        # 'type': ObjType(l_('type'), 'type'),
        # 'property': ObjType(l_('property'), 'property'),
        # 'flag': ObjType(l_('flag'), 'flag'),
        # 'object': ObjType(l_('object'), 'object'),
        # 'library-section': ObjType(l_('library-section'), 'library-section'),
        # 'compilation-flag': ObjType(l_('compilation-flag'), 'compilation-flag'),
    }

    directives = {
        'package': ZilCurrentPackage,
        'function': ZilFormObj,
    }

    roles = {
        'func': ZilXRefRole(),
    }

    initial_data = {
        'objects': {},
    }

    def resolve_xref(self, env, fromdocname, builder,
                     typ, target, node, contnode):
        objtypes = self.objtypes_for_role(typ) or []
        for objtype in objtypes:
            if (objtype, target) in self.data['objects']:
                docname, labelid = self.data['objects'][objtype, target]
                break
        else:
            docname, labelid = '', ''
        if not docname:
            return None
        return make_refnode(builder, fromdocname, docname,
                            labelid, contnode)

    def get_objects(self):
        for (type, name), info in self.data['objects'].iteritems():
            yield (name, name, type, info[0], info[1],
                   self.object_types[type].attrs['searchprio'])

    def clear_doc(self, docname):
        # type: (unicode) -> None
        for key, (doc, _) in list(self.data['objects'].items()):
            if doc == docname:
                del self.data['objects'][key]

    def merge_domaindata(self, docnames, otherdata):
        # type: (List[unicode], Dict) -> None
        # XXX check duplicates
        for key, (doc, _) in otherdata['objects'].items():
            if doc in docnames:
                self.data['objects'][key] = doc
