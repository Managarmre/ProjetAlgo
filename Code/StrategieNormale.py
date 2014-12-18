from Strategie import *
from Mouvement import *


class StrategieNormale( Strategie ):
    
    def __init__( self, robot ):
        Strategie.__init__( self, robot )
        
        
    # liste1 - liste2 : totu ce qui est présent dans liste1 mais pas dans liste2
    def difference_liste( liste1, liste2 ):
        return [ val for val in liste1 if val not in liste2 ]
        
    def decider(self):
        
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
        
        
    
    
from Robot import *

uid = "0947e717-02a1-4d83-9470-a941b6e8ed07"
s = "INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3"
state = "STATE20ac18ab-6d18-450e-94af-bee53fdc8fcaIS2;3CELLS:1[2]12'4,2[2]15'2,3[1]33'6;4MOVES:1<5[2]@232'>6[2]@488'>3[1]@4330'2,1<10[1]@2241'3"

c = Robot(uid)
c.initialiserMatch(s)
terrain = c.getTerrain()
for cellule in terrain.getCellules().values():
    cellule.setAttaque( 5 )
    cellule.setCouleurJoueur( c.getMaCouleur() )
    break


s=c.strategie
s = StrategieNormale(c)

s.decider()