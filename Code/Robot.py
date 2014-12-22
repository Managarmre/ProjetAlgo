
# module permettant de manipuler des expressions régulières
import re

import logging

# permet de générer l'aléatoire
import random

# le graphe modélisant le terrain
from Terrain import *
from Cellule import *
from Lien import *

# on import les différentes stratégies utilisées
from StrategieRandom import *
from StrategieNormale import *

class Robot:

    # initialise le robot (crée le robot)
    # à appeler dans la procédure 'register_pooo(uid)'
    # uid : (String) l'identifiant unique du robot que le serveur lui a attribué
    def __init__( self, uid ):
        
        self.uid = uid
        
        logging.info( "==== uid du robot : {chaine}".format(chaine=uid)  )
        
        self.strategie = StrategieNormale( self )
        #self.strategie = StrategieRandom( self )
        
        self.joue = False




    def analyseMessage( self, state ):
        
        end_of_game = re.compile( r"ENDOFGAME.*" )
        state_of_game = re.compile( r"STATE.*" )
        gameover = re.compile( r"GAMEOVER.*" ) 
        
        logging.info( "==== chaine reçue : {chaine}".format(chaine=state) )
        
        if( end_of_game.match( state ) ):
            self.end_of_game()
            
        elif( gameover.match(state) ) :
            self.game_over(state)
            
            
        elif( state_of_game.match( state ) ):
            self.updateTerrain(state)
            
        else:
            raise Exception("je ne comprend pas ce que c'est : {quezako} ".format( quezako=state ) )
            
            
    
    # arrête le match en cours 
    def end_of_game(self):
        self.joue = False
        logging.info("==== arret du match")
    
    
    
    def game_over( self, state_game_over ):
        
        regex_GameOver = re.compile( r"\AGAMEOVER\[(?P<id_joueur>[0-9]+)\](?P<id_match>.+)\Z" )
        informations = regex_GameOver.match( state_game_over )
        
        id_joueur = int( informations.group("id_joueur") )
        
        logging.info( "==== gameover du joueur {id_joueur}".format(id_joueur=id_joueur) )
        
        if( self.getMaCouleur() == id_joueur ):
            logging.info( "==== gameover : je ne joue plus" )
            self.joue = False
        
        self.nbJoueurs -= 1
        
        

    # initialise le robot pour un match
    # à appeler dans la procédure 'init_pooo(init_string)'
    # init_string : (String) chaine regroupant les informations envoyé par le serveur pour l'initialisation d'un nouveau match
    def initialiserMatch( self, init_string ):
        
        logging.info( "==== chaine d'initialisation reçu : {chaine}".format(chaine=init_string)  )
        
        regex_verifier = re.compile( r"\AINIT.{8}-.{4}-.{4}-.{4}-.{12}TO[0-9]*\[[0-9]*\];[0-9]*;[0-9]*CELLS:([0-9]+\([0-9]+,[0-9]+\)'[0-9]+'[0-9]+'[0-9]+'I+,?)*;[0-9]*LINES:([0-9]+@[0-9]+OF[0-9]+,?)*\Z" )
        if( not regex_verifier.match(init_string) ):
            raise Exception("la chaine entrée est invalide (ne correspond pas à la regex)")
            
            
        # on récupère autant d'informations que possible sur la chaine d'origine 
        regex_init = re.compile( r"INIT(?P<id_match>.+)TO(?P<nb_joueurs>[0-9]*)\[(?P<maCouleur>[0-9]*)\];(?P<vitesse>[0-9]*);(?P<nbCellules>[0-9]*)CELLS:(?P<cellules>.*);(?P<nbLines>[0-9]*)LINES:(?P<lignes>.*)" )
        informations = regex_init.match( init_string )


        self.vitesse = int( informations.group('vitesse') )
        self.id_match = informations.group('id_match')
        self.maCouleur = int( informations.group('maCouleur') )
        self.nbJoueursInitial = int( informations.group('nb_joueurs') )
        self.nbJoueurs = self.nbJoueursInitial 
        
        # création d'un terrain vide, que l'on remplira au fure et à mesure
        self.terrain = Terrain()

        nbCellules = informations.group("nbCellules")
        #logging.info( "==== création de {nb} cellules".format(nb=nbCellules)  )
        
        
        # on trouve toutes les correspondance au pattern correspondant à la description d'une cellule
        # et pour chaque correspondance, on en extraits les informations de la cellule
        regex_cellules = re.compile( r"[0-9]+\([0-9]+,[0-9]+\)'[0-9]+'[0-9]+'[0-9]+'I+" )
        regex_uneCellule = re.compile( r"(?P<id_cellule>[0-9]+)\((?P<x>[0-9]+),(?P<y>[0-9]+)\)'(?P<rayon>[0-9]+)'(?P<maxATT>[0-9]+)'(?P<maxDEF>[0-9]+)'(?P<production>I+)" )
        
        # on ne peut pas séparer ici pas un "," => donc on n'utilise pas re.split()
        for chaine in regex_cellules.findall( informations.group('cellules') ):

            ifs = regex_uneCellule.match( chaine )

            numero = int( ifs.group('id_cellule') )
            attaque, defense, couleurJoueur = 0, 0, -1    # cellule neutre, n'a ni attaque, ni defense
            attaqueMax = int( ifs.group('maxATT') )
            defenseMax = int( ifs.group('maxDEF') )
            production = len( ifs.group('production') )     # on compte le nombre de I

            x = int( ifs.group('x') )
            y = int( ifs.group('y') )
            rayon = int( ifs.group('rayon') )

            cellule = Cellule( numero, attaque, defense, attaqueMax, defenseMax, production, couleurJoueur, x, y, rayon )
            self.terrain.ajouterCellule( cellule )


        nbLines = informations.group("nbLines")
        #logging.info( "==== création de {nb} liens".format(nb=nbLines)  )
        
        
        # on fait de même pour les liens entres les cellules
        regex_unLien = re.compile( r"(?P<id_cellule_u>[0-9]+)@(?P<distance>[0-9]+)OF(?P<id_cellule_v>[0-9]+)" )
        
        for chaine in re.split( "," , informations.group("lignes") ) :
            
            ifs = regex_unLien.match( chaine )

            numero_u = int( ifs.group('id_cellule_u') )
            numero_v = int( ifs.group('id_cellule_v') )
            distance = int( ifs.group('distance')     )

            lien = Lien( self.terrain.getCellule(numero_u) , self.terrain.getCellule(numero_v) , distance )
            self.terrain.ajouterLien( lien )
                  
        self.joue = True
        
        pass


    

    #
    #
    #
    #
    # exemple de chaine state
    # state = "STATE20ac18ab-6d18-450e-94af-bee53fdc8fcaIS2;3CELLS:1[2]12'4,2[2]15'2,3[1]33'6;4MOVES:1<5[2]@232'>6[2]@488'>3[1]@4330'2,1<10[1]@2241'3"
    def updateTerrain(self, state):
        
        logging.info( "==> maj du terrain" )
        
        #logging.info( "==== chaine update reçu : {chaine}".format(chaine=state)  )
        
        #logging.info( "==== suppression des anciens mouvements"  )
        
        # on supprime tous les déplacements
        for numero,lien in self.getTerrain().getLiens().items():
            lien.clearAllMouvements()
        
        
        
        regex_state = re.compile( r"STATE(?P<id_match>.+)IS(?P<nbJoueurs>[0-9]+);(?P<nbCellules>[0-9]+)CELLS:?(?P<cellules>.*);(?P<nbMoves>[0-9]+)MOVES:?(?P<moves>.*)" )
        informations = regex_state.match( state )
        
        #récupération du nombre de joueurs en cours
        self.nbJoueurs = int( informations.group('nbJoueurs') )
        
        
        nbCellules = informations.group("nbCellules")
        #logging.info( "==== maj de {nb} cellules".format(nb=nbCellules)  )
        
        # on récupère les cellules modifiées
        regex_uneCellule = re.compile( r"(?P<id_cellule>[0-9]+)\[(?P<owner>-?[0-9]+)\](?P<offunits>[0-9]+)'(?P<defunits>[0-9]+)" )
        
        if( int( informations.group( "nbCellules" ) ) > 0 ):
            for chaine in re.split( "," , informations.group("cellules") ) :
                 
                 ifs_cellule = regex_uneCellule.match( chaine )
                 
                 # maj de la cellule
                 cellule = self.getTerrain().getCellule(int (ifs_cellule.group( 'id_cellule' ) ))
                 cellule.setCouleurJoueur(int (ifs_cellule.group( 'owner' ) ))
                 cellule.setAttaque(int (ifs_cellule.group( 'offunits' ) ))
                 cellule.setDefense(int (ifs_cellule.group( 'defunits' ) ))
        
        
        nbMoves = informations.group("nbMoves")
        #logging.info( "==== maj de {nb} mouvements".format(nb=nbMoves)  )
        
        # ======= regex sur les liens =======
        regex_unLien = re.compile(r"(?P<id_cellule_u>[0-9]+)((?P<deplacements>.+)')+(?P<id_cellule_v>[0-9]+)")

        # ======= regex sur les déplacements =======
        regex_unDeplacement = re.compile( r"(?P<direction>\<|\>)(?P<offunits>[0-9]+)\[(?P<owner>[0-9]+)\]@(?P<timestamp>[0-9]+)" )
          

        # parcourt de tous les liens qui ont des déplacements 
        if( int( informations.group( "nbMoves" ) ) > 0 ):
        
            for chaine_lien in re.split( ',' , informations.group( "moves" ) ):
                
                ifs_lien = regex_unLien.match ( chaine_lien )
                
                # on récupère les identifiants des cellules du lien
                cellule1 = self.getTerrain().getCellule( int( ifs_lien.group( 'id_cellule_u' ) ) )
                cellule2 = self.getTerrain().getCellule( int( ifs_lien.group( 'id_cellule_v' ) ) )
                
                # attention => peut lancer une exception...
                lien = self.getTerrain().getLien( Lien.hachage(cellule1,cellule2) )
                
                
                # on récupère tous les mouvements sur le lien actuel
                for chaine_deplacement in re.split( "'", ifs_lien.group("deplacements") ) :
                    
                    ifs_deplacement = regex_unDeplacement.match( chaine_deplacement )
                    
                    couleurJoueur = int( ifs_deplacement.group("owner") )
                    nbUnites = int( ifs_deplacement.group("offunits") )
                    trajet = int( ifs_deplacement.group("timestamp") )
                    direction = ifs_deplacement.group("direction") 
                    
                    
                    # on ajoute le mouvement de cellule1 vers cellule2 (donc ajout VERS cellule2 )
                    if( direction == ">" ):
                        depuis = cellule1
                        vers = cellule2
                    
                    # mouvement de cellule2 vers cellule1 ( donc ajout VERS cellule1 )
                    elif( direction == "<" ):
                        depuis = cellule2
                        vers = cellule1 
                    
                    else:
                        raise Exception( "la direction n'est pas bonne... : {d}".format( d=direction)  )
                    
                    mouvement = Mouvement( depuis, vers, nbUnites, couleurJoueur, trajet )
                    lien.ajouterMouvementVersCellule( vers, mouvement )
                
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
    
    # retourne le nombre de joueurs actuel
    def getNbJoueurs(self):
        return self.nbJoueurs
    
    # retourne le nombre de joueur initial
    def getNbJoueurInitial(self):
        return self.nbJoueursInitial

    # retourne vrai si une partie est en cours, faux sinon
    def partieEnCours(self):
        return self.joue