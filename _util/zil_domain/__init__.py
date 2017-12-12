from .domain import ZilDomain, ZilXRefRole

__all__ = ['ZilDomain', 'ZilXRefRole']


def setup(app):
    app.add_domain(ZilDomain)
