==============================================================================================================================================================
========================================================================= Projet Cheshire ====================================================================
==============================================================================================================================================================

## Sommaire
	Introduction
	1 - R�gles du jeu
	2 - Lexique
	3 - Faire fonctionner le jeu
	4 - Ce que contient le dossier

## Introduction
Ce projet a �t� r�alis� par CARON Cyril, HOULGATTE Pauline et PINEAU Maxime. Il a pour but de programmer un client capable de communiquer avec un client fourni ainsi que de d�velopper une IA pour le jeu Little Wars For Litte Stars 2.

1 - R�gles du jeu
Jeu de strat�gie temps r�el multi_joueurs.

	
1. Le terrain est g�n�r� par le syst�me, avec une position de d�part (une cellule unique) attribu�e � chaque joueur/robot engag�   


	2. Chaque cellule occup�e produit des unit�s offensives et d�fensives � concurrence de sa capacit� et � une cadence d�finie par le syst�me


	3. Chaque cellule neutre poss�de au d�part un nombre d�unit�s d�fini par le syst�me et ne produit aucune nouvelle unit�


	4. Une proportion quelconque de l�effectif offensif d�une cellule peut se d�placer vers une cellule adjacente, � une vitesse d�finie par le syst�me 


	5. Si l�effectif d�une cellule (off+def) est inf�rieur strictement � l�effectif entrant, la cellule est conquise 


	6. Dans tous les cas, l�effectif de la cellule diminue de l�effectif courant (off+def) moins l�effectif arrivant (min=0)


	7. Les unit�s consomm�es en priorit� sont les unit�s offensives


	8. Lorsqu'une cellule n'a plus aucune unit�, elle redevient neutre.
	

9. En transfert, les conflits entre unit�s ennemies qui se croisent sont r�solus imm�diatement

2 - Lexique
- Terrain: graphe g�om�trique planaire dont les noeuds sont les cellules du jeu
- Cellule:  noeud du graphe, avec ses propri�t�s ; 



	1. capacit�s offensive et d�fensive


	2. effectifs offensif et d�fensif


	3. cadences de production offensive et d�fensive
  


- Cellule occup�e: cellule appartenant � un joueur


- Cellule neutre: cellule libre de toute occupation


- Conqu�te: prise d'une cellule par un joueur


- Unit� offensive: unit� mobile, pour la conqu�te


- Unit� d�fensive: unit� fixe, propre � une cellule et utilis�e en cas de prise


- Capacit�: nombre max. d'unit�s que peut accueillir une cellule


- Cadence de production: vitesse � laquelle sont cr��es les unit�s dans une cellule

3 - Faire fonctionner le jeu
Pour lancer le jeu, il est n�cessaire de d�marrer le serveur :
	$ ./poooserver.py [-h] [-P PORT] [-B {1024,2048,4096}] [-s {1,2,4}]

	Options : 
	-h, --help visualiser le message d'aide et quitter 
	-P PORT, --port PORT  port du serveur (Defaut: 9876)
 
	-s {1,2,4}, --speed {1,2,4}
   vitesse du jeu (Defaut: 1)
  
	-r ROOMSIZE, --roomsize ROOMSIZE
   nombre de robots (Default: 4, accepted values: 2+)

Exemple: $ python poooserver.py -s 2 -r 4
Lancer ensuite les robots (avec les fichier pooobot.py et lolipooo.py dans le m�me r�pertoire) :
	a) avec r�cup�ration des logs : ./pooobot.py -s 127.0.0.1:9876 -b lolipooo c1 &> c1.log.txt
	b) sans r�cup�ration des logs : ./pooobot.py -s 127.0.0.1:9876 -b lolipooo c1
Choississez ensuite le num�ro de la carte de jeu (entre 0 et 8), puis "Entr�e".

Il est �galement possible de lancer une interface graphique avec le robot.
Pour cela, il suffit d'utiliser le fichier lolipooo par graphique_lolipooo :
	- ./pooobot.py -s 127.0.0.1:9876 -b graphique_lolipooo c1
Il faut noter que cette interface n'est qu'en version b�ta, et que des probl�mes existent, notamment :
	- si la salle du serveur est plus grande que pour 2 joueurs, l'interface ne veut pas afficher le 3eme match
	- si la vitesse du jeu n'est pas � 1, les unit�s sur les liens ont tendances � 'se t�l�porter' sur le lien plut�t que se d�placer.

4 - Ce que contient le rendu
Le dossier contient :
	- le compte rendu du projet
	- le code source du projet
	- un readme
	- la documentation li�e au projet
	- le code source de l'interface graphique