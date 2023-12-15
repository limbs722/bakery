from bakery.lib.motif import Private, Const
from bakery.app.poor.agency import Agency

class Admina(Private, Const):
    
    @staticmethod
    def create(name):
        x = object.__new__(Admina)
        x.name = name
        return x
    
    @staticmethod
    def instance():
        return Admina.create('poordb')
    
    def agent(self):
        return Agency()(self.name)
    

if __name__ == '__main__':
    inst = Admina.instance()
    agnt = inst.agent()

    from bakery.app.poor.mapper import Basis

    agnt.generate(Basis)