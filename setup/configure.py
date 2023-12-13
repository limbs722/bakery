import os, shutil, sys
from bakery.setup import cp
from bakery.setup.awskey import AWSKey
from argparse import ArgumentParser as Parser

# brew install postgresql@16

def drops( awscredsrc ):
    
    dst = cp.DROPS
    if os.path.exists( dst ):
        if os.path.isfile( dst ):
            os.remove( dst )
        else:
            shutil.rmtree( dst )


    if os.path.exists( os.path.join( dst, '.aws') ) == False:
            os.makedirs( os.path.join( dst, '.aws'))

    AWSKey.load( awscredsrc ).sink( os.path.join( dst, '.aws', 'key' ) )

def main():

    parser = Parser()
    #parser.add_argument( 'awscredsrc', help = 'full path to aws key-pair credentials.csv' )
    parser.add_argument( 'awscredsrc', help = 'full path to aws key-pair credentials.csv' )

    args = parser.parse_args()

    print( 'installing drops ...' )
    drops( args.awscredsrc )

if __name__ == '__main__':

    sys.exit( main() )
