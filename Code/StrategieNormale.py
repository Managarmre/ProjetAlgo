
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
            
                for productrice in productrices :
                    
                    # si on a au moins 10% de la capacitee d'attaque de la cellule, on envoi
                    if( productrice.getPourcentageAttaque() > 0.10 ):
                    
                        # utilisation du tableau de dijsktra ici
                        if( attaquantes_en_danger ):
                            numero_vers = composante.getCheminVersCellulePlusProche( productrice , attaquantes_en_danger )[1]
                        else:
                            numero_vers = composante.getCheminVersCellulePlusProche( productrice , attaquantes )[1]
                            
                        vers = composante.getCellule( numero_vers )
                        
                        nbUnites = productrice.getAttaque() 
                    
                        lien = composante.getLien( li.Lien.hachage( productrice, vers ) )
                        mouvement = mv.Mouvement( productrice, vers, nbUnites, productrice.getCouleurJoueur(), lien.getDistance() )
                        mouvements.append( mouvement )
                        
                    else:
                        pass
            
            #
            #   pour l'instant, pas de distinction entre les attaquants
            # 
            #
            for attaquante in attaquantes:
                
 ########################################
 ########################################
 #### PUPUTE DEBUT
 ########################################
 ########################################
 
                #
                #  => recherche si pupute applicable ici
                # stratégie applicable pour les planètes attaquantes safe
                # ici on regarde si une planète voisine est sur le point de se faire prendre
                # si c'est le cas on entre en stratégie "prise de planète"
                
                # initialisation de variables
                dist_mini=False
                cout_mini=-1
                couleur=-1
                cellule=""
                # pour chaque voisin on récupère le cout de la cellule et sa distance
                for ennemi in attaquante.getVoisinsEnnemis():
                    cout_cellule=self.getCoutCellule(ennemi)
                    dist_cellule=self.getRobot().getTerrain().getLien(li.Lien.hachage(attaquante,ennemi)).getDistance()
                    # si c'est la première cellule que l'on regarde et qu'elle est sur le point de se faire prendre
                    # on récupère ses coordonnées et son coût (-cout_cellule => pour le remettre en positif)
                    if (not dist_mini and cout_cellule<=0):
                        cout_mini=-cout_cellule
                        dist_mini=dist_cellule
                        couleur=ennemi.getCouleurJoueur()
                        cellule=ennemi
                    # sinon on compare les distances
                    # si la distance de la cellule est plus petite alors on récupère ses coordonnées et son coût
                    # on privilégie la distance
                    elif (dist_cellule<dist_mini and cout_cellule<=0):
                        dist_mini=dist_cellule
                        cout_mini=-cout_cellule
                        couleur=ennemi.getCouleurJoueur()
                        cellule=ennemi
                    # si deux planètes qui vont se faire prendre sont à la même distance, on compare leur cout
                    # on récupère le cout de la cellule la moins couteuse (pas besoin pour la distance car inchangée)
                    elif (dist_cellule==dist_mini and (-cout_cellule)<cout_mini and cout_cellule<=0):
                        cout_mini=-cout_cellule
                        couleur=ennemi.getCouleurJoueur()
                        cellule=ennemi
                # Si on a trouvé un planète dans ce cas là
                if not (dist_mini==False):
                    logging.info( "\o/ _o/ \o_ \o/" )
                    # on récupère les liens de la cellule
                    for lien in cellule.getLiens():
                        # on regarde le temps (temps_impact) avant que la planète soit prise 
                        # on récupère le temps le plus grand
                        temps_impact=-1
                        for mouvement in lien.getMouvementVersCellule(cellule):
                            temps_mouvement=mouvement.temps_restant
                            if not (mouvement.aPourCouleur(couleur) and mouvement.aPourCouleur(maCouleur)) and temps_impact<temps_mouvement:
                               temps_impact=temps_mouvement
                        # on compare ce temps avec le temps que nos troupes vont mettre pour atteindre la planète cible (dist_mini)
                        # si dist_mini > Temps_impact
                        if temps_impact<dist_mini:
                            # on envoie nos troupes pour prendre la planète
                            # on envoie le nombre de troupes attaquantes + 10%
                            a_envoyer=int(cout_mini+(cout_mini*30//100))
                            if a_envoyer>attaquante.getAttaque():
                                a_envoyer=attaquante.getAttaque()
                            elif a_envoyer==0:
                                a_envoyer=int(attaquante.getAttaque()//3)
                            
                            logging.info( "{exce} {cout_cell} ".format(exce=a_envoyer,cout_cell=cout_mini) ) 
                            logging.info( "{origin} attaque {cible} en envoyant {cell} !".format(origin=attaquante.getNumero(),cible=cellule,cell=a_envoyer) )
                                
                            lien = terrain.getLien( li.Lien.hachage(cellule,attaquante) )
                            
                            mon_mouvement = mv.Mouvement( attaquante, cellule, a_envoyer, attaquante.getCouleurJoueur(), lien.getDistance() )
                            mouvements.append( mon_mouvement )
                            
                            lien.ajouterMouvementVersCellule( cellule , mon_mouvement )
                            attaquante.setAttaque( attaquante.getAttaque() - a_envoyer )
                            
                        # sinon on passe
                        else:
                            pass                 
        
 ########################################
 ########################################
 #### PUPUTE FIN
 ########################################
 ########################################    
                else:  
                    logging.info( "j'entre dans la mauvaise partie wesh" )
                    # sinon
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
                        
                    lien = terrain.getLien( li.Lien.hachage(cellule_cible,attaquante) )
                    
                    mon_mouvement = mv.Mouvement( attaquante, cellule_cible, a_envoyer, attaquante.getCouleurJoueur(), lien.getDistance() )
                    mouvements.append( mon_mouvement )
                    
                    lien.ajouterMouvementVersCellule( cellule_cible , mon_mouvement )
                    attaquante.setAttaque( attaquante.getAttaque() - a_envoyer )
                
                
                """
                # si je peux la prendre, je l'attaque
                cout_cellule = self.getCoutCellule(vers)
                if( attaquante.getAttaque() > cout_cellule ):
                    
                    # la cellule est déja en train d'être conquise/prise
                    if( cout_cellule <= 0 ):
                        
                        # si j'ai quand même de l'excédent, j'envoie quand même
                        if( excedent > 0 ):
                            a_envoyer = excedent
                        else:
                            continue
                    
                    # la cellule n'est pas en train d'être conquise    
                    else:
                        a_envoyer = cout_cellule if cout_cellule > excedent else excedent
                        
                    logging.info( "{exce} {cout_cell} ".format(exce=excedent,cout_cell=cout_cellule) )
                    logging.info( "{origin} attaque {cible} en envoyant {cell} !".format(origin=attaquante.getNumero(),cible=num_cellule_choisie,cell=a_envoyer) )
                    
                    lien = terrain.getLien( li.Lien.hachage(vers,attaquante) )
                    
                    mon_mouvement = mv.Mouvement( attaquante, vers, a_envoyer, attaquante.getCouleurJoueur(), lien.getDistance() )
                    mouvements.append( mon_mouvement )
                    
                    lien.ajouterMouvementVersCellule( vers , mon_mouvement )
                    attaquante.setAttaque( attaquante.getAttaque() - a_envoyer )
                    
                    

                else:
                    logging.info( "j'attend d'être assez grand pour l'attaquer" )
                    # on attend 
                    pass
                
                """
            
        return mouvements
        

    # calcul l'indice p d'une cellule par rapport à la cellule d'origine voulant envoyer ses unitées
    # Cellule origine :
    # Cellule cellule : la cellule dont on veut calculer l'indice p
    def indiceP( self, origine, cellule ):
        
        cout = self.getCoutCellule( cellule )
        cout = -1 if cout == 0 else cout        # pour éviter une division par 0
        
        production = cellule.getProduction()
        
        nbVoisins = len( cellule.getVoisins() )
        
        distance = self.getRobot().getTerrain().getLien( li.Lien.hachage(origine,cellule) ).getDistance()
        
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
    def getCellulesAttaquantes( self, mesCellules, productrices ):
        # correspond à : mesCellules - productrices
        return list( set(mesCellules) - set(productrices) )
        
        
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