import re
from docutils.parsers.rst import directives
from sphinx import addnodes
from sphinx.util.console import red
from sphinx.locale import l_, _
from sphinx.roles import XRefRole
from sphinx.domains import Domain, ObjType
from sphinx.directives import ObjectDescription
from sphinx.util.nodes import make_refnode
from sphinx.util.compat import Directive
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
        # objtype = self.get_signature_prefix(sig)
        sig_split = sig.split(" ")
        # sig = sig_split[0]
        # signode.append(addnodes.desc_annotation(objtype, objtype))
        # lisp_args = ARGS[package].get(sig.upper(), "")
        # function_name = addnodes.desc_name(sig, sig)
        function_name = addnodes.desc_name(sig_split[0][1:])

        # if not lisp_args.strip() and self.objtype in ["function"]:
        #     lisp_args = "()"
        # if lisp_args.strip():
        #     types = []
        #     if self.objtype in ["method"]:
        #         types = self.arguments[0].split(' ')[1:]
        #     sexp = SEXP(lisp_args,
        #                 types=types,
        #                 show_defaults=self.env.app.config.cl_show_defaults)
        #     arg_list = sexp.as_parameterlist(function_name)
        #     signode.append(arg_list)
        # else:
        #     signode.append(function_name)

        signode.append(function_name)

        # # Add Slots
        # slots = SLOTS[package].get(sig.upper())
        # if slots and "noinitargs" not in self.options:
        #     # TODO add slot details if describing a class
        #     for slot in slots:
        #         initarg = slot.get(u'initarg')
        #         if initarg and initarg.lower() != 'nil':
        #             slotarg = addnodes.literal_emphasis(slot.get(u'name'), slot.get(u'name'))
        #             slotsig = initarg.lower() + u' '
        #             signode.append(addnodes.desc_optional(slotsig, slotsig, slotarg))

        symbol_name = sig
        if not symbol_name:
            raise Exception("Unknown symbol type for signature %s" % sig)
        # record_use(package, symbol_name, self.objtype)
        objtype = self.objtype
        return objtype.strip(), symbol_name


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
