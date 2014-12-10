
import Cellule as ce

# on utilise 'math' pour trouver l'entier supérieur ou égal le plus proche
import math

class Mouvement:
    
    # Cellule depuis
    # Cellule vers
    # Integer nbUnites
    # Integer couleurJoueur
    # Integer trajet
    def __init__(self, depuis, vers, nbUnites, couleurJoueur, trajet ):
        
        if( not ( isinstance( de, ce.Cellule ) and isinstance( vers, ce.Cellule ) ) ):
            raise Exception("les paramètres 'de' et 'vers' sont des cellules")
        
        if( not instance( nbUnites , int ) or nbUnites <= 0 ):
            raise Exception("le paramètre 'nbUnites' doit être un entier supérieur à 0")
        
        if( not instance( couleurJoueur , int ) or couleurJoueur < 0 ):
            raise Exception("le paramètre 'couleurJoueur' doit être un entier supérieur à 0")
            
        if( not instance( trajet , int ) or trajet <= 0 ):
            raise Exception("le paramètre 'trajet' doit être un entier supérieur à 0")
            
            
        self.depuis = depuis
        self.vers = vers 
        
        self.nbUnites = nbUnites 
        self.couleurJoueur = couleurJoueur 
        self.trajet = trajet 
        
        
    # retourne la cellule vers laquelle le mouvement ce dirige
    def toCellule(self):
        return self.vers
        
    # retourne la cellule depuis laquelle le mouvement est originaire
    def fromCellule(self):
        return self.depuis 
    
    def getNbUnites(self):
        return self.nbUnites
        
    def getCouleurJoueur(self):
        return self.couleurJoueur
    
    # retourne la distance déja parcourut par le mouvement
    def getTrajet(self):
        return self.trajet
        
    
    
    
    
    def toOrder( self, uid ):
        pourcentage = math.ceil( self.getNbUnites() * 100 / self.fromCellule().getAttaque() )
        return "[" + uid + "]" + "MOV" + str( pourcentage ) + "FROM" + str( self.fromCellule().getNumero() ) + "TO" + str( self.toCellule().getNumero() )
