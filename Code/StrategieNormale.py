from Strategie import *
from Mouvement import *


class StrategieNormale( Strategie ):
    
    def __init__( self, robot ):
        Strategie.__init__( self, robot )
        
        
    # liste1 - liste2 : totu ce qui est présent dans liste1 mais pas dans liste2
    def difference_liste( liste1, liste2 ):
        return [ val for val in liste1 if val not in liste2 ]
        
        
        
    def decider(self):
        
        terrain = self.getRobot().getTerrain()
        
        for composante in terrain.getSousGraphe( self.getMesCellules() ).getComposantesConnexes() :
            print( composante.toString() )
        
        """
        mesCellules = self.getMesCellules()
        
        productrices = self.getCellulesProductrices( mesCellules )
        attaquantes = self.getCellulesAttaquantes( mesCellules, productrices )
        
        semi_productrices = self.getSemiProductrices( productrices, attaquantes )
        full_productrices = self.getFullProductrices( productrices , semi_productrices )
        
        attaquantes_en_dangees = []
        attaquantes_en_suretees = []
        
        print( mesCellules )
        print( attaquantes )
        print( productrices )
        print( semi_productrices )
        print( full_productrices )
        print( attaquantes_en_dangees )
        print( attaquantes_en_suretees )
        
        """
        
        return []
        
    
    
    
    def getMesCellules( self ):
        return self.getRobot().getTerrain().getCellulesJoueur( self.getRobot().getMaCouleur() )
        
    
    
    def getCellulesProductrices( self, mesCellules ):
        
        maCouleur = self.getRobot().getMaCouleur()
        
        productrices = []
        
        for cellule in mesCellules:

            booleen = True
            for voisin in cellule.getVoisins():
                if( voisin.getCouleurJoueur() != maCouleur ):
                    booleen = False
                    break
            
            if( booleen ):
                productrices.append( cellule )
        
        return productrices
        
    
    def getCellulesAttaquantes( self, mesCellules, productrices ):
        return StrategieNormale.difference_liste(mesCellules,productrices)
        
        
    def getSemiProductrices( self, productrices, attaquantes ):
        
        maCouleur = self.getRobot().getMaCouleur()
        semi_productrices = [] 
        
        for cellule in productrices:
    
            for voisin in cellule.getVoisins():
                if( voisin in attaquantes ):
                    semi_productrices.append( cellule )
                    break
        
        return semi_productrices
    
    
    
    def getFullProductrices( self, productrices, semi_productrices ):
        return StrategieNormale.difference_liste(productrices, semi_productrices)
        
        
    