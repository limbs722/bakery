from bakery.lib.motif import Fixture, Const


class Region( Const ):
        
    def __init__( self, name, code, zone ):

        self.name = name
        self.code = code
        self.zone = set( zone )

    def __str__( self ):

        return self.name

    def __repr__( self ):

        return 'Region({0}|{1})'.format( self.name, self.code )

    def __eq__( self, other ):

        return self.name == other.name and self.code == other.code and self.zone == other.zone

    def __ne__( self, other ):
        
        return self.name != other.name or self.code != other.code or self.zone != other.zone
                            
    def __hash__( self ):

        return self.name.__hash__()

    def fullname( self ):

        return '-'.join( [ 'buy', 'signal', self.name ] )

    def specified( self, zone ):

        return self.code + zone
    

class Hub( Fixture ):

    @staticmethod
    def roster():

        f = lambda x: getattr( Hub, x )
        return [ f( t ) for t in Hub.__dict__ if isinstance( f( t ), Region ) ]

    @staticmethod
    def find( code ):

        for t in Hub.__dict__:
            a = getattr( Hub, t )
            if isinstance( a, Region ) and a.code == code:
                return a
        return None

Hub.fix( lambda x: ( x[ 0 ].upper(), Region( *x ) ), (
    ( 'tokyo', 'ap-northeast-1', 'ac' ),
    ( 'seoul', 'ap-northeast-2', 'ac' ),
    ( 'singapore', 'ap-southeast-1', 'ab' ),
    ( 'sydney', 'ap-southeast-2', 'abc' ),
    ( 'frankfurt', 'eu-central-1', 'ab' ),
    ( 'ireland', 'eu-west-1', 'abc' ),
    ( 'london', 'eu-west-2', 'ab' ),
    ( 'virginia', 'us-east-1', 'abcde' ),
    ( 'ohio', 'us-east-2', 'abc' ),
    ( 'california', 'us-west-1', 'abc' ),
    ( 'oregon', 'us-west-2', 'abc' )
) ) 

