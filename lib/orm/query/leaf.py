from croft.lib.orm.query import op
from croft.lib.orm.query.base import exactKey


def nested( tree ):

    revs = reversed( tree )
    todo = list()
    prev = next( revs )
    todo.append( ( op.SELECT_FROM, ( prev, ) ) )
    for node in revs:
        todo.append( ( op.JOIN, ( node, getattr( prev, node.__tablename__ + '_dbid' ) == node.dbid ) ) )
        prev = node
    return todo

def tandem( node, leaf ):

    return nested( ( node, leaf ) )
    
def implicit( tree, nkey ):

    return nested( tree ) + exactKey( tree[ 0 ], nkey )
    
def explicit( tree, dbid ):

    node, leaf = tree
    return [
        ( op.FILTER, ( getattr( leaf, node.__tablename__ + '_dbid' ) == dbid, ) ),
    ]
