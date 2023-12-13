from croft.lib.orm.query import op


def nodal( leaf, node ):

    return getattr( leaf, node.__tablename__ + '_dbid' )

def tandem( node, leaf ):

    parx, pary = node
    return [
        ( op.SELECT_FROM, ( leaf, ) ),
        ( op.JOIN, ( parx, nodal( leaf, parx ) == parx.dbid ) ),
        ( op.JOIN, ( pary, nodal( leaf, pary ) == pary.dbid ) ),
    ]

def implicit( node, leaf, nkey ):

    parx, pary = node
    tand = tandem( node, leaf )
    tand.append(
        ( op.FILTER, ( pary.aliasBind() == nkey, ) )
    )
    return tand

def explicit( node, leaf, dbid ):

    parx, pary = node
    x, y = dbid
    return [
        ( op.FILTER, ( nodal( leaf, parx ) == x, nodal( leaf, pary ) == y ) ),
    ]

