
from Strategie import *
from Mouvement import *

import logging

import math
import functools 
import operator 

class StrategieNormale( Strategie ):
    
    def __init__( self, robot ):
        Strategie.__init__( self, robot )
        
        
    # liste1 - liste2 : totu ce qui est présent dans liste1 mais pas dans liste2
    def difference_liste( liste1, liste2 ):
        return [ val for val in liste1 if val not in liste2 ]
        
        
        
    def decider(self):
        
        terrain = self.getRobot().getTerrain()
        
        for composante in terrain.getSousGraphe( self.getMesCellules() ).getComposantesConnexes() :
            
            # self.getMesCellules() 
            # revient au même, car on prend le sous graphe ne contenant que mes cellules (au dessus)
            mesCellules = composante.getCellules().values()
            
            productrices = self.getCellulesProductrices( mesCellules )
            attaquantes = self.getCellulesAttaquantes( mesCellules, productrices )
            
            semi_productrices = self.getSemiProductrices( productrices, attaquantes )
            full_productrices = self.getFullProductrices( productrices , semi_productrices )
            
            attaquantes_en_danger = self.getAttaquantesEnDanger( attaquantes )
            attaquantes_en_surete = self.getAttaquantesEnSurete( attaquantes , attaquantes_en_danger )
            
            logging.info( "mes cellules : {cell} ".format(cell=mesCellules) )
            logging.info( "cellules attaquantes : {cell} ".format(cell=attaquantes) )
            logging.info( "cellules productrices : {cell} ".format(cell=productrices) )
            logging.info( "cellules semi-productrices : {cell} ".format(cell=semi_productrices) )
            logging.info( "cellules full-productrices : {cell} ".format(cell=full_productrices) )
            logging.info( "cellules attaquantes en dangées : {cell} ".format(cell=attaquantes_en_danger) )
            logging.info( "cellules attaquantes en suretées : {cell} ".format(cell=attaquantes_en_surete) )
            
            
            # 
            #   ====> appel de dijkstra quelque part....
            #
            
            
            mouvements = []
            
            
            for cellule in productrices :
                
                # utilisation du tableau de dijsktra ici
                vers = None
                #
                #
                #
                #
                vers = cellule.getLiens()[0].getOtherCellule( cellule )
                
                # si c'est une productrice
                # on envoi tout
                if( cellule in full_productrices ):
                    pourcentage = 1
                    
                # sinon, on n'envoi qu'un certain pourcentage
                else:
                    pourcentage = 80 / 100
                    
                
                nbUnites = math.ceil( cellule.getAttaque() * pourcentage )
                
                # si on a au moins 10% de la capacitee d'attaque de la cellule, on envoi
                if( cellule.getPourcentageAttaque() > 0.10 ):
                    mouvements.append( Mouvement( cellule, vers, nbUnites, cellule.getCouleurJoueur(), 0 ) )
                else:
                    pass
            
            #
            #   pour l'instant, pas de distinction entre les attaquants
            # 
            #
            for cellule in attaquantes:
                
                excedent = cellule.getExcedent()
                if( excedent > 0 ):
                    # il faut au moins envoyer 'excedent' unités
                    pass
                
                
                
                pass
            
            
            return mouvements
        
        
        
    
    def calculerCoutCellule( self, cellule ):
        
        cout = cellule.getCout()
        
        maCouleur = self.getRobot().getMaCouleur()
        
        
        for lien in cellule.getLiens():
            
            # les unités vers cette cellules
            for mouvement in lien.getMouvementVersCellule( cellule ):
                
                couleurMouvement = mouvement.getCouleurJoueur() 
                
                # mes unités
                if( couleurMouvement == maCouleur ):
                    cout -= mouvement.getNbUnites()
                
                # ses unités
                elif( couleurMouvement == cellule.getCouleurJoueur() ):
                    cout += mouvement.getNbUnites()
                
                # des unités d'un autre joueur
                else:
                    cout += mouvement.getNbUnites()
                
            
            # les unitées depuis cette cellule
            for mouvement in lien.getMouvementVersCellule( lien.getOtherCellule( cellule ) ):
                
                pass
            
            
            
        
        pass
    
        
        
    
    # retourne la liste des cellules m'appartenant
    def getMesCellules( self ):
        return self.getRobot().getTerrain().getCellulesJoueur( self.getRobot().getMaCouleur() )
        
    
    
    # retourne la liste de mes cellules productrices
    # une cellule est productrice si elle n'est relié à aucun ennemie
    # List<Cellule> mesCellules : lalites des cellules m'appartenant
    def getCellulesProductrices( self, mesCellules ):
        
        maCouleur = self.getRobot().getMaCouleur()
        
        # funtools.reduce() correspond à un sum, fold left (on replie la liste sur elle même)
        return [ cellule for cellule in mesCellules if functools.reduce( operator.and_, [ voisin.getCouleurJoueur() == maCouleur for voisin in cellule.getVoisins() ]  ) ]
    
    
    # retourne la liste de mes cellules attaquantes à partir de mes cellules productrices
    # (calculé par différente - )
    # une cellule est attaquante si elle est au moin relié à un ennemie
    # List<Cellule> mesCellules : la liste des cellules m'appartenant
    # List<Cellule> productrices : laliste de mes cellules productrices
    def getCellulesAttaquantes( self, mesCellules, productrices ):
        # correspond à : mesCellules - productrices
        return list( set(mesCellules) - set(productrices) )
        #return [ cellule for cellule in mesCellules if functools.reduce( operator.or_, [ voisin.getCouleurJoueur() != maCouleur for voisin in cellule.getVoisins() ]  ) ]
        
        
        
    # retourne la liste de mes cellules semi-productrices
    # une cellule est semi-prodictrice si c'est une cellule productrice relié à au moins une cellule attaquante
    def getSemiProductrices( self, productrices, attaquantes ):
        return [ cellule for cellule in productrices if functools.reduce( operator.or_ , [ voisin in attaquantes for voisin in cellule.getVoisins() ]  ) ]
    
    # retourne la liste de mes cellules full-productrices
    # une cellule est full-productrice si c'est un ecellule productrice qui n'est relié à aucune cellule attaquante
    def getFullProductrices( self, productrices, semi_productrices ):
        
        return list( set(productrices) - set(semi_productrices) )
        
        
    # retroune la liste de mes cellules attaquantes en danger
    # une cellule attaquante est en danger lorsqu'il y a des unités ennemie se dirigeant vers elle
    def getAttaquantesEnDanger( self, attaquantes ):
        
        maCouleur = self.getRobot().getMaCouleur()
        
        en_danger = {}
        for cellule in attaquantes:
            
            for lien in cellule.getLiens() :
                
                for mouvement in lien.getMouvementVersCellule( cellule ) :
                
                    if( mouvement.getCouleurJoueur() != maCouleur ):
                        en_danger.add(cellule)
                
                    
                ennemie = lien.getOtherCellule( cellule )
                if( ennemie.getAttaque() > cellule.getCout() ):
                    en_danger.add( cellule )
                
            
        return list( en_danger )
        
    
    # retourne la liste de mes cellules attaquantes en sureté
    def getAttaquantesEnSurete( self , attaquantes , attaquantes_en_dangers ):
        return list( set(attaquantes) - set(attaquantes_en_dangers) )