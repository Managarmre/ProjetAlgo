


class Strategie:
    
    
    def __init__( self, robot ):
        self.robot = robot
        
        
    def getRobot(self):
        return self.robot
    
    
    
    def decider(self):
        raise NotImplementedError( "Abstract Class : Should have implemented this" )
        
    