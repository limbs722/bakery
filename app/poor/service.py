from bakery.lib.motif.const import Const
from bakery.app.poor.admina import Admina
from bakery.app.poor.mapper import User

class Service(Const):

    def __init__(self):
        self.agent = Admina.instance().agent()

    def signup(self, user_email):
        """
            cognito 에 등록된 user id 등록
        """
        with self.agent.scope() as session:
            user = session.query(User).filter(User.email == user_email).first()

            if not user:
                user = User(email=user_email)

                session.add(user)
                session.flush()

            else:
                raise Exception("user Exist")
            
    def withdraw(self, user_email):
        """
            cognito 에 등록된 user id 해제
        """
        with self.agent.scope() as session:
            user = session.query(User).filter(User.email == user_email).first()

            if user:
                session.delete(user)

            else:
                return Exception("User Not Found")