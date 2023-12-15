from sqlalchemy.orm import Load, joinedload
from bakery.lib.orm.query import op

def exactKey( mapclass, key ):

    return [ ( op.FILTER, ( mapclass.aliasBind() == key, ) ) ]

def explicit( mapclass, dbid ):

    return [ ( op.FILTER, ( mapclass.dbid == dbid, ) ) ]

def interval( mapclass, begin, end ):

    return [ ( op.FILTER, ( mapclass.ordinal >= begin, mapclass.ordinal < end ) ) ]

def matching( conds ):

    return [ ( op.FILTER, tuple( conds ) ) ]

def ordering( item, rule = 'asc' ):

    return [ ( op.ORDER_BY, ( getattr( item, rule )(), ) ) ]

def loadonly( mapclass, columns ):

    return [ ( op.OPTIONS, ( Load( mapclass ).load_only( *columns ), ) ) ]

def loadwith( item, only = tuple() ):

    load = joinedload( item )
    if len( only ):
        load.load_only( *only )
    return [ ( op.OPTIONS, ( load, ) ) ]

def pivot( mapclass ):

    return [ ( op.SELECT_FROM, ( mapclass, ) ) ]

def innerjoin( mapclass, binding ):

    return [ ( op.JOIN, ( mapclass, binding ) ) ]

def outerjoin( mapclass, binding ):

    return [ ( op.OUTERJOIN, ( mapclass, binding ) ) ]
