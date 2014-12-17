#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Client pour le jeu Pooo
    
    Projet d'algorithmique et programmation
    INFO3@Polytech Nantes 2014-2015

"""

import poooc
import argparse
import importlib
import threading
import logging

logging.basicConfig(level=logging.DEBUG)


parser = argparse.ArgumentParser(description='Client for Pooo game', epilog='Example: $pooobot.py -h 192.168.10.4:9876 -b lollipooo Alice')
parser.add_argument('-s','--server', required=True, help='address formatted as host:port of the Pooo server')
parser.add_argument('-b','--bot', required=True, help='module name of the bot')
parser.add_argument('player', help='name of the player')

# args.server et args.player
args = parser.parse_args()

logging.info('Bot {} playing as {} onto {}'.format(args.bot, args.player, args.server))

# charge le joueur-robot
bot = importlib.import_module(args.bot)

# récupère les informations de connexion
HOST, PORT = args.server.strip().split(':')


def main():
        
    # inscrit le joueur-robot à la compétition
    uid = poooc.register(args.player, HOST, PORT)
    if uid is None:
        logging.error('Registration failed')
        return
        
    bot.register_pooo(uid)

    if poooc.engage():
    
        while not poooc.contestover():
            # entre dans un match

            # appel bloquant: attend le lancement d'un nouveau match et récupère la chaîne d'initialisation
            init_string = poooc.init_match()
            bot.init_pooo(init_string)
            # le client est prêt à jouer
            poooc.ready()
            client = threading.Thread(target=bot.play_pooo)
            match = threading.Thread(target=poooc.run)
            # début de la phase de jeu
            client.start()
            match.start()
    
            # siffle la fin du match
            match.join()
            # /!\ le bot (thread client) est supposé terminer de lui-même sur interception de GAMEOVER puis ENDGAME (hum hum) !
            # dans le cas contraire, on va avoir des threads orphelins qui tournent à vide
            # avec un client.join(), on prendrait le risque de rester scotché ici. à choisir...
    
        #sortie de boucle: fin de la compétition
    else:
        logging.error('Contest engagement failed')


if __name__=='__main__':
    main()

