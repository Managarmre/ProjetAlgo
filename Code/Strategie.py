
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
        
        robot = self.getRobot()
        terrain = robot.getTerrain()
        lien = terrain.getLienEntreCellules( depuis_cellule, vers_cellules ) 
        
        distance = lien.getDistance()
        vitesse = robot.getVitesse()
        temps_actuel = 0 #robot.getTemps()
        temps_depart = 0 #temps_actuel

        mouvement = mv.Mouvement( depuis_cellule, vers_cellules, nb_unites, couleurJoueur, distance, vitesse, temps_depart, temps_actuel )
        
        lien.ajouterMouvementVersCellule( depuis_cellule, mouvement )
        depuis_cellule.setAttaque( depuis_cellule.getAttaque() - nb_unites )
        terrain.mouvements.append( mouvement )

        return mouvement
        