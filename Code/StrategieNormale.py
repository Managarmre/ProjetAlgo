
import Strategie as st
import Mouvement as mv
import Lien as li

import logging

import random
import math
import functools 
import operator 


class StrategieNormale( st.Strategie ):
    
    def __init__( self, robot ):
        st.Strategie.__init__( self, robot )
        
        
    
    def decider(self):
        
        terrain = self.getRobot().getTerrain()
        
        mouvements = []
        
        for composante in terrain.getSousGraphe( self.getMesCellules() ).getComposantesConnexes() :
            
            mesCellules = {}
            mesCellules[ "cellules" ] = composante.getCellules().values()
            mesCellules[ "productrices" ] = self.getCellulesProductrices( mesCellules[ "cellules" ] )
            mesCellules[ "attaquantes" ] = self.getCellulesAttaquantes( mesCellules[ "cellules" ] )
            mesCellules[ "attaquantesEnDanger" ] = self.getAttaquantesEnDanger( mesCellules[ "attaquantes" ] )
            mesCellules[ "attaquantesEnSurete" ] = self.getAttaquantesEnSurete( mesCellules[ "attaquantes" ] , mesCellules[ "attaquantesEnDanger" ]  )      
            
            StrategieNormale.afficherCellulesLogging( "cellules attaquantes" , mesCellules["attaquantes"] )
            """
            StrategieNormale.afficherCellulesLogging( "mes cellules" , mesCellules["cellules"] )
            StrategieNormale.afficherCellulesLogging( "cellules productrices" , mesCellules["productrices"] )
            StrategieNormale.afficherCellulesLogging( "cellules attaquantes en dangées" , mesCellules["attaquantesEnDanger"] )
            StrategieNormale.afficherCellulesLogging( "cellules attaquantes en suretées" , mesCellules["attaquantesEnSurete"] )
            """
            
            
            # on envoie les unités des productrices si on a au moins une cellule attaquante
            if( mesCellules[ "attaquantes" ] ):

                mouvements += self.envoyerUnitesProductrices( composante, mesCellules )


            mouvements += self.envoyerUnitesAttaquantes( terrain, composante, mesCellules )
                                        
        return mouvements
        

    def envoyerUnitesProductrices( self, composante, mesCellules ):

        mouvements = []
        productrices = mesCellules[ "productrices" ]

        for productrice in productrices :
                    
            # si on a au moins 10% de la capacitee d'attaque de la cellule, on envoi
            if( productrice.getPourcentageAttaque() > 0.10 ):
            
                # utilisation du tableau de dijsktra ici                
                destinations = mesCellules[ "attaquantesEnDanger"] if( mesCellules["attaquantesEnDanger"] ) else mesCellules["attaquantesEnSurete"]
                numero_vers = composante.getCheminVersCellulePlusProche( productrice , destinations )[1]
                    
                vers = composante.getCellule( numero_vers )
                
                nbUnites = productrice.getAttaque() 

                mouvement = self.envoyerUnites( productrice, vers, nbUnites )
                mouvements.append( mouvement )

            else:
                pass

        return mouvements



    def envoyerUnitesAttaquantes( self, terrain, composante, mesCellules ):

        mouvements = [] 
        attaquantes = mesCellules[ "attaquantes" ]
        
        #
        #   pour l'instant, pas de distinction entre les attaquants
        # 
        #
        for attaquante in attaquantes:
    
            logging.info( "Strategie Attaque" )
    
    
            # recherche de la cible    
            tableau_p = {}
            for ennemi in attaquante.getVoisinsEnnemis() :
                tableau_p.setdefault( self.indiceP(attaquante,ennemi), [] ).append( ennemi.getNumero() )
                # tableau_p[ self.indiceP(ennemi) ] = [ ennemi.getNumero() , ... ]
            
            indice_p_max = max( tableau_p.keys() )
            cellules_possibles = tableau_p[ indice_p_max ]
            
            num_cellule_choisie = cellules_possibles[ random.randint( 0 , len(cellules_possibles)-1 ) ]
            cellule_cible = terrain.getCellule(num_cellule_choisie)
    
            #
            # => si qu'un seul voisin ennemi, j'envoi tout sur lui ?
            #
            # sinon 
            
            cout_cellule = self.getCoutCellule( cellule_cible )
            excedent = attaquante.getExcedent()
            
            if( cout_cellule <= 0 ):
                
                if( excedent > 0 ):
                    a_envoyer = excedent
                else:
                    continue
            
            else:
                
                if( cout_cellule < excedent ):
                    a_envoyer = excedent
                
                elif( attaquante.getAttaque() < cout_cellule ):
                    
                    if( excedent > 0 ):
                        a_envoyer = excedent
                    else:
                        logging.info( "j'attends d'être assez grand pour l'attaquer" )
                        continue
                    
                else:
                    a_envoyer = cout_cellule
                
            logging.info( "{exce} {cout_cell} ".format(exce=excedent,cout_cell=cout_cellule) ) 
            logging.info( "{origin} attaque {cible} en envoyant {cell} !".format(origin=attaquante.getNumero(),cible=num_cellule_choisie,cell=a_envoyer) )
    
            mon_mouvement = self.envoyerUnites( attaquante, cellule_cible, a_envoyer )
            mouvements.append( mon_mouvement )
            
        return mouvements 


    # calcul l'indice p d'une cellule par rapport à la cellule d'origine voulant envoyer ses unitées
    # Cellule origine :
    # Cellule cellule : la cellule dont on veut calculer l'indice p
    def indiceP( self, origine, cellule ):
        
        cout = self.getCoutCellule( cellule )
        cout = 1 if cout == 0 else cout        # pour éviter une division par 0
        
        production = cellule.getProduction()
        
        nbVoisins = len( cellule.getVoisins() )
        
        distance = self.getRobot().getTerrain().getLienEntreCellules( origine, cellule ).getDistance()
        
        return production / ( cout * nbVoisins * distance )
    
    
    # calcul le nombre d'unités que l'on doit envoyer sur une cellule ennemie afin de la capturer
    # retourne un entier
    def getCoutCellule( self, cellule ):
        
        maCouleur = self.getRobot().getMaCouleur()
        couleurCellule = cellule.getCouleurJoueur()
        
        coutTotal = cellule.getCout()
        
        for lien in cellule.getLiens():
            
            cellule_adjacente = lien.getOtherCellule(cellule)
            
            for mouvement in lien.getMouvementVersCellule( cellule ):
                
                couleurMouvement = mouvement.getCouleurJoueur()
                
                if( mouvement.aPourCouleur(couleurCellule) ):
                    coutTotal += mouvement.getNbUnites()
                    
                elif( mouvement.aPourCouleur(maCouleur) ):
                    coutTotal -= mouvement.getNbUnites()
                    
                # cas ou plus de deux joueurs, incertain !!
                else:
                    coutTotal -= mouvement.getNbUnites()
            
            # si c'est une de mes cellules
            if( cellule_adjacente.aPourCouleur(maCouleur) ):
            
                for mouvement in lien.getMouvementVersCellule( cellule_adjacente ):
                    
                    # si ce n'est pas l'un de mes mouvement, cela augmente le coût
                    if( not mouvement.aPourCouleur(maCouleur) ):
                        coutTotal += mouvement.getNbUnites()
        
        return coutTotal + 5




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
        return [ cellule for cellule in mesCellules if all( [ voisin.getCouleurJoueur() == maCouleur for voisin in cellule.getVoisins() ] ) ]
    
    
    # retourne la liste de mes cellules attaquantes à partir de mes cellules productrices
    # (calculé par différente - )
    # une cellule est attaquante si elle est au moin relié à un ennemie
    # List<Cellule> mesCellules : la liste des cellules m'appartenant
    # List<Cellule> productrices : laliste de mes cellules productrices
    def getCellulesAttaquantes( self, mesCellules ):
        # correspond à : mesCellules - productrices
        #return list( set(mesCellules) - set(productrices) )

        maCouleur = self.getRobot().getMaCouleur()
        return [ cellule for cellule in mesCellules if any( [ voisin.getCouleurJoueur() != maCouleur for voisin in cellule.getVoisins() ] ) ]
    
        
        
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
                if( autre_cellule.getAttaque() > cellule.getCout() and not autre_cellule.aPourCouleur(maCouleur) and not autre_cellule.aPourCouleur(-1) ):
                    en_danger.add( cellule )
                
            
        return list( en_danger )
        
    
    # retourne la liste de mes cellules attaquantes en sureté
    def getAttaquantesEnSurete( self , attaquantes , attaquantes_en_dangers ):
        return list( set(attaquantes) - set(attaquantes_en_dangers) )