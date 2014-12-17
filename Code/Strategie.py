

# classe abstraite
class Strategie:
    
    
    def __init__( self, robot ):
        self.robot = robot
        
        
    def getRobot(self):
        return self.robot
    
    # méthode abstraite
    # retourne la liste des mouvements à effectuer après analyse du terrain (prise de décision)
    def decider(self):
        raise NotImplementedError( "Abstract Class : Should have implemented this" )
        
    