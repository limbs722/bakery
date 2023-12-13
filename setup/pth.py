import sys, os, site

def parent( p ):

    return os.path.split( p )[ 0 ]

def main():

    root = parent( parent( parent( os.path.abspath( __file__ ) ) ) )
    cand = site.getsitepackages()
    
    for path in cand:
        dest = os.path.join( path, 'dev.pth' )
        
        if os.path.isfile( dest ):
            with open( dest, 'r' ) as f:
                print( dest )
                line = next( f ).strip()
                
                if line == root:
                    print( 'correct dev.pth found' )
                    return
                
            print( 'remove conflicting dev.pth ...' )
            
            os.remove( dest )

    print( 'install new dev.pth ...' )
    
    path = cand[ 0 ]
    dest = os.path.join( path, 'dev.pth' )
    
    with open( dest, 'w' ) as f:
        f.write( root + '\n' )
        

if __name__ == '__main__':

    sys.exit( main() )
