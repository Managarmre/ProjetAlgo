import Strategie as st
import Mouvement as mv
import Lien as li
import logging
import random
import math
import functools 
import operator 

import StrategieNormale as stn



class StrategiePrevision( stn.StrategieNormale ):
    
    def __init__( self, robot ):
        stn.StrategieNormale.__init__( self, robot )


    def envoyerUnitesAttaquantes( self, terrain, composante, mesCellules ):

        mouvements = [] 
        a_envoyer=0
        maCouleur = self.getRobot().getMaCouleur()
        attaquantes = mesCellules[ "attaquantes" ]
        
        #
        #   pour l'instant, pas de distinction entre les attaquants
        # 
        #
        for attaquante in attaquantes:
    
            # stratégie applicable pour les planètes attaquantes safe
            # ici on regarde si une planète voisine est sur le point de se faire prendre
            # si c'est le cas on entre en stratégie "prise de planète"
            
            # initialisation de variables
            dist_mini=-1
            cout_mini=-1
            couleur=-1
            # pour chaque voisin on récupère le cout de la cellule et sa distance
            for ennemi in attaquante.getVoisinsEnnemis():
                
                # si la planète est sur le point de se faire prendre et que les vars sont encore initialisées
                if self.getPriseCellule(ennemi) and dist_mini==-1:
                    # on récupère ses coordonnées et son coût (-cout_cellule => pour le remettre en positif)
                    cout_mini=-self.getCoutCellule(ennemi)
                    dist_mini=self.getRobot().getTerrain().getLien(li.Lien.hachage(attaquante,ennemi)).getDistance()
                    couleur=ennemi.getCouleurJoueur()
                    cellule_cible=ennemi
                # sinon on compare les distances
                # si la distance de la cellule est plus petite alors on récupère ses coordonnées et son coût
                # on privilégie la distance
                elif (self.getRobot().getTerrain().getLien(li.Lien.hachage(attaquante,ennemi)).getDistance()<dist_mini and self.getPriseCellule(ennemi) ):
                    dist_mini=self.getRobot().getTerrain().getLien(li.Lien.hachage(attaquante,ennemi)).getDistance()
                    cout_mini=-self.getCoutCellule(ennemi)
                    couleur=ennemi.getCouleurJoueur()
                    cellule_ciblee=ennemi
                # si deux planètes qui vont se faire prendre sont à la même distance, on compare leur cout
                # on récupère le cout de la cellule la moins couteuse (pas besoin pour la distance car inchangée)
                elif (self.getRobot().getTerrain().getLien(li.Lien.hachage(attaquante,ennemi)).getDistance()==dist_mini and (-self.getCoutCellule(ennemi))<cout_mini and self.getPriseCellule(ennemi) ):
                    cout_mini=-self.getCoutCellule(ennemi)
                    couleur=ennemi.getCouleurJoueur()
                    cellule_cible=ennemi
            logging.info( "{exce} et dist mini {dist_mini} ".format(exce=attaquante.getAttaque(),dist_mini=dist_mini) ) 
            # Si on a trouvé un planète dans ce cas là
            if dist_mini!=-1 and attaquante.getAttaque()>cout_mini:
                logging.info( "Stratégie Prévision" )
                # on récupère les liens de la cellule
                for lien in cellule_cible.getLiens():
                    # on regarde le temps (temps_impact) avant que la planète soit prise 
                    # on récupère le temps le plus grand
                    temps_impact=-1
                    for mouvement in lien.getMouvementVersCellule(cellule_cible):
                        temps_mouvement=mouvement.getTempsRestant()
                        if not (mouvement.aPourCouleur(couleur) and mouvement.aPourCouleur(maCouleur)) and temps_impact<temps_mouvement:
                           temps_impact=temps_mouvement
                    # on compare ce temps avec le temps que nos troupes vont mettre pour atteindre la planète cible (dist_mini)
                    # si dist_mini > Temps_impact
                    if temps_impact<dist_mini and attaquante.getAttaque()>cout_mini:
                        # on envoie nos troupes pour prendre la planète
                        
                        #j'envoie tout
                        a_envoyer=attaquante.getAttaque()
                        
                        # on envoie le nombre de troupes attaquantes + 10%
                        #a_envoyer=cout_mini+(cout_mini*10//100)
                        #if a_envoyer>attaquante.getAttaque() or a_envoyer==0:
                        #    a_envoyer=attaquante.getAttaque()
                            

            elif dist_mini==-1:  
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
                
        if a_envoyer!=0:
            logging.info( "{origin} attaque {cible} en envoyant {cell} et sur la planète il y a {total}!".format(origin=attaquante.getNumero(),cible=cellule_cible.getNumero(),cell=a_envoyer,total=attaquante.getAttaque()) )
    
            mon_mouvement = self.envoyerUnites( attaquante, cellule_cible, a_envoyer )
            mouvements.append( mon_mouvement )   
        return mouvements 


    # regarde si une planète est sur le point de se faire capturer par l'adversaire ou non
    # retourne un booleen
    def getPriseCellule( self, cellule ):
        
        maCouleur = self.getRobot().getMaCouleur()
        couleurCellule = cellule.getCouleurJoueur()
        
        coutTotal = cellule.getCout()
        
        for lien in cellule.getLiens():
            
            for mouvement in lien.getMouvementVersCellule( cellule ):
                # on ajoute le soutien
                if( mouvement.aPourCouleur(couleurCellule) ):
                    coutTotal += mouvement.getNbUnites()
                    
                # on soustrait les mouvements adverses
                else:
                    coutTotal -= mouvement.getNbUnites()

        return (coutTotal<=0)
