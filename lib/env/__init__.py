from croft.lib.motif.fixture import Fixture

class Base( Fixture ): pass

Base.fix( lambda x: x , (
    ('DEV', 'DEV'),
))


from croft.lib.env.domain import Domain

