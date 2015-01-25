
# module permettant de manipuler des expressions régulières
import re

import logging
import threading

# le graphe modélisant le terrain
import Terrain as te
import Cellule as ce
import Lien as li
import Mouvement as mv

# on import les différentes stratégies utilisées
import StrategieAleatoire as alea
import StrategieAnalyse as ana
import StrategiePrevision as previ

from Exceptions import RobotException


"""
le robot du jeu, contiendra toutes les informations, et traduira les chaines que nous renverra le serveur
"""

class Robot:

    """
    La classe Robot. 
    Initialise le robot.
    A appeler dans la procédure 'register_pooo(uid)'
    
    :param uid: identifiant unique du robot que le serveur lui a attribué
    :type uid: str
    """

    def __init__( self, uid ):
        
        logging.info( "==== uid du robot : {chaine}".format(chaine=uid)  )
        
        self.uid = uid
        
        self.strategie = previ.StrategiePrevision( self )
        #self.strategie = ana.StrategieAnalyse( self )

        self.temps = 0
        self.joue = False

        self.mutex = threading.Semaphore(1)


    def analyseMessage( self, state ):
        """
        Décompose la chaine state passée en paramètre et agit en conséquence, exécute soit :
            - state of game
            - game over
            - end of game

        :param state: la chaine reçue, envoyée par le serveur, peut contenir un message STATE, GAMEOVER, ou ENDOFGAME 
        :type state: str
        """

        state_of_game = re.compile( r"\ASTATE(?P<id_match>.+)IS(?P<nbJoueurs>[0-9]+);(?P<nbCellules>[0-9]+)CELLS:?(?P<cellules>.*);(?P<nbMoves>[0-9]+)MOVES:?(?P<moves>.*)\Z"  )
        gameover = re.compile( r"\AGAMEOVER\[(?P<id_joueur>[0-9]+)\]IN(?P<id_match>.{8}-.{4}-.{4}-.{4}-.{12})\Z" ) 
        end_of_game = re.compile( r"\AENDOFGAME(?P<id_match>.{8}-.{4}-.{4}-.{4}-.{12})\Z" )
        
        logging.info( "==== chaine reçue : {chaine}".format(chaine=state) )
        
        if( state_of_game.match( state ) ):
            self.updateTerrain( state )
            
        elif( gameover.match( state ) ) :
            self.game_over( state )
            
        elif( end_of_game.match( state ) ):
            self.end_of_game()
            
        else:
            raise RobotException("je ne comprends pas ce que c'est, ne correspond pas au protocole : {quezako} ".format( quezako=state ) )
            

    def end_of_game(self):
        """
        Arrête le match en cours
        """
        self.partie_en_cours = False
        logging.info("==== arret du match")
    
    
    def game_over( self, state_game_over ):
        """
        L'un des participants du match a perdu, on analyse plus en détail la chaine reçue pour savoir si c'est ce robot qui ne peut plus jouer.

        :param state_game_over: chaine de caractère GAMEOVER envoyé par le serveur
        :type state_game_over: str
        """

        regex_GameOver = re.compile( r"\AGAMEOVER\[(?P<id_joueur>[0-9]+)\]IN(?P<id_match>.{8}-.{4}-.{4}-.{4}-.{12})\Z" ) 
        informations = regex_GameOver.match( state_game_over )
        
        id_joueur = int( informations.group("id_joueur") )
        
        logging.info( "==== gameover du joueur {id_joueur}".format(id_joueur=id_joueur) )
        
        if( self.getMaCouleur() == id_joueur ):
            
            if( self.getTerrain().getCellulesJoueur( self.getMaCouleur() ) ):
                logging.info( "==== gameover : j'ai gagné !!!" )
            
            else:
                logging.info( "==== gameover : j'ai perdu, je boude !" )
            
            self.peut_jouer = False
        
        self.nbJoueurs -= 1
        
        
    def initialiserMatch( self, init_string ):
        """
        Initialise le robot pour un match.
        A appeler dans la procédure 'init_pooo(init_string)'

        exemple : "INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3"
        
        :param init_string: chaîne regroupant les informations envoyées par le serveur pour l'initialisation d'un nouveau match, sous la forme INIT.
        :type init_string: str
        """

        logging.info( "==== initialisation"  )
        
        regex_init = re.compile( r"INIT(?P<id_match>.{8}-.{4}-.{4}-.{4}-.{12})TO(?P<nb_joueurs>[0-9]*)\[(?P<maCouleur>[0-9]*)\];(?P<vitesse>[0-9]*);(?P<nbCellules>[0-9]*)CELLS:(?P<cellules>([0-9]+\([0-9]+,[0-9]+\)'[0-9]+'[0-9]+'[0-9]+'I+,?)*);(?P<nbLines>[0-9]*)LINES:(?P<lignes>([0-9]+@[0-9]+OF[0-9]+,?)*)" )
        informations = regex_init.match( init_string )
        if( not informations ):
            raise Exception("la chaine entrée est invalide (ne correspond pas à la regex)")

        # on récupère autant d'informations que possible sur la chaine d'origine 
        self.vitesse = int( informations.group('vitesse') )
        self.id_match = informations.group('id_match')
        self.maCouleur = int( informations.group('maCouleur') )
        self.nbJoueursInitial = int( informations.group('nb_joueurs') )
        self.nbJoueurs = self.nbJoueursInitial 
        
        # création d'un terrain vide, que l'on remplira au fur et à mesure
        self.terrain = te.Terrain()

        nbCellules = informations.group("nbCellules")
        
        # on trouve toutes les correspondances au pattern correspondant à la description d'une cellule
        # et pour chaque correspondance, on en extrait les informations de la cellule
        regex_cellules = re.compile( r"[0-9]+\([0-9]+,[0-9]+\)'[0-9]+'[0-9]+'[0-9]+'I+" )
        regex_uneCellule = re.compile( r"(?P<id_cellule>[0-9]+)\((?P<x>[0-9]+),(?P<y>[0-9]+)\)'(?P<rayon>[0-9]+)'(?P<maxATT>[0-9]+)'(?P<maxDEF>[0-9]+)'(?P<production>I+)" )
        
        # on ne peut pas séparer ici pas un "," => donc on n'utilise pas re.split()
        for chaine in regex_cellules.findall( informations.group('cellules') ):

            ifs = regex_uneCellule.match( chaine )

            try:

                numero = int( ifs.group('id_cellule') )
                attaque, defense, couleurJoueur = 0, 0, -1    # cellule neutre, n'a ni attaque, ni defense
                attaqueMax = int( ifs.group('maxATT') )
                defenseMax = int( ifs.group('maxDEF') )
                production = len( ifs.group('production') )     # on compte le nombre de I
    
                x = int( ifs.group('x') )
                y = int( ifs.group('y') )
                rayon = int( ifs.group('rayon') )
    
                cellule = ce.Cellule( numero, attaque, defense, attaqueMax, defenseMax, production, couleurJoueur, x, y, rayon )
                self.terrain.ajouterCellule( cellule )
            
            except Exception as e:
                logging.info( "======== /!\ IMPOSSIBLE DE CREER UNE CELLULE (initialiserMatch) : " + e )


        nbLines = informations.group("nbLines")
        
        # on fait de même pour les liens entres les cellules
        regex_unLien = re.compile( r"(?P<id_cellule_u>[0-9]+)@(?P<distance>[0-9]+)OF(?P<id_cellule_v>[0-9]+)" )
        
        for chaine in re.split( "," , informations.group("lignes") ) :
            
            try:
            
                ifs = regex_unLien.match( chaine )
    
                numero_u = int( ifs.group('id_cellule_u') )
                numero_v = int( ifs.group('id_cellule_v') )
                distance = int( ifs.group('distance')     )
    
                lien = li.Lien( self.terrain.getCellule(numero_u) , self.terrain.getCellule(numero_v) , distance )
                self.terrain.ajouterLien( lien )
            
            except Exception as e:
                logging.info( "======== /!\ IMPOSSIBLE DE CREER LE LIEN : " + e )
             
        self.peut_jouer = True
        self.partie_en_cours = True
        
        pass


    def updateTerrain(self, state):
        """
        Met à jour les informations sur le terrain en fonction de la chaîne passée en paramètre
        
        exemple de chaine state
        state = "STATE20ac18ab-6d18-450e-94af-bee53fdc8fcaIS2;3CELLS:1[2]12'4,2[2]15'2,3[1]33'6;4MOVES:1<5[2]@232'>6[2]@488'>3[1]@4330'2,1<10[1]@2241'3"

        :param state: la chaîne envoyée par le serveur, de la forme STATE
        :type state: str
        """

        self.mutex.acquire()

        logging.info( "==== mise à jour du terrain"  )
        
        # on supprime tous les déplacements
        terrain = self.getTerrain()

        terrain.mouvements = []
        for numero,lien in terrain.getLiens().items():
            lien.clearAllMouvements()
        
        regex_state = re.compile( r"STATE(?P<id_match>.+)IS(?P<nbJoueurs>[0-9]+);(?P<nbCellules>[0-9]+)CELLS:?(?P<cellules>.*);(?P<nbMoves>[0-9]+)MOVES:?(?P<moves>.*)" )
        informations = regex_state.match( state )
        
        #récupération du nombre de joueurs en cours
        self.nbJoueurs = int( informations.group('nbJoueurs') )
        
        
        # on récupère les cellules modifiées
        regex_uneCellule = re.compile( r"(?P<id_cellule>[0-9]+)\[(?P<owner>-?[0-9]+)\](?P<offunits>[0-9]+)'(?P<defunits>[0-9]+)" )
        
        nbCellules = int( informations.group("nbCellules") )
        if( nbCellules > 0 ):
            for chaine in re.split( "," , informations.group("cellules") ) :
                 
                 ifs_cellule = regex_uneCellule.match( chaine )
                 
                 # maj de la cellule
                 cellule = self.getTerrain().getCellule(int (ifs_cellule.group( 'id_cellule' ) ))
                 cellule.setCouleur(int (ifs_cellule.group( 'owner' ) ))
                 cellule.setAttaque(int (ifs_cellule.group( 'offunits' ) ))
                 cellule.setDefense(int (ifs_cellule.group( 'defunits' ) ))
        
        # regex utilisées sur les liens et les mouvements
        regex_unLien = re.compile(r"(?P<id_cellule_u>[0-9]+)((?P<deplacements>.+)')+(?P<id_cellule_v>[0-9]+)")
        regex_unDeplacement = re.compile( r"(?P<direction>\<|\>)(?P<offunits>[0-9]+)\[(?P<owner>[0-9]+)\]@(?P<timestamp>[0-9]+)" )
          
        # parcours de tous les liens qui ont des déplacements 
        nbMoves = int( informations.group("nbMoves") )
        if( nbMoves > 0 ):
        
            for chaine_lien in re.split( ',' , informations.group( "moves" ) ):
                
                ifs_lien = regex_unLien.match ( chaine_lien )
                
                numero_cellule_1 = int( ifs_lien.group( 'id_cellule_u' ) )
                numero_cellule_2 = int( ifs_lien.group( 'id_cellule_v' ) )
                
                # on récupère les identifiants des cellules du lien
                cellule1 = self.getTerrain().getCellule( numero_cellule_1 )
                cellule2 = self.getTerrain().getCellule( numero_cellule_2 )
                
                lien = self.getTerrain().getLien( li.Lien.hachage(cellule1,cellule2) )
                
                # on récupère tous les mouvements sur le lien actuel
                for chaine_deplacement in re.split( "'", ifs_lien.group("deplacements") ) :
                    
                    ifs_deplacement = regex_unDeplacement.match( chaine_deplacement )
                    
                    couleurJoueur = int( ifs_deplacement.group("owner") )
                    nbUnites = int( ifs_deplacement.group("offunits") )
                    temps_depart = int( ifs_deplacement.group("timestamp") )
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
                    
                    # on calcule le temps réel restant avant que le mouvement n'arrive à destination
                    temps_actuel = self.getTemps()
                    distance = lien.getDistance() 
                    vitesse = self.getVitesse()
                    
                    mouvement = mv.Mouvement( depuis, vers, nbUnites, couleurJoueur, distance, vitesse, temps_depart, temps_actuel )
                    lien.ajouterMouvementVersCellule( vers, mouvement )
                    terrain.mouvements.append( mouvement )
        
        self.mutex.release()    
        pass


    def getDecisions(self):
        """
        Retourne la liste des décisions, chacune conforme au protocole du serveur. 
        Ces décisions sont prises selon la stratégie adoptée.
        
        exemple : [ '[0947e717-02a1-4d83-9470-a941b6e8ed07]100FROM0TO2', '[0947e717-02a1-4d83-9470-a941b6e8ed07]56FROM6TO4' ]

        :returns: la liste des décisions
        :rtype: List<str>
        """

        self.mutex.acquire()
        ordres = [ mouv.toOrder( self.getUID() ) for mouv in self.getStrategie().decider() ]
        self.mutex.release()
        return ordres


    def getUID(self):
        """
        Retourne l'identifiant du robot
        
        :returns: l'identifiant du robot
        :rtype: str
        """
        return self.uid


    def getIdMatch(self):
        """
        Retourne l'identifiant du match
        
        :returns: l'identifiant du match
        :rtype: str
        """
        return self.id_match


    def getVitesse(self):
        """
        Retourne la vitesse du match en cours
        
        :returns: la vitesse du match en cours
        :rtype: int
        """
        return self.vitesse
    

    def getMaCouleur(self):
        """
        Retourne la couleur du robot
        
        :return: la couleur du robot
        :rtype: int
        """
        return self.maCouleur


    def getTerrain(self):
        """
        Retourne le terrain du match en cours
        
        :return: le terrain du match en cours
        :rtype: Terrain
        """
        return self.terrain
        

    def getStrategie(self):
        """
        Retourne la stratégie du robot
        
        :returns: la stratégie du robot
        :rtype: Strategie
        """
        return self.strategie
    

    def getNbJoueurs(self):
        """
        Retourne le nombre de joueurs actuellement en train de jouer
        
        :returns: le nombre de joueurs pouvant encore jouer
        :rtype: int
        """
        return self.nbJoueurs
    

    def getNbJoueurInitial(self):
        """
        Retourne le nombre de joueurs initial
        
        :returns: le nombre de joueurs initial
        :rtype: int
        """
        return self.nbJoueursInitial


    def getTemps(self):
        """
        Retourne le temps actuel du jeu (fournie par le serveur)
        
        :return: le temps actuel du jeu
        :rtype: int
        """
        return self.temps


    def setTemps( self , temps ):
        """
        Modifie le temps actuel du jeu, c'est à dire la variable temps du Robot, 
        mais également touts les attributs temps_actuel des mouvements (modifiant ainsi le temps restant).
        
        :param temps: Le temps
        :type temps: int
        """
        self.mutex.acquire()
        self.temps = temps 

        for mouvement in self.terrain.mouvements :
            mouvement.setTempsActuel( temps )

        self.mutex.release()


    def setStrategie( self, strategie ):
        """
        Modifie la stratégie du robot
        
        :param strategie: la nouvelle stratégie du robot
        :type strategie: Strategie
        """
        self.strategie = strategie

        
    def partieEnCours(self):
        """
        Retourne vrai si une partie est en cours, faux sinon
        
        :returns: vrai si une partie est en cours, faux sinon
        :rtype: booleen
        """
        self.mutex.acquire()
        en_cours = self.partie_en_cours
        self.mutex.release()
        return en_cours
        

    def peutJouer(self):
        """
        Retourne vrai si le robot peut jouer, et si il ne peut plus jouer
        
        :returns: vrai si le robot a le droit de jouer, faux sinon
        :rtype: booleen
        """
        self.mutex.acquire()
        play = self.peut_jouer
        self.mutex.release()
        return play