import Strategie as st
import Mouvement as mv
import Lien as li
import logging
import random
import math
import functools 
import operator 


# stratégie appelable uniquement pour les cellules attaquantes non en danger
# stratégie qui regarde quelle planète voisine est sur le point de ce faire capturer
# (si plusieurs en même temps, laquelle privilégier ? : la plus proche, la moins coûteuse en troupe (sachant qu'il faut compter les liens), autre)
# pour l'instant on privilégie la distance
# envoyer les troupes pour prendre la planète + 10% des troupes restantes sur la planète attaquante
# on regarde le temps avant que la planète soit prise (mouvement ennemi qui arrive à destination)
# et on le compare au temps que nos troupes vont mettre pour atteindre la planète cible
# si leur temps est plus grand que le notre alors on attend sinon on envoie

class StrategiePupute(st.Strategie):
    def __init__(self,robot):
        st.Strategie.__init__(self,robot)
        
    