from bakery.lib.motif.fixture import Fixture
from bakery.lib.aws.secret import get_secret
from bakery.lib.orm.agent import Agent

class Shape(Fixture):
    pass

Shape.fix(lambda t: t, (
    ("DBSTR", "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}"),
    ('LOCAL', 'localhost'),
    ('DBLOC', 'BAKERYDBLOC')
))

def specifier(name, container):
    if not container:
        pass

    secret = get_secret(container)

    return Shape.DBSTR.format(
        secret['username'],
        secret['password'],
        secret['host'],
        secret['port'],
        name
    )

class Agency:
    ''' 데이터베이스 접속 정보를 관리 '''
    """
        conf = os.environ.get( Shape.DBLOC )

        if conf == 'PROD':
            return Agency.prod( name )

        elif conf == 'DEV':
            return Agency.dev( name )

        elif conf == 'LOCAL':
            return Agency.local( name )

        else:
            raise Exception( '환경 세팅 오류' )
    """

    def __init__(self):
        self.book = dict()

    def __call__(self, name):
        return Agency.local(name)

    @staticmethod
    def prod(name, container='prod/bakery/poor'):
        return Agent(specifier(name, container))

    @staticmethod
    def dev(name, container='dev/bakery/poor'):
        return Agent(specifier(name, container))

    @staticmethod
    def local(name, container=None):

        spec = Shape.DBSTR.format(
            'postgres',
            'test1234',
            'localhost',
            5432,
            name
        )

        return Agent(spec)