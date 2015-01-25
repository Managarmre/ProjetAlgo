
import Mouvement as mv


class Strategie:
    """
    Classe abstraite à implémenter pour faire une stratégie
    """
    
    def __init__( self, robot ):
        """
        Constructeur de la classe abstraite Strategie
        """
        self.robot = robot
        
        
    def getRobot(self):
        """
        Retourne le robot 
    
        :return: le robot
        :rtype: :class:'Robot'
        """
        return self.robot
    
    # méthode abstraite
    # retourne la liste des mouvements à effectuer après analyse du terrain (prise de décision)
    def decider(self):
        """
        Méthode abstraite, retourne la liste des mouvements à effectuer après anlayse du terrain pour la prise de décision

        :returns: la liste des nouveaux mouvements à effectuer 
        :rtype: list of :class:'Mouvement'
        :raises NotImplementedError: si la méthode n'a pas été redéfinie.
        """
        raise NotImplementedError( "Abstract Class : Should have implemented this" )
        
        
    def envoyerUnites( self, depuis_cellule, vers_cellules, nb_unites ):
        """
        Permet d'envoyer des unités attaquantes d'une cellule vers une autre, ne fait que modifier le terrain (ne les envoie pas au serveur).
        On modifie le terrain afin de ne par reprendre en compte les unitées déjà utilisés.
        Retourne le mouvement créer !
    
        :param :class:'Cellule' depuis_cellule: La cellule qui envoie les unités attaquantes
        :param :class:'Cellule' vers_cellules: La cellule qui reçoit les unités attaquantes
        :returns: le mouvement créé
        :rtype: :class:'Mouvement'
        """

        couleurJoueur =  depuis_cellule.getCouleur()
        
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
        