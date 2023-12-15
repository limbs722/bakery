from bakery.lib.motif import Singleton, Const
import re

class Camel( Const, Singleton ):

    def __init__( self ):

        self.rega = re.compile( '(.)([A-Z][a-z]+)' )
        self.rege = re.compile( '([a-z0-9])([A-Z])' )

    def __call__( self, s ):

        return self.rege.sub( r'\1_\2', self.rega.sub( r'\1_\2', s ) ).lower()

