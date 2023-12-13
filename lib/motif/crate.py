import json


def _usr( a, b ):

    return a[ :2 ] != '__' and not type( b ).__name__.endswith( 'method' )


class Crate( object ):

    """
    Json compatible immutable container

    """

    @staticmethod
    def c2f( c ):

        if c is None or isinstance( c, ( int, float, str ) ):
            return c
        elif isinstance( c, ( list, tuple ) ):
            return list( map( lambda t: Crate.c2f( t ), c ) )
        elif isinstance( c, dict ):
            d = dict()
            for k, v in c.items():
                d[ k ] = Crate.c2f( v )
            return d
        elif isinstance( c, Crate ):
            return c.deflate()
        else:
            raise ValueError( 'Unsupportd value type.' )
    
    @staticmethod
    def f2c( x ):

        if x is None or isinstance( x, ( int, float, str, Crate ) ):
            return x
        elif isinstance( x, bytes ):
            return x.decode()
        elif isinstance( x, ( list, tuple ) ):
            return tuple( map( Crate.f2c, x ) )
        elif isinstance( x, dict ):
            h = object.__new__( Crate )
            for k, v in x.items():
                setattr( h, k, Crate.f2c( v ) )
            return h
        else:
            raise ValueError( 'Unsupported value type.' )

    @staticmethod
    def pup( p, u ):

        for a, b in u:
            if not p.has( a ):
                setattr( p, a, b )
            elif isinstance( b, Crate ):
                q = p( a )
                if isinstance( q, Crate ):
                    Crate.pup( q, b )

    @staticmethod
    def compare( x, y ):

        if x is None or isinstance( x, ( int, float, str ) ):
            
            return x == y
        
        elif isinstance( x, tuple ):
            
            if not isinstance( y, tuple ) or len( x ) != len( y ):
                return False
            
            for a, b in zip( x, y ):
                
                if not Crate.compare( a, b ):
                    return False
                
            return True
        elif isinstance( x, Crate ):
            
            if not isinstance( y, Crate ):
                return False
            
            p = set( a for a, b in x )
            q = set( a for a, b in y )
            
            if p != q:
                return False
            for k in p:
                if not Crate.compare( x( k ), y( k ) ):
                    return False
            return True
        else:
            raise ValueError( 'Unsupported value type.' )
    
    @staticmethod
    def inflate( d ):

        c = Crate.f2c( d )
        if not isinstance( c, Crate ):
            raise ValueError( 'Invalid representation for Crate.' )
        return c
        
    def __iter__( self ):

        return ( ( a, b ) for a, b in self.__dict__.items() if _usr( a, b ) )

    def __call__( self, key, fail = None ):

        x = getattr( self, key, fail )
        if not type( x ).__name__.endswith( 'method' ):
            return x

    def __setattr__( self, key, val_ ):

        if key in self.__dict__:
            raise AttributeError( "can't reset an attribute for const object." )
        val = Crate.f2c( val_ )
        super( Crate, self ).__setattr__( key, val )

    def __len__( self ):

        return sum( 1 for a, b in self.__dict__.items() if _usr( a, b ) )

    def __eq__( self, other ):

        if not isinstance( other, Crate ):
            return False
        return Crate.compare( self, other )

    def __ne__( self, other ):

        return not( other == self )

    def __contains__( self, key ):

        return self.has( key )

    def keys( self ):

        return [ a for a, b in self.__dict__.items() if _usr( a, b ) ]

    def has( self, key ):

        v = getattr( self, key, None )
        return v is not None and isinstance( v, ( int, float, str, tuple, Crate ) )

    def update( self, other ):

        Crate.pup( self, other )

    def deflate( self ):

        d = dict()
        for a, b in self:
            d[ a ] = Crate.c2f( b ) 
        return d

    def pack( self ):

        return json.dumps( self.deflate() )

    @staticmethod
    def parse( s ):

        return Crate.f2c( json.loads( s ) )

    def cover( self, other ):

        for a, b in other:
            if not hasattr( self, a ):
                return False
            if isinstance( b, Crate ):
                p = getattr( self, a )
                if not isinstance( p, Crate ):
                    return False
                if not p.cover( b ):
                    return False
        return True

    def conflict( self, other ):

        for a, b in other:
            if hasattr( self, a ) and getattr( self, a ) != b:
                return True
        return False

    def superior( self, other ):

        return self.cover( other ) and not self.conflict( other )
