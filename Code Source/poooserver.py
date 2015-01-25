#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Serveur de jeu temps réel Pooo
        
"""

import socketserver
import socket
import threading
import logging
import re
import argparse

logging.basicConfig(level=logging.DEBUG)


parser = argparse.ArgumentParser(description='Pooo game server', epilog='Example: $python poooserver.py -P 9876 -B 2048 --speed 2 --roomsize 4')
parser.add_argument('-P','--port', type=int, default=9876, help='port number of the Pooo server (Default: 9876)')
parser.add_argument('-B','--bufsize', type=int, choices=[1024, 2048, 4096], default=2048, help='size of the socket buffer (Default: 2048)')
parser.add_argument('-s','--speed', type=int, choices=[1, 2, 4], default=1, help='speed of the game (Default: 1)')
parser.add_argument('-r','--roomsize', type=int, default=4, help='size of the room (Default: 4, accepted values: 2+)')
parser.add_argument('-g','--gui', help='address (IP:Port) of the GUI if any')
#parser.add_argument('-M','--matchsize', type=int, default=2, help='number of bots in a match (Default: 2, accepted values: 2)')

# args.server et args.player
args = parser.parse_args()

BUFSIZE=args.bufsize
ROOM_SIZE=args.roomsize
SPEED=args.speed
HOST, PORT = "localhost", args.port


from pooogame import Room, Contest, Player, PoooSocket

#LOG_FILENAME=
#LEVELS = { 'debug':logging.DEBUG,
#            'info':logging.INFO,
#            'warning':logging.WARNING,
#            'error':logging.ERROR,
#            'critical':logging.CRITICAL,
#            }
logging.basicConfig(level=logging.DEBUG)



class PoooHandler(socketserver.BaseRequestHandler):
    """callback du serveur lorsqu'il enregistre une nouvelle connexion (un nouveau client) 
    
    """
    
    def handle(self):
        self.request.set_inheritable(True)  # tricks pour la version python 3.4 (3 jours de debug...)
        # register new player
        p=Player(self.request, self.client_address, self.server.engage, bufsize=BUFSIZE)
        p.start()
        self.server.join(p)        
        return
            
            

class PoooServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    engage=threading.Event()  # set when a contest is created from current room (then reseted)
    contests=[]
    room=None
    
    @property
    def load(self):
        return len(self.contests)


def fucking_failing_main():
    server = PoooServer((HOST, PORT), PoooHandler)
    room=Room(server, room_size=ROOM_SIZE, speed=SPEED)
    room.start()
    
    # Démarre un thread pour le serveur -- chaque nouvelle connexion entrante
    # démarre un nouveau thread également
    server_thread = threading.Thread(name='Pooo server', target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    logging.info("{} up and running at {}:{}".format(server_thread.name, HOST, PORT))

    try: 
        server_thread.join()
    except KeyboardInterrupt:
        logging.warning('Ctr-C  Stop server\n')


class Server:
    lock = threading.Lock()
    engage=threading.Event()
    contests = []
    
    @property
    def load(self):
        return len(self.contests)   
        

def main(): # version avec socket bloquante, mais au moins ça fonctionne !
    server=Server()
    
    room = Room(server, ROOM_SIZE, SPEED)
    room.start()

    ssock = socket.socket()
    ssock.bind(('', PORT))
    ssock.listen(ROOM_SIZE*3)
    while True:
        try: 
            sock, addr = ssock.accept()            
            with server.lock:
                # register new player
                p=Player(PoooSocket(sock=sock), server.engage)
                p.start()
                room.join(p)        
                
        except KeyboardInterrupt:
            print('Ctrl C')
            ssock.close()
            break
            

if __name__ == "__main__":    
    main()
