

class Mouvement:
    
    # Integer nbUnites
    # Integer couleurJoueur
    # Integer trajet
    def __init__(self, nbUnites, couleurJoueur, trajet ):
        
        self.nbUnites = nbUnites 
        self.couleurJoueur = couleurJoueur 
        self.trajet = trajet 
        
        
    
    def getNbUnites(self):
        return self.nbUnites
        
    def getCouleurJoueur(self):
        return self.couleurJoueur
        
    def getTrajet(self):
        return self.trajet