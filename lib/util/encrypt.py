import bcrypt

class Encrypt:
    @staticmethod
    def encode_if_necessary( input ):
        if isinstance(input, bytes):
            try:
                input.decode( 'utf-8' )
                return input
            except UnicodeDecodeError:
                pass
        return str( input ).encode( 'utf-8' )
    
    @staticmethod
    def encrypt( input_password ):
        return bcrypt.hashpw( Encrypt.encode_if_necessary( input_password ), bcrypt.gensalt() )
    
    @staticmethod
    def verify( plain_password, hashed_password ):
        return bcrypt.checkpw( Encrypt.encode_if_necessary( plain_password ), Encrypt.encode_if_necessary( hashed_password ) )