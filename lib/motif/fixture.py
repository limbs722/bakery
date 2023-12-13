class FixtureDescriptor( object ):

    def __init__( self, fget ):

        self._fget = fget

    def __get__( self, obj, cls ):

        return self._fget.__get__( obj, cls )()

    def __set__( self, obj, val ):

        raise AttributeError( 'Fixture is not allowed to reset.' )

def fixture( func ):

    if not isinstance( func, ( classmethod, staticmethod ) ):
        func = classmethod( func )

    return FixtureDescriptor( func )

class FixtureMeta( type ):

    def __setattr__( self, key, value ):

        if key in self.__dict__:
            obj = self.__dict__.get( key )
            if obj and type( obj ) is FixtureDescriptor:
                return obj.__set__( self, value )

        return super( FixtureMeta, self ).__setattr__( key, value )
    
def easyfix( x ):

    return fixture( lambda cls: x )

def regular( a ):

    return str( a or '' ).upper().replace( '-', '_' )

class Fixture( FixtureMeta( 'FixtureMeta', ( object, ), {} ) ):

    @classmethod
    def fix( cls, parser, iterable ):
        
        for item in iterable:
            a, b = parser( item )
            setattr( cls, a, easyfix( b ) )

    @classmethod
    def native( cls ):

        f = lambda x: getattr( cls, x )
        return [ f( t ) for t in set( cls.__dict__ ) if not t.startswith( '__' ) ]

    @classmethod
    def bind( cls, a ):

        return getattr( cls, regular( a ) )

    @classmethod
    def bindOrNone( cls, a ):

        return cls.bind( a ) if hasattr( cls, regular( a ) ) else None
    
    @staticmethod
    def union( parser, *args ) :
        
        nset = []
        nobj = type(f'MergedFixture', (Fixture,), {})        
        
        for u in args:            
            nset += [ ( t, getattr( u, t )) for t in set( u.__dict__ ) if not t.startswith( '__' )]

        nobj.fix( parser, nset )
        
        return nobj


if __name__ == '__main__':
    
    class A( Fixture ): pass
    class B( Fixture ): pass
    class C( Fixture ): pass
    
    
    A.fix( lambda t: t, ( ( 'a', '1'),))
    B.fix( lambda t: t, ( ( 'b', '2'),))
    C.fix( lambda t: t, ( ( 'c', '3'),))
    
    merged = Fixture.union(lambda t: t, A, B, C )
    
    print( merged.a )
    print( merged.b )
    print( merged.c )