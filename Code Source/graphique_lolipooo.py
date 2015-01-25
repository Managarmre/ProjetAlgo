# -*- coding: utf-8 -*-


"""
    Robot-joueur de Pooo
    
    Le module fournit les fonctions suivantes :
        register_pooo(uid)
        init_pooo(init_string)
        play_pooo()
        
"""
 

## chargement de l'interface de communication avec le serveur
import poooc

# mieux que des print partout
import logging

# pour faire de l'introspection
import inspect
import time

import threading
#import functools

# notre robot
from Robot import *
from Graphique import *


cheshire = None




def register_pooo(uid):
    """
    Inscrit un joueur et initialise le robot pour la compétition

    :param uid: identifiant utilisateur
    :type uid:  chaîne de caractères str(UUID) 
        
    :Example:
       
    "0947e717-02a1-4d83-9470-a941b6e8ed07"
    """
    global cheshire
    logging.info('[register_pooo] Bot {} registered'.format(uid))
    logging.info( "-- Initialisation du robot --" )
    
    cheshire = Robot( uid )
    #cheshire.setStrategie( .... )
    
    
 
def init_pooo(init_string):
    """
    Initialise le robot pour un match
        
    :param init_string: instruction du protocole de communication de Pooo (voire ci-dessous)
    :type init_string: chaîne de caractères (utf-8 string)
       
       
    INIT<matchid>TO<#players>[<me>];<speed>;\
    <#cells>CELLS:<cellid>(<x>,<y>)'<radius>'<offsize>'<defsize>'<prod>,...;\
    <#lines>LINES:<cellid>@<dist>OF<cellid>,...

    <me> et <owner> désignent des numéros de 'couleur' attribués aux joueurs. La couleur 0 est le neutre.
    le neutre n'est pas compté dans l'effectif de joueurs (<#players>).
    '...' signifie que l'on répète la séquence précédente autant de fois qu'il y a de cellules (ou d'arêtes).
    0CELLS ou 0LINES sont des cas particuliers sans suffixe.
    <dist> est la distance qui sépare 2 cellules, exprimée en... millisecondes !
    /!\ attention: un match à vitesse x2 réduit de moitié le temps effectif de trajet d'une cellule à l'autre par rapport à l'indication <dist>.
    De manière générale temps_de_trajet=<dist>/vitesse (division entière).
       
    :Example:
        
    "INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3"    
    """
    logging.info('[init_pooo] Game init: {!r}'.format(init_string))
    
    global cheshire
    
    logging.info( "-- Initialisation d'un match --" )
    
    if( cheshire ):
        cheshire.initialiserMatch( init_string )
    else:
        raise Exception("cheshire doit être initialisé avant d'initialiser un match !")
    


def play_pooo():
    """Active le robot-joueur
    
    """
    
    global cheshire

    if( not cheshire ):
        raise Exception("vous devez exécuter les fonctions register_pooo() et init_pooo() avant !")
    
    if( not cheshire.partieEnCours() ):
        raise Exception("vous devez exécuter la fonction init_pooo() pour initialiser un match avant !")
    
    
    logging.info('Entering play_pooo fonction from {} module...'.format(inspect.currentframe().f_back.f_code.co_filename))

    
    graphique = Graphique( cheshire )
    graphique.dessinerCellules()
    graphique.dessinerLiens()
    

    thread_updateTime = threading.Thread( target=updateTime, args=(cheshire,) )
    thread_updateGame = threading.Thread( target=updateGame, args=(cheshire,) )
    thread_sendDecisions = threading.Thread( target=sendDecisions, args=(cheshire,) )
    thread_graphique = threading.Thread( target=updateGraphique, args=(graphique,) )
    
    thread_updateTime.start()
    thread_updateGame.start()
    thread_sendDecisions.start()
    thread_graphique.start()

    #graphique.canvas.after( 10, updateGraphique, args=(graphique,) )
    #graphique.canvas.after( 10, functools.partial(updateGraphique, graphique) )
    graphique.fenetre.mainloop()    # start application main loop, bloquant

    thread_updateTime.join()
    thread_updateGame.join()
    thread_sendDecisions.join()  
    thread_graphique.join()         # probleme ici

    pass
    


def updateGraphique( graphique ):
    """
    Permet la mise à jour automatique de l'interface graphique

    :param graphique: l'interface graphique
    :type graphique: Graphique
    """
    event = threading.Event()

    while( graphique.robot.partie_en_cours ):

        graphique.redessinerCellules()
        graphique.dessinerMouvements() 

        #time.sleep( 0.05 )
        event.wait( 0.05 )
        
    #graphique.fenetre.quit()
    graphique.canvas.after( 10, graphique.fenetre.destroy )
    
    #graphique.fenetre.destroy()     # probleme ici
    # détruit la fenêtre
    
    logging.info( "fenetre détruite dans update graphique" )

    #graphique.fenetre.quit()    # ferme la fenetre




def updateTime( robot ):
    """
    Permet la mise à jour automatique du temps.

    :param robot: le robot
    :type robot: Robot
    """

    event = threading.Event()

    while( robot.partieEnCours() ):
        
        temps = poooc.etime()
        
        # logging.info( "==> temps du jeu: {t}".format(t=temps) )

        try:
            robot.setTemps( temps )
        
        except Exception as e : 
            logging.info( e )
        

        #time.sleep( 0.02 )
        event.wait( 0.02 )

    pass


def updateGame( robot ):
    """
    Permet la mise à jour automatique de l'état du jeu (terrain...).

    :param robot: le robot
    :type robot: Robot
    """
    event = threading.Event()

    while( robot.partieEnCours() ):

        state = poooc.state_on_update()     # bloquant

        try:
            robot.analyseMessage( state )

        except Exception as e :
            logging.info( e )
        

        #time.sleep( 0.05 )
        event.wait( 0.02 )
    pass
        
        
def sendDecisions( robot ):
    """
    Permet l'envoi automatique des decisions au serveur.

    :param robot: le robot
    :type robot: Robot
    """
    event = threading.Event()

    while( robot.peutJouer() ):

        try: 
            ordres = robot.getDecisions()

            for ordre in ordres :
                poooc.order( ordre )

                #time.sleep( 0.02 )

        except Exception as e :
            logging.info( e )

        #time.sleep( 0.02 )
        event.wait( 0.02 )

    pass    


