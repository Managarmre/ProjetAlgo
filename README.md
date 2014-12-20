**Projet Algo 3ème année**
=====================


## **Sommaire**

[TOC]

----------

## **Introduction**

Ce projet a pour but la programmation d'une IA pour du jeu Little Wars For Little Stars 2.


## **Les règles du jeu**

jeu de stratégie temps réel multi-joueurs

1. Le terrain est généré par le système, avec une position de départ (une cellule unique) attribuée à chaque joueur/robot engagé   

2. Chaque cellule occupée produit des unités offensives et défensives à concurrence de sa capacité et à une cadence définie par le système

3. Chaque cellule neutre possède au départ un nombre d’unités défini par le système et ne produit aucune nouvelle unité

4. Une proportion quelconque de l’effectif offensif d’une cellule peut se déplacer vers une cellule adjacente, à une vitesse définie par le système 

5. Si l’effectif d’une cellule (off+def) est inférieur strictement à l’effectif entrant, la cellule est conquise 

6. Dans tous les cas, l’effectif de la cellule diminue de l’effectif courant (off+def) moins l’effectif arrivant (min=0)

7. Les unités consommées en priorité sont les unités offensives

8. Lorsqu'une cellule n'a plus aucune unité, elle redevient neutre.

9. En transfert, les conflits entre unités ennemies qui se croisent sont résolus immédiatement



----------

## **Petit lexique**

- Terrain: graphe géométrique planaire dont les nœuds sont les cellules du jeu

- Cellule:  nœud du graphe, avec ses propriétés : 
1. capacités offensive et défensive
2. effectifs offensif et défensif
3. cadences de production offensive et défensive

- Cellule occupée: cellule appartenant à un joueur

- Cellule neutre: cellule libre de toute occupation

- Conquête: prise d'une cellule par un joueur

- Unité offensive: unité mobile, pour la conquête

- Unité défensive: unité fixe, propre à une cellule et utilisée en cas de prise

-  Capacité: nombre max. d'unités que peut accueillir une cellule

- Cadence de production: vitesse à laquelle sont créées les unités dans une cellule

----------

## **Le Protocole**


Chaîne d'enregistrement du joueur :  
: REG< uid >
:  
> "REG0947e717-02a1-4d83-9470-a941b6e8ed07"
  

Chaîne d'initialisation :
: INIT< matchid >TO<#players>[< me >];< speed >;\
:  <#cells>CELLS:
: - < cellid >(< x >,< y >)'< radius >'< offsize >'< defsize >'< prod >,...;\
:  <#lines>LINES:
: - < cellid >@< dist >OF< cellid >,...
:  
> "INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3"  

: < me > et < owner > désignent des numéros de 'couleur' attribués aux joueurs.

: < dist > est la distance qui sépare 2 cellules, exprimée en... millisecondes !
: -- La couleur -1 est le neutre.
: -- Le neutre n'est pas compté dans l'effectif de joueurs (<#players>).
: -- '...' signifie que l'on répète la séquence précédente autant de fois qu'il y a de cellules (ou d'arêtes).
: -- 0CELLS ou 0LINES sont des cas particuliers sans suffixe.

: /!\ attention: un match à vitesse x2 réduit de moitié le temps 'effectif' de trajet d'une cellule à l'autre par rapport à l'indication < dist >. De manière générale temps_de_trajet=< dist >/vitesse (division entière)


Chaîne d'état du jeu :
: STATE< matchid >IS<#players>;
: <#cells>CELLS:
: - < cellid >[< owner >]< offunits >'< defunits >,...;\
: <#moves>MOVES:
: - < cellid >
: - - < direction ><#units>[< owner >]@< timestamp >'...
: - < cellid >, ...
: 
> "STATE20ac18ab-6d18-450e-94af-bee53fdc8fcaIS2;3CELLS:1[2]12'4,2[2]15'2,3[1]33'6;4MOVES:1<5[2]@232'>6[2]@488'>3[1]@4330'2,1<10[1]@2241'3"  

: < timestamp > en millisecondes, donnée à vitesse 1 : top départ des unités de la cellule source.

: < direction > désigne le caractère '>' ou '<' et indique le sens des unités en mouvement en suivant la pointe de flèche.


Ordre de mouvement (MOVe FROM TO)  :
: [< userid >]MOV<%offunits>FROM< cellid >TO< cellid >   
:   
> "[0947e717-02a1-4d83-9470-a941b6e8ed07]MOV33FROM1TO4"

: -- le pourcentage des unités offensives utilise la division entière. 

: Par exemple : 25% de 50=50*25/100=12.   

: -- un ordre dont l'effectif d'unités off est nul (par ex., 33% de 2 unités) est ignoré.    




Fin de jeu pour le joueur (éliminé ou vainqueur) :
: GAMEOVER[ < color > ]IN< matchid >  
: 
>"GAMEOVER[ 2 ]IN20ac18ab-6d18-450e-94af-bee53fdc8fca"
: 


Fin du jeu :
: ENDOFGAME< matchid >
: 
> "ENDOFGAME20ac18ab-6d18-450e-94af-bee53fdc8fca"


--------------------

## **Vos Droits**

Les fonctions disponibles pour obtenir/transmettre de l'information du/au serveur
sont exposées par le module poooc. Ces fonctions sont au nombre de 4 :

Ordonne un mouvement
: order(msg)

: param msg: type chaîne de caractères (utf-8 string), conforme au protocole "Ordre de mouvement"


Demande l'état courant du jeu
: state()

: retourne un message sous la forme d'une "Chaîne d’état du jeu" selon le protocole 

Demande l'état du jeu modifié
: state_on_update()
: -- La valeur de retour est identique à celle de la fonction state().
: -- La principale différence provient du fait que le processus est mis en attente d'une mise à jour de l'état du jeu.

: -- L'appel de state_on_update() est bloquant.

Obtenir le temps écoulé (elapsed time) depuis le début du match
: etime()
: -- retourne temps écoulé (elapsed time) en millisecondes (un entier).
: /!\ le temps indiqué n'est qu'une approximation (la plus précise possible)




--------------------

## **Vos Devoirs**

- Les fonctions que vous devez implémenter, comme points d'entrée du robot-joueur pour qu'il puisse dialoguer avec le serveur de jeu, sont les suivantes :

1. register_pooo(uid) : inscrit le joueur et initialise le robot pour la compétition
2. init_pooo(init_string) : initialise le robot pour un match
3. play_pooo() : active le robot-joueur

- Ces fonctions sont documentées dans le modèle de fichier disponible.
- Ces fonctions sont à incorporer dans un seul module (un fichier .py) dont le nom vous est propre et qui sera chargé au moment de lancer le programme client. 
- Tout le reste (vos structures de données, vos fonctions, etc.) est à définir et à organiser par vos soins.


