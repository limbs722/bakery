import os

def parent( path ):

    return os.path.split( path )[ 0 ]

CROFT = parent( parent( os.path.abspath( __file__ ) ) )
DROPS = os.path.join( parent( CROFT ), 'drops' )
