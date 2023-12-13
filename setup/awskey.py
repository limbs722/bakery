import boto3, csv, os

class AWSKey( object ):

    def __init__( self, access, secret ):

        self._access = access
        self._secret = secret
        
    @staticmethod
    def load( path ):

        with open( path, 'r' ) as f:
            reader = csv.reader( f )
            next( reader )
            access, secret = next( reader )

        return AWSKey( access, secret )
            
    def sink( self, dest ):


        if self.verify():
            with open( dest, 'w' ) as f:
                f.write( 'AWSAccessKeyId={0}\n'.format( self._access ) )
                f.write( 'AWSSecretKey={0}\n'.format( self._secret ) )
        else:
            raise RuntimeError( 'Invalid key pair')

    def verify( self, r = 'us-west-1' ):

        session = boto3.session.Session(
            aws_access_key_id = self._access,
            aws_secret_access_key = self._secret,
            region_name = r
            )
        try:
            return len( session.client( 'ec2' ).describe_hosts() ) > 0
        except Exception:
            return False

