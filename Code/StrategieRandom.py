import logging
import random
from Strategie import *
from Mouvement import *


class StrategieRandom( Strategie ):
    
    def __init__( self, robot ):
        Strategie.__init__( self, robot )
        
        
    def decider(self):
        
        logging.info( "prise de décision en cours...." )
        
        robot = self.getRobot()
        
        mesCellules = robot.getTerrain().getCellulesJoueur( robot.getMaCouleur() )
        
        # liste des mouvements que le robot va faire
        mouvements = []
        
        for maCellule in mesCellules :
            
            # si il y a au moins 10% des unités max de la cellule
            if( maCellule.getAttaque() >= maCellule.getAttaqueMax() * 10 / 100 ):
                
                lesLiens = maCellule.getLiens()
                leLien = lesLiens[ random.randint(0, len(lesLiens)-1 ) ]
                
                nbUnitees = random.randint(1, maCellule.getAttaque() )
                pourcentage = nbUnitees / maCellule.getAttaque()
                
                
                mouv = Mouvement( maCellule, leLien.getOtherCellule( maCellule ), nbUnitees, robot.getMaCouleur(), 0 )
                
                # [<userid>]MOV<%offunits>FROM<cellid>TO<cellid>
                
                mouvements.append( mouv )
                
        return mouvements
        
    