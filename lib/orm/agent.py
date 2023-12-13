from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager

'''test/lib/agent.py
'''
def barf( s ):

    raise RuntimeError( s )

class Agent:
    
    def __init__( self, specifier, isolation = 'READ UNCOMMITTED', timeout = 5 ):
        
        self.engine = create_engine(
            specifier,
            isolation_level = isolation,
            connect_args = { 'connect_timeout': timeout }
        )
        
        self.generator = sessionmaker( bind = self.engine )

    @property
    def name( self ):

        return str( self.engine )
    
    def session( self ):

        return scoped_session( self.generator )
    
    @contextmanager
    def scope( self, handler = barf ):

        session = self.session()
        
        try:
            yield session
            session.commit()
            
        except exc.SQLAlchemyError as e:
            session.rollback()
            handler( str( e ) )
            
        finally:
            session.remove()
            
    def generate( self, basis ):
        
        basis.metadata.create_all( self.engine )