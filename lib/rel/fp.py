import os
from bakery.lib.motif import Fixture


def parent( p ):

    return os.path.split( p )[ 0 ]

_BAKERY = parent( parent( parent( os.path.abspath( __file__ ) ) ) )
_DROPS = os.path.join( os.path.split( _BAKERY )[ 0 ], 'drops' )

class fp( Fixture ):
    pass
    

    
fp.fix( lambda x: ( x[ 0 ].upper(), os.path.join( *x[ 1 ] ) ), (
    ( 'bakery', ( _BAKERY, ) ),
    ( 'awsauth', ( _DROPS, '.aws' ) ),
    ( 'bakeryauth', ( _DROPS, '.croft' ) ),
    ( 'drops', ( _DROPS, ) ),
    ( 'git', ( _BAKERY, '.git' ) ),
    ( 'ssh', ( os.path.expanduser( '~' ), '.ssh' ) ),    
) )
