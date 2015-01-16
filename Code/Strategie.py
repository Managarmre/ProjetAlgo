
import Mouvement as mv


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
        
        
    def envoyerUnites( self, depuis_cellule, vers_cellules, nb_unites ):
                        
        couleurJoueur =  depuis_cellule.getCouleurJoueur()
        
        terrain = self.getRobot().getTerrain()
        lien = terrain.getLienEntreCellules( depuis_cellule, vers_cellules ) 
        
        mouvement = mv.Mouvement( depuis_cellule, vers_cellules, nb_unites, couleurJoueur, lien.getDistance() )
        
        lien.ajouterMouvementVersCellule( depuis_cellule, mouvement )
        depuis_cellule.setAttaque( depuis_cellule.getAttaque() - nb_unites )
        
        return mouvement
        