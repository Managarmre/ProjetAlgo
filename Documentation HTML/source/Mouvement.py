
# on utilise 'math' pour trouver l'entier supérieur ou égal le plus proche
import math
from Exceptions import MouvementException
import Cellule as ce


class Mouvement:
    """
    Un mouvement représente un déplacement d'unités sur un lien.
    
    :param depuis: la cellule au départ du mouvement
    :type depuis: Cellule
    :param vers: la cellule à l'arrivée du mouvement
    :type vers: Cellule
    :param nbUnites: le nombre d'unités qui sont sur le mouvement
    :type nbUnites: int
    :param couleurJoueur: le numéro du joueur auquel appartiennent les unités offensives
    :type couleurJoueur: int
    :param distance: la distance à parcourir sur le lien
    :type distance: int
    :param temps_depart: temps du serveur  lors de l'envoi du mouvement
    :type temps_depart: int
    :param temps_actuel: temps du serveur
    :type temps_actuel: int
    """

    def __init__(self, depuis, vers, nbUnites, couleurJoueur, distance, vitesse, temps_depart, temps_actuel ):

        if( not ( isinstance( depuis, ce.Cellule ) and isinstance( vers, ce.Cellule ) ) ):
            raise MouvementException("les paramètres 'de' et 'vers' sont des cellules")
        
        if( not isinstance( nbUnites , int ) or nbUnites <= 0 ):
            raise MouvementException("le paramètre 'nbUnites' doit être un entier supérieur à 0")
        
        if( not isinstance( couleurJoueur , int ) or couleurJoueur < 0 ):
            raise MouvementException("le paramètre 'couleurJoueur' doit être un entier supérieur à 0")
            
        self.depuis = depuis
        self.vers = vers 
        
        self.nbUnites = nbUnites 
        self.couleurJoueur = couleurJoueur 

        self.distance = distance
        self.vitesse = vitesse
        self.temps_depart = temps_depart
        self.temps_actuel = temps_actuel

        
    def toCellule(self):
        """
        Retourne la cellule vers laquelle le mouvement se dirige
        
        :returns: la cellule vers laquelle le mouvement se dirige
        :rtype: Cellule
        """
        return self.vers
        

    def fromCellule(self):
        """
        Retourne la cellule depuis laquelle le mouvement est originaire
        
        :returns: la cellule depuis laquelle le mouvement est originaire
        :rtype: Cellule
        """
        return self.depuis 
    

    def getNbUnites(self):
        """
        Retourne le nombre d'unités sur le mouvement
        
        :returns: le nombre d'unités 
        :rtype: int
        """
        return self.nbUnites
        

    def getCouleur(self):
        """
        Retourne la couleur du mouvement, c'est à dire le numéro du joueur qui envoie le mouvement.
        
        :returns: la couleur du mouvement
        :rtype: int
        """
        return self.couleurJoueur


    def getTempsRestant(self):
        """
        Retourne le temps restant à parcourir avant l'arrivée du mouvement à destination.
        
        :returns: le temps restant à parcourir
        :rtype: int
        """

        distance_parcourue = self.temps_actuel - self.temps_depart

        temps_restant = ( self.distance - distance_parcourue ) / self.vitesse

        return temps_restant if temps_restant > 0 else 0


    def getTempsDepart(self):
        """
        Retourne le temps de départ du mouvement
        
        :returns: le temps de départ du mouvement
        :rtype: int
        """
        return self.temps_depart


    def getVitesse(self):
        """
        Retourne la vitesse du mouvement
        
        :returns: la vitesse du mouvement
        :rtype: int
        """
        return self.vitesse


    def getDistance(self):
        """
        Retourne la distance totale à parcourir par le mouvement.
        
        :returns: la distance totale à parcourir par le mouvement
        :rtype: int
        """
        return self.distance


    def getTempsActuel(self):
        """
        Retourne le temps actuel du serveur
        
        :returns: le temps actuel du serveur
        :rtype: int
        """
        return self.temps_actuel


    def setTempsActuel( self, temps_actuel ):
        """
        Affecte la variable temps_actuel avec la valeur passée en paramètre
        
        :param temps_actuel: le temps du serveur
        :type temps_actuel: int
        """
        self.temps_actuel = temps_actuel
    

    def aPourCouleur( self, couleurJoueur ):
        """
        Retourne vrai si le mouvement possède la couleur passée en paramètre.
        (donc si le mouvement appartient au joueur ayant cette couleur)
        
        :param int couleurJoueur: la couleur du joueur
        :type couleurJoueur: int
        :returns: vrai si le mouvement possède cette couleur, faux sinon.
        :rtype: booleen
        """
        return self.couleurJoueur == couleurJoueur
    

    def toOrder( self, uid ):
        """
        Retourne l'ordre correspondant au mouvement associé dans la forme du protocole du serveur

        :returns: l'ordre correspondant au mouvement
        :rtype: str
        """
        pourcentage = math.ceil( self.getNbUnites() * 100 / ( self.fromCellule().getAttaque() + self.getNbUnites() ) )
        
        return "[{uid}]MOV{pourcentage}FROM{origine}TO{destination}".format(    uid = uid,
                                                                                pourcentage = pourcentage ,
                                                                                origine = self.fromCellule().getNumero() ,
                                                                                destination = self.toCellule().getNumero() )
                                                                                