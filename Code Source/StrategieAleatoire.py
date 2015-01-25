import logging
import random
from Strategie import *
from Mouvement import *


class StrategieAleatoire( Strategie ):
    """
    1ere stratégie qui attaque aléatoirement.

    L'envoi des unités ainsi que leur destination sera déterminée aléatoirement.

    :param robot: Le robot devant prendre une decision
    :type robot: Robot
    """

    def __init__( self, robot ):
        Strategie.__init__( self, robot )
        
        
    def decider(self):
        """
        Retourne la liste des mouvements à effectuer après analyse du terrain pour la prise de décision.

        :returns: la liste des nouveaux mouvements à effectuer 
        :rtype: List<Mouvement>
        """

        
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
                    
                pourcentage = nbUnitees / maCellule.getAttaque()
            
                vers_cellule = leLien.getOtherCellule( maCellule )
                nbUnites = random.randint(1, maCellule.getAttaque() )

                mouv = self.envoyerUnites( maCellule, vers_cellule, nb_unites )
                                
                mouvements.append( mouv )
        
        return mouvements
        
    