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


    
    
    thread_updateTime = threading.Thread( target=updateTime, args=(cheshire,) )
    thread_updateGame = threading.Thread( target=updateGame, args=(cheshire,) )
    thread_sendDecisions = threading.Thread( target=sendDecisions, args=(cheshire,) )
    
    thread_updateTime.start()
    thread_updateGame.start()
    thread_sendDecisions.start()
    
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
        
        logging.info( "==> temps du jeu: {t}".format(t=temps) )

        robot.setTemps( temps )
        
        
        #
        #
        #
        
        time.sleep( 0.02 )
        
    pass


def updateGame( robot ):
    
    while( robot.partieEnCours() ):

        state = poooc.state_on_update()

        robot.analyseMessage( state )

        time.sleep( 0.02 )

    pass
        
        
def sendDecisions( robot ):

    while( robot.peutJouer() ):

        ordres = robot.getDecisions()

        for ordre in ordres :

            poooc.order( ordre )

            time.sleep( 0.02 )


        time.sleep( 0.2 )

    pass    


# test 

uid = "0947e717-02a1-4d83-9470-a941b6e8ed07"

init = "INITc71db0bc-9863-4d51-bd6f-459de3fafdb7TO2[1];2;7CELLS:0(0,0)'100'30'8'I,1(0,5)'100'30'8'I,2(5,0)'100'30'8'I,3(5,5)'200'30'8'II,4(5,10)'100'30'8'I,5(10,5)'100'30'8'I,6(10,10)'100'30'8'I;6LINES:0@4800OF1,0@4800OF2,2@4700OF3,3@4700OF4,4@4800OF6,5@4800OF6"
state =   "STATEc71db0bc-9863-4d51-bd6f-459de3fafdb7IS2;7CELLS:0[0]6'1,1[-1]6'0,2[-1]6'0,3[-1]12'0,4[-1]6'0,5[-1]6'0,6[1]6'1;0MOVES"

init_1 = "INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3"
state_1 = "STATE20ac18ab-6d18-450e-94af-bee53fdc8fcaIS2;3CELLS:1[2]12'4,2[2]15'2,3[1]19'5;4MOVES:1<5[2]@232'>6[2]@488'>3[1]@4330'2,1<10[1]@2241'3"

state_1_err = "STATE20ac18ab-6d18-450e-94af-bee53fdc8fcaIS2;3CELLS:1[2]12'4,2[2]15'2,3[1]33'6;4MOVES:1<5[2]@232'>6[2]@488'>3[1]@4330'2,1<10[1]@2241'3"

init = "INITc7f08867-3c21-46e9-94bb-d2c1e94fdb90TO2[0];2;7CELLS:0(0,0)'100'30'8'I,1(0,5)'100'30'8'I,2(5,0)'100'30'8'I,3(5,5)'200'30'8'II,4(5,10)'100'30'8'I,5(10,5)'100'30'8'I,6(10,10)'100'30'8'I;6LINES:0@4800OF2,0@4800OF1,2@4700OF3,3@4700OF4,4@4800OF6,5@4800OF6"
state = "STATEc7f08867-3c21-46e9-94bb-d2c1e94fdb90IS1;7CELLS:0[1]1'0,1[-1]6'0,2[1]1'8,3[1]1'8,4[1]15'8,5[-1]6'0,6[1]25'8;2MOVES:0<6[1]@3937675638'2,2<4[1]@3937675285'3"

init = "INIT920cd190-a714-452b-89e1-eccdddd861ccTO2[1];2;7CELLS:0(0,0)'100'30'8'I,1(0,5)'100'30'8'I,2(5,0)'100'30'8'I,3(5,5)'200'30'8'II,4(5,10)'100'30'8'I,5(10,5)'100'30'8'I,6(10,10)'100'30'8'I;6LINES:0@4800OF1,0@4800OF2,2@4700OF3,3@4700OF4,4@4800OF6,5@4800OF6"
state = "STATE920cd190-a714-452b-89e1-eccdddd861ccIS2;7CELLS:0[0]1'8,1[0]2'8,2[1]2'1,3[1]2'3,4[1]1'8,5[-1]6'0,6[1]4'8;7MOVES:0>9[0]@3938751928'>11[0]@3938753580'<4[0]@3938752563'<5[0]@3938753369'1,2<4[1]@3938752815'3,3<4[1]@3938752565'<4[1]@3938752718'4"


init = "INIT97068b57-6d72-489a-9f2b-9ba415dd861dTO2[1];2;7CELLS:0(0,0)'100'30'8'I,1(0,5)'100'30'8'I,2(5,0)'100'30'8'I,3(5,5)'200'30'8'II,4(5,10)'100'30'8'I,5(10,5)'100'30'8'I,6(10,10)'100'30'8'I;6LINES:0@4800OF1,0@4800OF2,2@4700OF3,3@4700OF4,4@4800OF6,5@4800OF6"
state = "STATEc2544a1a-76ee-4d00-941d-9fe14ea145f5IS2;7CELLS:0[0]0'8,1[0]0'2,2[0]1'8,3[1]2'3,4[1]1'8,5[1]0'2,6[1]0'8;6MOVES:0>4[0]@4027069315'2,0<4[0]@4027069566'1,2<4[1]@4027068817'3,3<4[1]@4027068567'4,4<4[1]@4027069317'6,5>4[1]@4027069567'6"

init = "INIT97068b57-6d72-489a-9f2b-9ba415dd861dTO2[1];2;7CELLS:0(0,0)'100'30'8'I,1(0,5)'100'30'8'I,2(5,0)'100'30'8'I,3(5,5)'200'30'8'II,4(5,10)'100'30'8'I,5(10,5)'100'30'8'I,6(10,10)'100'30'8'I;6LINES:0@4800OF1,0@4800OF2,2@4700OF3,3@4700OF4,4@4800OF6,5@4800OF6"
state = "STATE34fae468-a98a-41cb-a47c-d597dfa1d952IS2;7CELLS:0[0]17'8,1[0]12'8,2[0]20'8,3[0]30'8,4[0]26'8,5[1]2'8,6[1]29'8;4MOVES:4<1[1]@518103561'<1[1]@518105455'<1[1]@518105617'6,5>2[1]@518105255'6"

register_pooo(uid)
init_pooo( init )

terrain = cheshire.getTerrain()

"""

cheshire.setTemps( 518109648 )
cheshire.analyseMessage(state)

print( cheshire.getDecisions() )
"""
