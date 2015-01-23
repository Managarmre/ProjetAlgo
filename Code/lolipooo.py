# -*- coding: utf-8 -*-


"""Robot-joueur de Pooo
    
    Le module fournit les fonctions suivantes :
        register_pooo(uid)
        init_pooo(init_string)
        play_pooo()
        
"""

__version__='0.1'
 

## chargement de l'interface de communication avec le serveur
import poooc

# mieux que des print partout
import logging

# pour faire de l'introspection
import inspect
import time

import threading

# notre robot
from Robot import *
from Graphique import *

#import tkinter as tk

cheshire = None


def register_pooo(uid):
    """Inscrit un joueur et initialise le robot pour la compétition

        :param uid: identifiant utilisateur
        :type uid:  chaîne de caractères str(UUID) 
        
        :Example:
        
        "0947e717-02a1-4d83-9470-a941b6e8ed07"

    """
    global cheshire
    logging.info('[register_pooo] Bot {} registered'.format(uid))
    logging.info( "-- Initialisation du robot --" )
    
    cheshire = Robot( uid )
    
    
 
def init_pooo(init_string):
    """Initialise le robot pour un match
        
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


    """graphique = Graphique( cheshire )
    graphique.dessinerLiens()
    graphique.dessinerCellules()
    """
    thread_updateTime = threading.Thread( target=updateTime, args=(cheshire,) )
    thread_updateGame = threading.Thread( target=updateGame, args=(cheshire,) )
    thread_sendDecisions = threading.Thread( target=sendDecisions, args=(cheshire,) )
    #thread_graphique = threading.Thread( target=creerGraphique, args=(graphique,) )

    thread_updateTime.start()
    thread_updateGame.start()
    thread_sendDecisions.start()
    #thread_graphique.start()

    #graphique.fenetre.mainloop()

    thread_updateTime.join()
    thread_updateGame.join()
    thread_sendDecisions.join()


    
    
    """
    
    logging.info( "==> demande de l'état du jeu initial" )
    
    
    while ( cheshire.partieEnCours() ):
         
        logging.info( "==> demande de l'état du jeu" )
        
        
        t1 = time.time()
        
        temps = poooc.etime()
        
        t2 = time.time()
        
        state = poooc.state_on_update()   # bloquant
        
        t3 = time.time()
        
        logging.info( "==> temps du jeu: {t}".format(t=temps) )
        logging.info( "==> analyse de la réponse serveur" )
        
        t4 = time.time()
        cheshire.setTemps( temps )
        
        try: 
            cheshire.analyseMessage(state)
            
            t5 = time.time()
            t6 = 0
            
            if( cheshire.peutJouer() ):
            
                logging.info( "==> prise de décision" )
                decisions = cheshire.getDecisions()
                
                t6 = time.time()
                
                logging.info( "==> envoie des décisions au serveur" )
                logging.info( decisions )
                
                for decision in decisions:
                    poooc.order( decision )
                    time.sleep(0.2)
                    
            else:
                logging.info( "==== je n'ai plus le droit de jouer" )
        
            logging.info( "etime() {t}".format( t=(t2-t1)*1000 ) )
            logging.info( "state_on_update() {t}".format( t=(t3-t2)*1000 ) )
            logging.info( "loggings() {t}".format( t=(t4-t3)*1000 ) )
            logging.info( "analyseMessage() {t}".format( t=(t5-t4)*1000 ) )
            logging.info( "getDecisions() {t}".format( t=(t6-t5)*1000 ) )
        
        except Exception as e:
            logging.info( e )
         
    logging.info( "==> partie finie" )
    logging.info('>>> Exit play_pooo function')    
           
    """

    pass
    




def updateTime( robot ):
    
    while( robot.partieEnCours() ):
        
        temps = poooc.etime()
        
        # logging.info( "==> temps du jeu: {t}".format(t=temps) )

        try:
            robot.setTemps( temps )
        
        except Exception as e:
            logging.info( e )
                
        time.sleep( 0.05 )
        
    pass


def updateGame( robot ):
    
    while( robot.partieEnCours() ):

        state = poooc.state_on_update()

        try:
            robot.analyseMessage( state )

        except Exception as e:
            logging.info( e )

        time.sleep( 0.05 )

    pass
        
        
def sendDecisions( robot ):

    while( robot.peutJouer() ):

        try: 
            ordres = robot.getDecisions()

            for ordre in ordres :

                poooc.order( ordre )

                time.sleep( 0.02 )

        except Exception as e:
            logging.info( e )

        time.sleep( 0.2 )

    pass    


"""def creerGraphique( graphique ):

    while( graphique.robot.partieEnCours() ):

        graphique.redessinerCellules()
        graphique.dessinerMouvements() 

        time.sleep( 0.1 )

    graphique.fenetre.quit()
"""

    

