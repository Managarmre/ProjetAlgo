
# module permettant de manipuler des expressions régulières
import re

# le graphe modélisant le terrain
from Terrain import *
from Cellule import *

# permet de générer l'aléatoire
import random

# on import les différentes stratégies utilisées
from StrategieRandom import *


class Robot:

    # initialise le robot (crée le robot)
    # à appeler dans la procédure 'register_pooo(uid)'
    # uid : (String) l'identifiant unique du robot que le serveur lui a attribué
    def __init__( self, uid ):
        self.uid = uid
        
        self.strategie = StrategieRandom( self )



    # initialise le robot pour un match
    # à appeler dans la procédure 'init_pooo(init_string)'
    # init_string : (String) chaine regroupant les informations envoyé par le serveur pour l'initialisation d'un nouveau match
    def initialiserMatch( self, init_string ):

        regex_verifier = re.compile( r"\AINIT.{8}-.{4}-.{4}-.{4}-.{12}TO[0-9]*\[[0-9]*\];[0-9]*;[0-9]*CELLS:([0-9]+\([0-9]+,[0-9]+\)'[0-9]+'[0-9]+'[0-9]+'I+,?)*;[0-9]*LINES:([0-9]+@[0-9]+OF[0-9]+,?)*\Z" )
        if( not regex_verifier.match(init_string) ):
            raise Exception("la chaine entrée est invalide (ne correspond pas à la regex)")
            
            
        # on récupère autant d'informations que possible sur la chaine d'origine 
        regex_init = re.compile( r"INIT(?P<id_match>.+)TO(?P<nb_joueurs>[0-9]*)\[(?P<maCouleur>[0-9]*)\];(?P<vitesse>[0-9]*);(?P<nbCellules>[0-9]*)CELLS:(?P<cellules>.*);(?P<nbLines>[0-9]*)LINES:(?P<lignes>.*)" )
        informations = regex_init.match( init_string )


        self.vitesse = int( informations.group('vitesse') )
        self.id_match = informations.group('id_match')
        self.maCouleur = int( informations.group('maCouleur') )
        self.nbJoueurInitial = int( informations.group('nb_joueurs') )

        # création d'un terrain vide, que l'on remplira au fure et à mesure
        self.terrain = Terrain()

        # on trouve toutes les correspondance au pattern correspondant à la description d'une cellule
        # et pour chaque correspondance, on en extraits les informations de la cellule
        regex_cellules = re.compile( r"[0-9]+\([0-9]+,[0-9]+\)'[0-9]+'[0-9]+'[0-9]+'I+" )
        regex_uneCellule = re.compile( r"(?P<id_cellule>[0-9]+)\((?P<x>[0-9]+),(?P<y>[0-9]+)\)'(?P<rayon>[0-9]+)'(?P<maxATT>[0-9]+)'(?P<maxDEF>[0-9]+)'(?P<production>I+)" )
        for chaine in regex_cellules.findall( informations.group('cellules') ):

            ifs = regex_uneCellule.match( chaine )

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
        regex_liens = re.compile( r"[0-9]+@[0-9]+OF[0-9]+" )
        regex_unLien = re.compile( r"(?P<id_cellule_u>[0-9]+)@(?P<distance>[0-9]+)OF(?P<id_cellule_v>[0-9]+)" )
        for chaine in regex_liens.findall( informations.group('lignes') ):
            
            ifs = regex_unLien.match( chaine )
            #print( ifs.groupdict() )
            
            numero_u = int( ifs.group('id_cellule_u') )
            numero_v = int( ifs.group('id_cellule_v') )
            distance = int( ifs.group('distance')     )

            self.terrain.ajouterLien( self.terrain.getCellule(numero_u) , self.terrain.getCellule(numero_v) , distance )
                    
        pass


    def updateTerrain(self, state):
        #exemple de chaine state
        #state = "STATE20ac18ab-6d18-450e-94af-bee53fdc8fcaIS2;3CELLS:1[2]12'4,2[2]15'2,3[1]33'6;4MOVES:1<5[2]@232'>6[2]@488'>3[1]@4330'2,1<10[1]@2241'3"
        regex_state = re.compile( r"STATE(?P<id_match>.+)IS(?P<nbJoueurs>[0-9]+);(?P<nbCellules>[0-9]*)CELLS:(?P<cellules>.*);(?P<nbMoves>[0-9]*)MOVES:(?P<moves>.*)" )
        informations = regex_state.match( state )
        #récupération du nombre de joueurs en cours
        self.nbJoueur = int( informations.group('nbJoueurs') )
        
        
        # on récupère le format des cellules
        regex_cellules = re.compile( r"[0-9]+\[[0-9]+\][0-9]+'[0-9]+" )
        regex_uneCellule = re.compile( r"(?P<id_cellule>[0-9]+)\[(?P<owner>[0-9]+)\](?P<offunits>[0-9]+)'(?P<defunits>[0-9]+)+" )
        
        for chaine in regex_cellules.findall( informations.group( 'cellules' ) ):
             
             ifs = regex_uneCellule.match( chaine )
             
             cellule = self.getTerrain().getCellule(int (ifs.group( 'id_cellule' ) ))
             cellule.setCouleurJoueur(int (ifs.group( 'owner' ) ))
             cellule.setAttaque(int (ifs.group( 'offunits' ) ))
             cellule.setDefense(int (ifs.group( 'defunits' ) ))
        
        regex_liens = re.compile(r"[0-9]+.*[0-9]+")
        regex_unLien = re.compile(r"(?P<id_cellule_u>[0-9]+(?P<deplacements>.+)(?P<id_cellule_v>[0-9]+)),+")
       
        #parcourt de tous les liens qui ont des déplacements 
        for chaine in regex_liens.findall( informations.group( 'moves' )):
            
            ifs = regex_unLien.match ( chaine )
            
            # on fait de même pour les déplacements entre les cellules
            regex_deplacement = re.compile( r"[0-9]+\<|\>[0-9]+\[[0-9]+\]\>|\<@[0-9]+" )
            regex_unDeplacement = re.compile( r"(?P<id_cellule_u>[0-9]+)(?P<direction>\<|\>)(?P<offunits>[0-9]+)\[(?P<owner>[0-9]+)\]@(?P<timestamp>[0-9]+)" )
            
            #pour chaque lien on parcourt la liste des déplacements en cours sur ce lien
            for chaine2 in regex_deplacement.findall( ifs.group( 'deplacements' )):
                
                ifs = regex_unDeplacement.match ( chaine2 )
                # on supprime les mouvements
                for numero,lien in self.getTerrain().getliens().items():
                    lien.clearAllMouvements()
                
                
                # on les recréé de nouveau 
                cellule1 = Cellule.getCellule(int (ifs.group( 'id_cellule_u' ) ) )
                cellule2 = Cellule.getCellule(int (ifs.group( 'id_cellule_v' ) ) )
                
                #on récupère le lien entre les 2 cellules
                id_lien = Lien.hashage(cellule1, cellule2)
                lienOk = None
                
                for numero, lien in self.getTerrain().getLiens().items():
                    if numero == id_lien:
                        lienOk = lien
                        
                        
                        
                
                
                # si la direction est de gauche à droite:
                if (ifs.group( 'direction' )) == ">":
                    # on créé le mouvement et on l'ajoute au lien
                    mvt = Mouvement(cellule1, cellule2, int ( ifs.group( 'offunits' )), int ( ifs.group( 'owner' )), int ( ifs.group( 'timestamp' )) )
                    lienOk.ajouterMouvementVersCellule(cellule1, mvt)
                    # si la direction est de droite à gauche
                elif (ifs.group( 'direction' )) == "<":
                    mvt = Mouvement(cellule2, cellule1, int ( ifs.group( 'offunits' )), int ( ifs.group( 'owner' )), int ( ifs.group( 'timestamp' )) )
                    lienOk.ajouterMouvementVersCellule(cellule1, mvt)
                else:
                    print( "Erreur, la direction indiquée est mauvaise" )


        pass


    # retourne la liste des decisions, chacune conforme au protocole du serveur
    def getDecisions(self):
        return [ mouv.toOrder( self.getUID() ) for mouv in self.getStrategie().decider() ]
    




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
        
    # retourne la stratégie du robot (une instance de la classe abstraite Strategie)
    def getStrategie(self):
        return self.strategie
    

