

class Mouvement:
    
    # Integer nbUnites
    # Integer couleurJoueur
    # Integer trajet
    def __init__(self, nbUnites, couleurJoueur, trajet ):
        
        
        if( not instance( nbUnites , int ) or nbUnites <= 0 ):
            raise Exception("le paramètre 'nbUnites' doit être un entier supérieur à 0")
        
        if( not instance( couleurJoueur , int ) or couleurJoueur < 0 ):
            raise Exception("le paramètre 'couleurJoueur' doit être un entier supérieur à 0")
            
        if( not instance( trajet , int ) or trajet <= 0 ):
            raise Exception("le paramètre 'trajet' doit être un entier supérieur à 0")
            
            
        self.nbUnites = nbUnites 
        self.couleurJoueur = couleurJoueur 
        self.trajet = trajet 
        
        
    
    def getNbUnites(self):
        return self.nbUnites
        
    def getCouleurJoueur(self):
        return self.couleurJoueur
        
    def getTrajet(self):
        return self.trajet