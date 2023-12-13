from sqlalchemy.orm import joinedload
from croft.lib.orm.query import util

def count( session, mapclass ):

    return session.query( mapclass.dbid ).count()

def keymap( session, mapclass, custom = tuple() ):

    query = util.customise( session.query( mapclass.aliasBind(), mapclass.dbid ), custom )
    return dict( t for t in query.all() )

def keys( session, mapclass, custom = tuple() ):

    query = util.customise( session.query( mapclass.aliasBind() ), custom )
    return tuple( t[ 0 ] for t in query.all() )

def pull( session, select, build, custom = tuple(), postfilter = None ):
    
    query = util.customise( session.query( *select ), custom )
    return util.process( query.all(), build, postfilter )

def push( session, generator, items, part = 1 << 10 ):

    n = 1
    for item in items:
        session.add( generator( *item ) )
        if n % part == 0:
            session.flush()
        n += 1
    session.flush()

def bulkpush( session, generator, items, part = 1 << 10 ):

    pool = list()
    n = 1
    for item in items:
        pool.append( generator( *item ) )
        if n % part == 0:
            session.bulk_save_objects( pool )
            session.flush()
            pool[ : ] = list()
        n += 1
    session.bulk_save_objects( pool )
    session.flush()

def replace( session, mapclass, argmap, custom, legend ):

    query = util.customise( session.query( mapclass ), custom )
    r = dict( ( f.emblem(), f ) for f in query.all() )
    for key, args in argmap.items():
        f = r.get( key )
        if f:
            for n, a in zip( legend, args ):
                setattr( f, n, a )
    session.flush()

def update( session, mapclass, argmap, custom, asof ):

    mapprog, maparch = mapclass 
    query = util.customise( session.query( mapprog ), custom )
    r = dict( ( f.emblem(), f ) for f in query.all() )
    for key, args in argmap.items():
        f = r.get( key )
        if f:
            save = f.archiveCopy( maparch, asof )
            f.update( *args )
            f.archive.append( save )
    session.flush()

def version( session, mapclass, custom ):

    query = util.customise( session.query( mapclass ), custom ).options( joinedload( 'archive' ).load_only( 'asof' ) )
    return tuple( t.asof for t in query.one().archive )

def asof( session, mapclass, build, custom, at, postfilter = None ):

    query = util.customise( session.query( mapclass ), custom ).options( joinedload( 'archive' ) )
    gen = lambda x: build( x, util.recent( x, at ) )
    return util.process( query.all(), gen, postfilter )

def deleteByKey( session, tablename, dbid ):

    session.execute( 'DELETE FROM {} WHERE dbid =:param'.format( tablename ), { 'param': dbid } )
    session.flush()

def delete( session, mapclass, custom, noload = True ):

    query = util.customise( session.query( mapclass ), custom )
    if noload:
        query.delete()
    else:
        for f in query.all():
            session.delete( f )
    session.flush()


