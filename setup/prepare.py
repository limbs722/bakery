import sys, os, subprocess
from bakery.setup import cp
from argparse import ArgumentParser

def bsh( cmd ):

    proc = subprocess.Popen( cmd, shell = True, executable = '/opt/homebrew/bin/zsh' )
    if proc.wait() != 0:
        raise RuntimeError( 'Failed: {0}'.format( cmd ) )

def proc(targ, nkey, nval):
    node = os.path.expanduser('~/{0}'.format(targ))
    
    with open(node, 'r') as f:
        nset = f.readlines()
    
    # nkey가 포함된 라인을 제외하고 모든 라인들을 선택합니다.
    fset = [line for line in nset if nkey not in line]
    
    with open(node, 'w') as f:
        f.writelines(fset)
        f.write('export {0}={1}\n'.format(nkey, nval))  # 이 부분을 'w' 모드에서 같이 처리해 줄 수 있습니다.
    
    
def main( target_os = 'linux'):

    if target_os == 'mac':
        bsh('brew install python3')
        bsh('sudo -H pip3 install --upgrade pip')
        
    else:
        bsh( 'sudo apt update' )
        bsh( 'sudo apt install python3-pip' )
        bsh( 'sudo -H pip3 install --upgrade pip' )
    
    bsh( 'sudo -H pip install -r {0}/requirements.txt'.format( cp.CROFT ) )
        
    targ = '.zshrc'
    
    proc( targ, 'BAKERYDBLOC', 'DEV' )
    proc( targ, 'BAKERYENV', 'DEV' )
        
    bsh( 'source ~/{0}'.format( targ ) )
    
    
if __name__ == '__main__':
    
    parser = ArgumentParser()
    parser.add_argument( "os", type = str, choices=( 'mac', 'linux' ) )

    args = parser.parse_args()

    sys.exit( main( args.os ) )
