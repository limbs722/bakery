"""
    local 환경 세팅을 위한 script 파일
    * 주의: 환경 변수 자동으로 LOCAL로 mapping
"""
import sys, os, subprocess
from croft.setup import cp
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

    
    
def main( target_os = 'linux', user_id = None, user_password= None, server_port = 3306):

    if target_os == 'mac':
        bsh('brew update')
        bsh('brew install mysql')
        bsh('brew services start mysql')
        
    elif target_os == 'linux':
        bsh( 'sudo apt update' )
        bsh( 'sudo apt install mysql-server' )
        bsh( 'sudo service mysql start' )

    else:
        raise Exception('')
    
    targ = '.zshrc'
    
    proc( targ, 'CROFTDBLOC', 'LOCAL' )
    proc( targ, 'MYSQLID', user_id )
    proc( targ, 'MYSQLPASSWORD', user_password )
    proc( targ, 'MYSQLPORT', server_port )
    
    bsh( 'source ~/{0}'.format( targ ) )
    
    
if __name__ == '__main__':
    
    parser = ArgumentParser()
    parser.add_argument( "os", type = str, choices=( 'mac', 'linux' ) )
    parser.add_argument( "-i", "--mysql_user_id", type = str, default='root' )
    parser.add_argument( "-s", "--mysql_user_password", type = str, default=None )
    parser.add_argument( "-p", "--mysql_port", type = str, default='3306' )

    args = parser.parse_args()

    sys.exit( main( args.os, args.mysql_user_id, args.mysql_user_password, args.mysql_port ) )
