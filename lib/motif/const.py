class Const( object ):

    def __setattr__( self, key, val ):
        if key in self.__dict__:
            raise AttributeError( "can't reset an attribute for const object." )

        super( Const, self ).__setattr__( key, val )

    def __copy__( self ):

        return self

    def __deepcopy__( self, memo ):

        return self

    def adopt( self, key, val ):

        super( Const, self ).__setattr__( key, val )
