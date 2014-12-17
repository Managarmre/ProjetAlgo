# -*- coding: utf-8 -*-


"""Serveur de jeu temps réel Pooo
        
"""

import socketserver
import socket
import threading
import logging
import re

ROOM_SIZE=4

from pooogame import Room, Contest, Player


BUFSIZE=2048

HOST, PORT = "localhost", 9876


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
        p=Player(self.request, self.client_address, self.server.engage)
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
                
    def join(self, player):
        room.join(player)


def fucking_failing_main():
    server = PoooServer((HOST, PORT), PoooHandler)
    room=Room(server)
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
    room = Room(server, ROOM_SIZE)
    room.start()

    ssock = socket.socket()
    ssock.bind(('', 9876))
    ssock.listen(ROOM_SIZE*3)
    while True:
        try: 
            sock, addr = ssock.accept()            
            with server.lock:
                # register new player
                sock.set_inheritable(True)  # tricks pour la version python 3.4
                p=Player(sock, addr, server.engage)
                p.start()
                room.join(p)        
                
        except KeyboardInterrupt:
            print('Ctrl C')
            ssock.close()
            break
            

if __name__ == "__main__":    
    main()
