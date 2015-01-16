
import Cellule as ce

# on utilise 'math' pour trouver l'entier supérieur ou égal le plus proche
import math

class Mouvement:
    
    # Cellule depuis
    # Cellule vers
    # Integer nbUnites
    # Integer couleurJoueur
    # Float temps_restant :  le temps restant avant l'arrivé des unités à destination
    def __init__(self, depuis, vers, nbUnites, couleurJoueur, temps_restant ):
        
        if( not ( isinstance( depuis, ce.Cellule ) and isinstance( vers, ce.Cellule ) ) ):
            raise Exception("les paramètres 'de' et 'vers' sont des cellules")
        
        if( not isinstance( nbUnites , int ) or nbUnites <= 0 ):
            raise Exception("le paramètre 'nbUnites' doit être un entier supérieur à 0")
        
        if( not isinstance( couleurJoueur , int ) or couleurJoueur < 0 ):
            raise Exception("le paramètre 'couleurJoueur' doit être un entier supérieur à 0")
            
        if( temps_restant < 0 ):
            raise Exception("le paramètre 'temps_restant' ne peut pas être inférieur à 0")
            
            
        self.depuis = depuis
        self.vers = vers 
        
        self.nbUnites = nbUnites 
        self.couleurJoueur = couleurJoueur 
        self.temps_restant = temps_restant 
        
        
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
        return self.temps_restant
    
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
                                                                                