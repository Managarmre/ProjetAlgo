
import Cellule as ce

# on utilise 'math' pour trouver l'entier supérieur ou égal le plus proche
import math

class Mouvement:
    
    # Cellule depuis
    # Cellule vers
    # 
    # Integer nbUnites
    # Integer couleurJoueur
    # Float temps_restant :  le temps restant avant l'arrivé des unités à destination
    def __init__(self, depuis, vers, nbUnites, couleurJoueur, distance, vitesse, temps_depart, temps_actuel ):
        
        if( not ( isinstance( depuis, ce.Cellule ) and isinstance( vers, ce.Cellule ) ) ):
            raise Exception("les paramètres 'de' et 'vers' sont des cellules")
        
        if( not isinstance( nbUnites , int ) or nbUnites <= 0 ):
            raise Exception("le paramètre 'nbUnites' doit être un entier supérieur à 0")
        
        if( not isinstance( couleurJoueur , int ) or couleurJoueur < 0 ):
            raise Exception("le paramètre 'couleurJoueur' doit être un entier supérieur à 0")
        
        """ 
        if( temps_restant < 0 ):
            raise Exception("le paramètre 'temps_restant' ne peut pas être inférieur à 0")
        """ 
            
        self.depuis = depuis
        self.vers = vers 
        
        self.nbUnites = nbUnites 
        self.couleurJoueur = couleurJoueur 

        self.distance = distance
        self.vitesse = vitesse
        self.temps_depart = temps_depart
        self.temps_actuel = temps_actuel

        # self.temps_restant = temps_restant 
        
        
    # retourne la cellule vers laquelle le mouvement se dirige
    def toCellule(self):
        return self.vers
        
    # retourne la cellule depuis laquelle le mouvement est originaire
    def fromCellule(self):
        return self.depuis 
    
    def getNbUnites(self):
        return self.nbUnites
        
    def getCouleurJoueur(self):
        return self.couleurJoueur
    




    # retourne le temps de trajet restant avant l'arrivée des unités à destination
    def getTempsRestant(self):
        
        distance_parcourue = self.temps_actuel - self.temps_depart

        temps_restant = ( self.distance - distance_parcourue ) / self.vitesse

        return temps_restant if temps_restant > 0 else 0


    def getTempsDepart(self):
        return self.temps_depart

    def getVitesse(self):
        return self.vitesse

    def getDistance(self):
        return self.distance

    def getTempsActuel(self):
        return self.temps_actuel

    def setTempsActuel( self, temps_actuel ):
        self.temps_actuel = temps_actuel





    
    # retourne vrai si le mouvement a la couleur donnée (appartient au joueur ayant cette couleur)
    def aPourCouleur( self, couleurJoueur ):
        return self.couleurJoueur == couleurJoueur
    
    # retourne dans la forme du protocole du serveur, l'ordre correspondant au mouvement associé
    def toOrder( self, uid ):
        pourcentage = math.ceil( self.getNbUnites() * 100 / ( self.fromCellule().getAttaque() + self.getNbUnites() ) )
        
        return "[{uid}]MOV{pourcentage}FROM{origine}TO{destination}".format(    uid = uid,
                                                                                pourcentage = pourcentage ,
                                                                                origine = self.fromCellule().getNumero() ,
                                                                                destination = self.toCellule().getNumero() )
                                                                                