from bakery.lib.orm.query import op
from bakery.lib.orm.query.base import exactKey


def tandem( node, leaf, join = op.JOIN ):

    return [
        ( op.SELECT_FROM, ( node, ) ),
        ( join, ( leaf, getattr( leaf, node.__tablename__ + '_dbid' ) == node.dbid ) )
    ]

def implicit( node, leaf, nkey ):

    return tandem( node, leaf ) + exactKey( node, nkey )
    

