==============================================================================================================================================================
========================================================================= Projet Cheshire ====================================================================
==============================================================================================================================================================

## Sommaire
	Introduction
	1 - Règles du jeu
	2 - Lexique
	3 - Faire fonctionner le jeu
	4 - Ce que contient le dossier

## Introduction
Ce projet a été réalisé par CARON Cyril, HOULGATTE Pauline et PINEAU Maxime. Il a pour but de programmer un client capable de communiquer avec un client fourni ainsi que de développer une IA pour le jeu Little Wars For Litte Stars 2.

1 - Règles du jeu
Jeu de stratégie temps réel multi_joueurs.

	
1. Le terrain est généré par le système, avec une position de départ (une cellule unique) attribuée à chaque joueur/robot engagé   


	2. Chaque cellule occupée produit des unités offensives et défensives à concurrence de sa capacité et à une cadence définie par le système


	3. Chaque cellule neutre possède au départ un nombre d’unités défini par le système et ne produit aucune nouvelle unité


	4. Une proportion quelconque de l’effectif offensif d’une cellule peut se déplacer vers une cellule adjacente, à une vitesse définie par le système 


	5. Si l’effectif d’une cellule (off+def) est inférieur strictement à l’effectif entrant, la cellule est conquise 


	6. Dans tous les cas, l’effectif de la cellule diminue de l’effectif courant (off+def) moins l’effectif arrivant (min=0)


	7. Les unités consommées en priorité sont les unités offensives


	8. Lorsqu'une cellule n'a plus aucune unité, elle redevient neutre.
	

9. En transfert, les conflits entre unités ennemies qui se croisent sont résolus immédiatement

2 - Lexique
- Terrain: graphe géométrique planaire dont les noeuds sont les cellules du jeu
- Cellule:  noeud du graphe, avec ses propriétés ; 



	1. capacités offensive et défensive


	2. effectifs offensif et défensif


	3. cadences de production offensive et défensive
  


- Cellule occupée: cellule appartenant à un joueur


- Cellule neutre: cellule libre de toute occupation


- Conquête: prise d'une cellule par un joueur


- Unité offensive: unité mobile, pour la conquête


- Unité défensive: unité fixe, propre à une cellule et utilisée en cas de prise


- Capacité: nombre max. d'unités que peut accueillir une cellule


- Cadence de production: vitesse à laquelle sont créées les unités dans une cellule

3 - Faire fonctionner le jeu
Pour lancer le jeu, il est nécessaire de démarrer le serveur :
	$ ./poooserver.py [-h] [-P PORT] [-B {1024,2048,4096}] [-s {1,2,4}]

	Options : 
	-h, --help visualiser le message d'aide et quitter 
	-P PORT, --port PORT  port du serveur (Defaut: 9876)
 
	-s {1,2,4}, --speed {1,2,4}
   vitesse du jeu (Defaut: 1)
  
	-r ROOMSIZE, --roomsize ROOMSIZE
   nombre de robots (Default: 4, accepted values: 2+)

Exemple: $ python poooserver.py -s 2 -r 4
Lancer ensuite les robots (avec les fichier pooobot.py et lolipooo.py dans le même répertoire) :
	a) avec récupération des logs : ./pooobot.py -s 127.0.0.1:9876 -b lolipooo c1 &> c1.log.txt
	b) sans récupération des logs : ./pooobot.py -s 127.0.0.1:9876 -b lolipooo c1
Choississez ensuite le numéro de la carte de jeu (entre 0 et 8), puis "Entrée".

Il est également possible de lancer une interface graphique avec le robot.
Pour cela, il suffit d'utiliser le fichier lolipooo par graphique_lolipooo :
	- ./pooobot.py -s 127.0.0.1:9876 -b graphique_lolipooo c1
Il faut noter que cette interface n'est qu'en version béta, et que des problèmes existent, notamment :
	- si la salle du serveur est plus grande que pour 2 joueurs, l'interface ne veut pas afficher le 3eme match
	- si la vitesse du jeu n'est pas à 1, les unités sur les liens ont tendances à 'se téléporter' sur le lien plutôt que se déplacer.

4 - Ce que contient le rendu
Le dossier contient :
	- le compte rendu du projet
	- le code source du projet
	- un readme
	- la documentation liée au projet
	- le code source de l'interface graphique