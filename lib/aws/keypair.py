from bakery.lib.motif import Const, Singleton
from bakery.lib.rel import fp
import os


class KeyPair( Const, Singleton ):

    """
    THE key pair for the current user
    """
    
    def __init__( self ):

        def check( x, s ):

            if len( x ) != 2:
                raise RuntimeError( 'Invalid key file.' )
            if x[ 0 ] != s:
                raise RuntimeError( s + ' is not found in the expected place.' )

        path = os.path.join( fp.AWSAUTH, 'key' )
        
        with open( path, 'r' ) as f:
            v = f.readline().strip().split( '=' )
            check( v, 'AWSAccessKeyId' )
            self.access = v[ 1 ]
            u = f.readline().strip().split( '=' )
            check( u, 'AWSSecretKey' )
            self.secret = u[ 1 ]

    def get( self ):

        return self.access, self.secret
