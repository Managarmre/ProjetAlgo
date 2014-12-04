
# module permettant de manipuler des expressions régulières
import re

# le graphe modélisant le terrain
from Terrain import *


class Robot:

    # initialise le robot (crée le robot)
    # à appeler dans la procédure 'register_pooo(uid)'
    # uid : (String) l'identifiant unique du robot que le serveur lui a attribué
    def __init__( self, uid ):
        self.uid = uid



    # initialise le robot pour un match
    # à appeler dans la procédure 'init_pooo(init_string)'
    # init_string : (String) chaine regroupant les informations envoyé par le serveur pour l'initialisation d'un nouveau match
    def initialiserMatch( self, init_string ):

        # on récupère autemps d'information qu epossible sur la chaine d'origine 
        regex_init = r"INIT(?P<id_match>.+)TO(?P<nb_joueurs>[0-9]*)\[(?P<maCouleur>[0-9]*)\];(?P<vitesse>[0-9]*);(?P<nbCellules>[0-9]*)CELLS:(?P<cellules>.*);(?P<nbLines>[0-9]*)LINES:(?P<lignes>.*)"
        informations = re.match( regex_init , init_string )

        self.vitesse = int( informations.group('vitesse') )
        self.id_match = informations.group('id_match')
        self.maCouleur = int( informations.group('maCouleur') )
        self.nbJoueurInitial = int( informations.group('nb_joueurs') )

        # création d'un terrain vide, que l'on remplira au fure et à mesure
        self.terrain = Terrain()
        #print( informations.groupdict() )


        # on trouve toutes les correspondance au pattern correspondant à la description d'une cellule
        # et pour chaque correspondance, on en extraits les informations de la cellule
        pattern_cellule = r"[0-9]+\([0-9]+,[0-9]+\)'[0-9]+'[0-9]+'[0-9]+'I+"
        regex_cellule = r"(?P<id_cellule>[0-9]+)\((?P<x>[0-9]+),(?P<y>[0-9]+)\)'(?P<rayon>[0-9]+)'(?P<maxATT>[0-9]+)'(?P<maxDEF>[0-9]+)'(?P<production>I+)"
        for chaine in re.findall( pattern_cellule , informations.group('cellules') ):
            
            ifs = re.match( regex_cellule , chaine )

            numero = int( ifs.group('id_cellule') )
            attaque, defense, couleurJoueur = 0, 0, 0    # cellule neutre, n'a ni attaque, ni defense
            attaqueMax = int( ifs.group('maxATT') )
            defenseMax = int( ifs.group('maxDEF') )
            production = len( ifs.group('production') )     # on compte le nombre de I

            x = int( ifs.group('x') )
            y = int( ifs.group('y') )
            rayon = int( ifs.group('rayon') )

            cellule = Cellule( numero, attaque, defense, attaqueMax, defenseMax, production, couleurJoueur, x, y, rayon )
            self.terrain.ajouterCellule( cellule )
            #print( informations_cellule.groupdict() )

        # on fait de même pour les liens entres les cellules
        pattern_lien = r"[0-9]+@[0-9]+OF[0-9]+"
        regex_lien = r"(?P<id_cellule_u>[0-9]+)@(?P<distance>[0-9]+)OF(?P<id_cellule_v>[0-9]+)"
        for chaine in re.findall( pattern_lien , informations.group('lignes') ):
            
            ifs = re.match( regex_lien , chaine )
            #print( ifs.groupdict() )
            
            numero_u = int( ifs.group('id_cellule_u') )
            numero_v = int( ifs.group('id_cellule_v') )
            distance = int( ifs.group('distance')     )

            self.terrain.ajouterLien( self.terrain.getCellule(numero_u) , self.terrain.getCellule(numero_v) , distance )
                    
        pass


    def updateTerrain(self, state):
        pass


    # ----- getters ----

    # retourne l'uid du robot (string)
    def getUID(self):
        return self.uid

    # retourne l'identifiant du match en cours (string)
    def getIdMatch(self):
        return self.id_match

    # retourne la vitesse du match en cours (entier)
    def getVitesse(self):
        return self.vitesse
    
    # retourne la couleur du robot (entier)
    def getMaCouleur(self):
        return self.maCouleur

    # retourne le terrain du match en cours (Terrain)
    def getTerrain(self):
        return self.terrain

    

