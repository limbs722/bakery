from bakery.lib.motif import Const, Singleton
from bakery.lib.aws.hub import Hub
from bakery.lib.aws.keypair import KeyPair
from fnmatch import fnmatch
from boto3.s3.transfer import TransferConfig
import botocore, boto3

def _delimit( p ):

    return p if p[ -1 ] == '/' else p + '/'


class Section( Const ):

    def __init__( self, bucket ):

        self.bucket = bucket
        
    @property
    def name( self ):

        return self.bucket.name

    def region( self ):

        return Hub.find( self.bucket.meta.client.get_bucket_location( Bucket = self.bucket.name )[ "LocationConstraint" ] )

    def nodes( self, prefix = None ):

        pagn = self.bucket.meta.client.get_paginator( 'list_objects' )
        kwargs = dict(
            Bucket = self.bucket.name,
            Delimiter = '/'
        )
        if prefix:
            kwargs[ 'Prefix' ] = _delimit( prefix )

        p = list()
        for i in pagn.paginate( **kwargs ):
            p.extend( i.get( 'CommonPrefixes' ) )

        if len( p ):
            return [ t.get( 'Prefix' ) for t in p ]
        else:
            return list()

    def leaves( self, prefix = None ):
        
        if prefix is not None:
            return [
                t.key for t in self.bucket.objects.filter( Prefix = prefix )
            ]
        else:
            return [ t.key for t in self.bucket.objects.all() ]

    def add( self, key, content, mimetype = None ):

        kwargs = dict( Key = key, Body = content )
        if mimetype is not None:
            kwargs[ 'ContentType' ] = mimetype
        self.bucket.put_object( **kwargs )

    def content( self, key ):

        return self.bucket.Object( key ).get()[ 'Body' ].read()

    def remove( self, keys ):

        for key in keys:
            f = self.bucket.Object( key )
            f.delete()

    def clear( self ):

        for item in self.bucket.objects.all():
            item.delete()

    def rename( self, before, after ):

        name = self.bucket.name + '/' + before
        self.bucket.Object( after ).copy_from( CopySource = name )
        self.bucket.Object( before ).delete()            


class Storage( Const, Singleton ):

    def __init__( self ):

        k = KeyPair()
        s = boto3.session.Session(
            aws_access_key_id = k.access,
            aws_secret_access_key = k.secret
        )
        self.resource = s.resource( 's3' )
        self.client = s.client( 's3' )

    def has( self, name ):

        try:
            self.resource.meta.client.head_bucket( Bucket = name )
        except botocore.exceptions.ClientError as e:
            code = int( e.response[ 'Error' ][ 'Code' ] )
            if code == 404:
                return False
        return True

    def section( self, name ):

        bucket = self.resource.Bucket( name )
        return Section( bucket )

    def create( self, name, region ):

        r = Hub.bind( region )
        if r is Hub.VIRGINIA:
            return Section( self.resource.create_bucket( Bucket = name ) )
        else:
            return Section( 
                self.resource.create_bucket( 
                    Bucket = name,
                    CreateBucketConfiguration = { 
                        'LocationConstraint': r.code
                    }
                ) 
        )

    def delete( self, name ):

        if self.has( name ):
            s = self.section( name )
            s.clear()
            s._bucket.delete()

    def match( self, pattern ):

        resp = self.client.list_buckets()
        f = list()
        for b in resp[ 'Buckets' ]:
            n = b[ 'Name' ]
            if fnmatch( n, pattern ):
                f.append( n )
        return f

    def upload( self, local, remote, key, option = {}, speedup = False ):

        if speedup:
            self.client.upload_file( local, remote, key, ExtraArgs = option, Config = TransferConfig() )
        else:
            self.client.upload_file( local, remote, key, ExtraArgs = option )

    def reload( self, local, remote, key, option = {} ):

        s = self.section( remote )
        if key in s.leaves():
            s.remove( [ key ] )
        self.upload( local, remote, key, option )

    def download( self, remote, key, local ):

        self.client.download_file( remote, key, local )

    def transfer( self, src, dst, key ):

        bdst = self.resource.Bucket( dst )
        bdst.Object( key ).copy_from( CopySource = '/'.join( [ src, key ] ) )
        bsrc = self.resource.Bucket( src )
        bsrc.Object( key ).delete()

    def remove( self, src, key ):

        bsrc = self.resource.Bucket( src )
        bsrc.Object( key ).delete()

    def read( self, remote, key ):

        obj = self.client.get_object( Bucket = remote, Key = key )
        return obj[ 'Body' ].read()

    def sizeof( self, remote, key ):

        obj = self.client.get_object( Bucket = remote, Key = key )
        return obj[ 'ContentLength' ]
