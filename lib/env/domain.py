from bakery.lib.motif import Singleton, Const, Fixture
import os

class Local( Fixture ): pass
class Dev( Fixture ): pass
class Prod( Fixture ): pass
class Third( Fixture ): pass


Local.fix( lambda t: t, (
    ( 'AUTH', 'http://localhost:8001' ),
    ( 'SYNC', 'http://localhost:8000' ),
))

Dev.fix( lambda t: t, (
    ( 'AUTH', 'http://localhost:8001' ),
    ( 'SYNC', 'https://sync.carepia.co.kr' ),
))

Prod.fix( lambda t: t, (
    ( 'AUTH', 'http://localhost:8001' ),
    ( 'SYNC', 'https://sync.carepia.co.kr' ),
))

class Domain( Singleton, Const ):
  
    def __init__ ( self ):
        
        conf = os.environ.get( 'BAKERYDBLOC' )
        
        if conf == 'DEV':
            self.inst = Dev
        elif conf == 'PROD':
            self.inst = Prod
        else:
            self.inst = Local
        
    @property
    def AUTH( self ):
        
        return self.inst.AUTH
    
    @property
    def SYNC( self ):
        
        return self.inst.SYNC
