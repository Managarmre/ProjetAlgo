import Strategie as st
import Mouvement as mv
import Lien as li
import logging
import random
import math

import StrategieAnalyse as ana



class StrategiePrevision( ana.StrategieAnalyse ):
    """
    Cette stratégie est une surcouche de la stratégie Analyse.
    Elle essaie de prendre les cellules au bon moment, afin de subir le moins de pertes possible

    """
    
    def __init__( self, robot ):
        """
        Constructeur de la classe StrategiePrevision
        """
        ana.StrategieAnalyse.__init__( self, robot )


    def determinerCible( self, attaquante ):
        """
        Dértermine la cible d'une cellule attaquante 



        :param :class:'Cellule' attaquante: la cellule attaquante cherchant une cible
        :returns: la cellule cible
        :rtype: :class:'Cellule'
        """

        robot = self.getRobot()
        terrain = robot.getTerrain()           
        tableau_p = {}  # tableau contenant les indices P des cellules voisines ennemies

        # initialisation de variables pour la stratégie prévision
        dist_ennemi_cible = float("inf")        # distance à l'infini !
        cout_ennemi_cible = float("inf")
        ennemi_va_etre_pris = False

       
        # pour chaque voisin on récupère le cout de la cellule et sa distance
        for ennemi in attaquante.getVoisinsEnnemis():

            # stratégie analyse
            tableau_p.setdefault( self.indiceP(attaquante,ennemi), [] ).append( ennemi )    # calcul indice P de l'ennemi

            # cas stratégie prévision
            lien = terrain.getLienEntreCellules( attaquante , ennemi )
            distance_ennemi_actuel = lien.getDistance()
            cout_ennemi_actuel = self.getCoutCellule( ennemi )    # le nombre d'unités que me coutera la cellule ennemi

            # si l'ennemi va être pris, mais pas par moi
            if( ennemi.vaEtrePrise() and cout_ennemi_actuel > 0 ):
                
                # si cet ennemi est plus proche, ou si il est moins couteux
                if( distance_ennemi_actuel < dist_ennemi_cible or ( distance_ennemi_actuel == dist_ennemi_cible and cout_ennemi_cible < cout_ennemi_actuel ) ): 
                    ennemi_va_etre_pris = True
                    cout_ennemi_cible = cout_ennemi_actuel
                    dist_ennemi_cible = distance_ennemi_actuel
                    cellule_cible = ennemi
                
                    logging.info( "planète {numero} a {exce} et dist de la cible {dist_mini} ".format(numero=attaquante.getNumero(),exce=attaquante.getAttaque(),dist_mini=dist_ennemi_cible) ) 
        

        # Si un ennemi va être pris et que je peux le prendre
        if ennemi_va_etre_pris and attaquante.getAttaque() > cout_ennemi_cible:

            logging.info( "Stratégie Prévision" )

            # on prend le temps restant le plus grand => le temps d'impact
            temps_impact = -1
            for mouvement in cellule_cible.getMouvementsVersCellule() :
                temps_mouvement = mouvement.getTempsRestant()
                temps_impact = temps_mouvement if temps_mouvement > temps_impact else temps_impact

            
            allies = attaquante.getVoisinsAllies() 
            # on compare ce temps avec le temps que nos troupes vont mettre pour atteindre la planète cible (dist_mini)
            # si dist_mini > Temps_impact
            if temps_impact < dist_ennemi_cible :
                # on envoie nos troupes pour prendre la planète

                return cellule_cible

                """
                # on envoie 10% de troupes en plus
                a_envoyer=int(cout_mini+(cout_mini*10//100))
                if a_envoyer>attaquante.getAttaque() or a_envoyer==0:
                    a_envoyer=attaquante.getAttaque()
                """
            elif( allies ):
                # on doit attendre avant d'attaquer, on envoie notre excédent vers une cellule alliée si possible
                return allies[0]
            else:
                # si on a pas d'alliés autour, on est cuit
                return None


        else:  
            logging.info( "Strategie Attaque" )

            indice_p_max = max( tableau_p.keys() )
            cellules_possibles = tableau_p[ indice_p_max ]
            
            cellule_cible = cellules_possibles[ random.randint( 0 , len(cellules_possibles)-1 ) ]
            
            return cellule_cible

