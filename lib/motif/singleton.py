class SingletonMeta( type ):

    _instance = dict()

    def __call__( cls, *args, **kwargs ):

        if cls not in cls._instance:
            cls._instance[ cls ] = super( SingletonMeta, cls ).__call__( *args, **kwargs )

        return cls._instance[ cls ]

    def __setattr__( self, key, value ):

        if key == '_instance':
            raise AttributeError( 'It is not allowed to reset the instance storage.' )

        return super( SingletonMeta, self ).__setattr__( key, value )


class Singleton( SingletonMeta( 'SingletonMeta', ( object, ), {} ) ):

    def __copy__( self ):

        raise RuntimeError( 'Singleton is noncopyable.' )

    def __deepcopy__( self, memo ):

        raise RuntimeError( 'Singleton is noncopyable.' )
