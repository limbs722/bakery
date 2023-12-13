import boto3, json
from botocore.exceptions import ClientError
from bakery.lib.aws.keypair import KeyPair

'''test/lib/secret.py
'''
def get_secret( secret_name, region_name = 'ap-northeast-2' ):
    keypair = KeyPair()
    sess = boto3.session.Session( aws_access_key_id = keypair.access, aws_secret_access_key = keypair.secret )
    node = sess.client( service_name = 'secretsmanager', region_name = region_name )
    
    try:
        resp = node.get_secret_value( SecretId = secret_name, )
        
    except ClientError as e:
        
        raise e

    return json.loads( resp[ 'SecretString' ] )
    