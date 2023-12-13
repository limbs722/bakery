def first( x ):

    return x[ 0 ]

def last( x ):

    return x[ -1 ]

def full( x ):

    return x

def recent( f, at ):

    candidate = f
    for a in f.archive:
        if a.asof < at:
            break
        else:
            candidate = a
    return candidate

def customise( query, custom ):

    for opn, arg in custom:
        query = getattr( query, opn )( *arg )
    return query

def process( found, action, postfilter ):

    if postfilter is None:
        return list( map( action, found ) )
    else:
        return [ action( f ) for f in found if postfilter( f ) ]

class HookPair( object ):

    def __init__( self, node, leaf ):

        self.nxat, self.nyat = tuple( [ t + '_dbid' for t in node ] )
        self.leaf = leaf

    def __call__( self, x, y, args = tuple() ):

        f = self.leaf( *args )
        setattr( f, self.nxat, x )
        setattr( f, self.nyat, y )
        return f

class HookDual( HookPair ):

    def __init__( self, node, leaf ):

        super( HookDual, self ).__init__( [ t.__tablename__ for t in node ], leaf )

class HookChain( HookPair ):

    def __init__( self, leaf ):

        super( HookChain, self ).__init__( ( 'past', 'post' ), leaf )

class HookMono( object ):

    def __init__( self, node, leaf ):

        self.node = node.__tablename__ + '_dbid'
        self.leaf = leaf

    def __call__( self, dbid, args = tuple() ):

        f = self.leaf( *args )
        setattr( f, self.node, dbid )
        return f

class HookDualSeries( object ):

    def __init__( self, node, leaf, dbid ):

        self.nxat, self.nyat = tuple( [ t.__tablename__ + '_dbid' for t in node ] )
        self.nxid, self.nyid = dbid
        self.leaf = leaf

    def __call__( self, args ):

        f = self.leaf( *args )
        setattr( f, self.nxat, self.nxid )
        setattr( f, self.nyat, self.nyid )
        return f

class HookMonoSeries( object ):

    def __init__( self, node, leaf, dbid ):

        self.noat = node.__tablename__ + '_dbid'
        self.noid = dbid
        self.leaf = leaf

    def __call__( self, args ):

        f = self.leaf( *args )
        setattr( f, self.noat, self.noid )
        return f
