# -*- coding: utf-8 -*-


"""Robot-joueur de Pooo
    
    Le module fournit les fonctions suivantes :
        register_pooo(uid)
        init_pooo(init_string)
        play_pooo()
        
"""

__version__='0.1'
 

## chargement de l'interface de communication avec le serveur
from poooc import order, state, state_on_update, etime

# mieux que des print partout
import logging
# pour faire de l'introspection
import inspect


# notre robot
from Robot import *

cheshire = None


"""Inscrit un joueur et initialise le robot pour la compétition

  :param uid: identifiant utilisateur
  :type uid:  chaîne de caractères str(UUID) 
  
  :Example:  "0947e717-02a1-4d83-9470-a941b6e8ed07"

"""
def register_pooo(uid):
    global cheshire
    logging.info( "-- Initialisation du robot --" )
    logging.info( "==== chaine uid reçu : {chaine}".format(chaine=uid)  )
    cheshire = Robot( uid )
    
    
    

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
def init_pooo(init_string):
    global cheshire
    
    logging.info( "-- Initialisation d'un match --" )
    
    if( cheshire ):
        cheshire.initialiserMatch( init_string )
    else:
        raise Exception("cheshire doit être initialisé avant d'initialiser un match !")
    
    
    
    
"""Active le robot-joueur

"""   
def play_pooo():
    global cheshire
    
    if( not cheshire ):
        raise Exception("vous devez exécuter les fonctions register_pooo() et init_pooo() avant !")
    
    logging.info('Entering play_pooo fonction from {} module...'.format(inspect.currentframe().f_back.f_code.co_filename))

    logging.info( "==> demande de l'état du jeu initial" )
    
    """
    init_state = state_on_update()#state()        # bloquant
    cheshire.updateTerrain( init_state )
    """
    
    while True:
        
        logging.info( "==> demande de l'état du jeu" )
        state = state_on_update()   # bloquant
        
        logging.info( "==> analyse de la réponse serveur" )
        cheshire.analyseMessage(state)
        
        if( cheshire.partieEnCours() ):
        
            logging.info( "==> prise de décision" )
            decisions = cheshire.getDecisions()
        
            logging.info( "==> envoie des décisions au serveur" )
            for decision in decisions:
                order( decision )
                
        else:
            logging.info( "==> partie fini" )
            break
            
    pass
    


# test 
"""
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


register_pooo(uid)
init_pooo( init )

cheshire.updateTerrain(state)

print( cheshire.getDecisions() )
"""