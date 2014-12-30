
from Strategie import *
from Mouvement import *
from Lien import *

import logging

import random
import math
import functools 
import operator 


class StrategieNormale( Strategie ):
    
    def __init__( self, robot ):
        Strategie.__init__( self, robot )
        
        
    
    
    def decider(self):
        
        terrain = self.getRobot().getTerrain()
        
        mouvements = []
        
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
            


            StrategieNormale.afficherCellulesLogging( "mes cellules" , mesCellules )
            StrategieNormale.afficherCellulesLogging( "cellules attaquantes" , attaquantes )
            StrategieNormale.afficherCellulesLogging( "cellules productrices" , productrices )
            StrategieNormale.afficherCellulesLogging( "cellules semi-productrices" , semi_productrices )
            StrategieNormale.afficherCellulesLogging( "cellules full-productrices" , full_productrices )
            StrategieNormale.afficherCellulesLogging( "cellules attaquantes en dangées" , attaquantes_en_danger )
            StrategieNormale.afficherCellulesLogging( "cellules attaquantes en suretées" , attaquantes_en_surete )

            
            # on envoie les cellules des productrices si on a au moins une cellule attaquante
            if( attaquantes ):
            
                for cellule in productrices :
                    
                    # si on a au moins 10% de la capacitee d'attaque de la cellule, on envoi
                    if( cellule.getPourcentageAttaque() > 0.10 ):
                    
                        # utilisation du tableau de dijsktra ici
                        if( attaquantes_en_danger ):
                            numero_vers = composante.getCheminVersCellulePlusProche( cellule , attaquantes_en_danger )[1]
                        else:
                            numero_vers = composante.getCheminVersCellulePlusProche( cellule , attaquantes )[1]
                            
                        vers = composante.getCellule( numero_vers )
                        
                        # si c'est une productrice
                        # on envoi tout
                        if( cellule in full_productrices ):
                            pourcentage = 1
                            
                        # sinon, on n'envoi qu'un certain pourcentage
                        else:
                            pourcentage = 80 / 100
                            
                        
                        nbUnites = math.ceil( cellule.getAttaque() * pourcentage )
                    
                        mouvements.append( Mouvement( cellule, vers, nbUnites, cellule.getCouleurJoueur(), 0 ) )
                        
                    else:
                        pass
            
            #
            #   pour l'instant, pas de distinction entre les attaquants
            # 
            #
            for cellule in attaquantes:
                
                
                #
                #  => recherche si pupute applicable ici
                # sinon
                
                
                # calcul de mon excédent
                excedent = cellule.getExcedent()

                # recherche de la cible    
                tableau_p = {}
                for ennemi in cellule.getVoisinsEnnemis() :
                    tableau_p.setdefault( self.indiceP(cellule,ennemi), [] ).append( ennemi.getNumero() )
                    # tablea_p[ self.indiceP(ennemi) ] = ennemi.getNumero()
                
                indice_p_max = max( tableau_p.keys() )
                
                cellules_possibles = tableau_p[ indice_p_max ]
                
                cellule_choisie = cellules_possibles[ random.randint( 0 , len(cellules_possibles)-1 ) ]
                vers = terrain.getCellule(cellule_choisie)
                
                # si je peux la prendre, je l'attaque
                # ===> !!!!!! ne prend pas encore en compte les mouvements sur les liens !!!!
                if( cellule.getAttaque() > vers.getCout() ):
                    
                    a_envoyer = excedent if vers.getCout() < excedent else vers.getCout()
                    logging.info( "j'attaque {cible} en envoyant {cell} !".format(cible=cellule_choisie,cell=a_envoyer) )
                    
                    mon_mouvement = Mouvement( cellule, vers, cellule.getAttaque(), cellule.getCouleurJoueur(), 0 )
                    mouvements.append( mon_mouvement )
                    terrain.getLien( Lien.hachage(vers,cellule) ).ajouterMouvementVersCellule( vers , mon_mouvement )

                else:
                    logging.info( "j'attend d'être assez grand pour l'attaquer" )
                    # on attend 
                    pass
                
                
            
        return mouvements
        
        
        
    #
    # ===> a terminer
    #
    
    # calcul l'indice p d'une cellule par rapport à la cellule d'origine voulant envoyer ses unitées
    # Cellule origine :
    # Cellule cellule : la cellule dont on veut calculer l'indice p
    def indiceP( self, origine, cellule ):
        
        cout = cellule.getCout()
        
        production = cellule.getProduction()
        
        nbVoisins = len( cellule.getVoisins() )
        
        distance = self.getRobot().getTerrain().getLien( Lien.hachage(origine,cellule) ).getDistance()
        
        return production / ( cout * nbVoisins * distance )
        
        """
        
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
        """
        
        
    

    ###### pour l'affichage
    def afficherCellulesLogging( message , cellules ):
        
        liste = [ cellule.getNumero() for cellule in cellules ]
        chaine = message + " : {liste}" 
        logging.info( chaine.format(liste=liste) )
        
        
    
    
    # ==============================================
    #   Fonctions permettant de récupérer mes 
    # cellules full-productrices, semi-productrices...
    # ==============================================
    
    # retourne la liste des cellules m'appartenant
    def getMesCellules( self ):
        return self.getRobot().getTerrain().getCellulesJoueur( self.getRobot().getMaCouleur() )
        
    
    
    # retourne la liste de mes cellules productrices
    # une cellule est productrice si elle n'est relié à aucun ennemie
    # List<Cellule> mesCellules : lalites des cellules m'appartenant
    def getCellulesProductrices( self, mesCellules ):
        
        maCouleur = self.getRobot().getMaCouleur()
        
        # funtools.reduce() correspond à un sum, fold left (on replie la liste sur elle même)
        # return [ cellule for cellule in mesCellules if functools.reduce( operator.and_, [ voisin.getCouleurJoueur() == maCouleur for voisin in cellule.getVoisins() ]  ) ]
        return [ cellule for cellule in mesCellules if all( [ voisin.getCouleurJoueur() == maCouleur for voisin in cellule.getVoisins() ] ) ]
    
    
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
        return [ cellule for cellule in productrices if any( [ voisin in attaquantes for voisin in cellule.getVoisins() ]  ) ]
    
    # retourne la liste de mes cellules full-productrices
    # une cellule est full-productrice si c'est un ecellule productrice qui n'est relié à aucune cellule attaquante
    def getFullProductrices( self, productrices, semi_productrices ):
        return list( set(productrices) - set(semi_productrices) )
        
        
    # retroune la liste de mes cellules attaquantes en danger
    # une cellule attaquante est en danger lorsqu'il y a des unités ennemie se dirigeant vers elle
    def getAttaquantesEnDanger( self, attaquantes ):
        
        maCouleur = self.getRobot().getMaCouleur()
        
        en_danger = set()
        for cellule in attaquantes:
            
            for lien in cellule.getLiens() :
                
                for mouvement in lien.getMouvementVersCellule( cellule ) :
                
                    if( mouvement.getCouleurJoueur() != maCouleur ):
                        en_danger.add(cellule)
                
                 
                autre_cellule = lien.getOtherCellule( cellule )
                if( autre_cellule.getAttaque() > cellule.getCout() and autre_cellule.getCouleurJoueur() != maCouleur and autre_cellule.getCouleurJoueur() != -1 ):
                    en_danger.add( cellule )
                
            
        return list( en_danger )
        
    
    # retourne la liste de mes cellules attaquantes en sureté
    def getAttaquantesEnSurete( self , attaquantes , attaquantes_en_dangers ):
        return list( set(attaquantes) - set(attaquantes_en_dangers) )