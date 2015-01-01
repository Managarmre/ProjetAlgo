
#from Cellule import *
#from Lien import *

import Cellule as ce 
import Lien as li 


# le terrain du jeu
# représente un graphe
class Terrain:

	def __init__( self ):

		# les cellules représentent des sommets
		# les liens représentent des arêtes

		self.cellules = {}
		self.liens = {}

		# on utilise ici des dictionnaires (équivalent des hashmaps en python)



	# ajoute une cellule dans le terrain / graphe
	# Cellule cellule : la cellule à ajouter
	def ajouterCellule(self, cellule):
		
		if( not isinstance( cellule , ce.Cellule ) ):
			raise Exception("ce n'est pas une instance de l'objet Cellule")
		
		# comme un numéro de cellule n'identifie qu'une seule cellule, on l'utilise pour retrouver la cellule
		self.cellules[ cellule.getNumero() ] = cellule
	

	# ajoute un lien entre deux cellules dans le terrain
	# Lien lien : le lien à ajouter
	def ajouterLien(self, lien):
		
		if( not isinstance(lien, li.Lien ) ):
			raise Exception("le parametre lien n'est pas une instance de l'objet Lien ")
		if( lien.getU() not in self.getCellules().values() or lien.getV() not in self.getCellules().values() ):
			raise Exception("l'une des cellules (ou les deux) n'est pas présente dans le graphe")
			
		self.liens[ lien.hash() ] = lien


	
	# retourne la liste des composantes connexes du graphe
	# return : List<Terrain>
	def getComposantesConnexes(self):

		# initialisation
		# au debut, à chaque sommet on fait correspondre un numéro de composante connexe différente
		composante_des_sommets = { cellule.getNumero(): cellule.getNumero() for cellule in self.getCellules().values() }

		# on parcourt tous les sommets
		for numero,cellule in self.getCellules().items():

			cesVoisins = self.getVoisinsCellule( cellule )
			
			# on change son numéro de composante connexe
			# car, comme elle est voisine avec cette cellule
			# elles sont toutes deux dans la même composante connexe
			for voisin in cesVoisins:

				# si mon voisin a un numéro plus grand que mon numero
				# alors son numéro devient le mien
				if( composante_des_sommets[ voisin.getNumero() ] > composante_des_sommets[ numero ]  ):
					composante_des_sommets[ voisin.getNumero() ] = composante_des_sommets[ numero ]
			
			
		# on inverse
		# pour chaque numéro de composantes connexes, on y fait correspondre les numéro des sommets qui y sont présents
		composantes = {}
		for key, value in composante_des_sommets.items():
			composantes.setdefault( value, [] ).append( self.getCellule(key) )

		# on retourne la liste des sous graphes ayant ces sommets
		return [ self.getSousGraphe(sommets_composante) for sommets_composante in composantes.values()  ]


	# retourne le sous graphe contenant les cellules données en paramètre
	# List<Cellule> listeCellules : la liste des cellules contenu dans le sous graphe
	# return : Terrain
	def getSousGraphe(self, listeCellules):
		
		# on crée un nouveau terrain
		terrain = Terrain()

		# on ajoute les cellules dans ce nouveau terrain
		for cellule in listeCellules:
			terrain.ajouterCellule(cellule)


		a_faire = listeCellules[:]
		# on ajoute les liens reliant les cellules du terrain
		for cellule in listeCellules:
			
			for lien in cellule.getLiens():

				if( lien.getOtherCellule( cellule ) in a_faire ):
					terrain.ajouterLien(lien)
			
			a_faire.remove(cellule)
			
		return terrain




	# retourne le plus court chemin entre deux cellules/sommets
	# Cellule depart : la cellule de départ
	# Cellule arivee : la cellule d'arrivée
	# retourne : le plus court chemin sous forme d'une liste de sommet et la distance totale à parcourir
	def dijkstra( self, depart, arrivee ):

		infinity = float("inf")


		# initialisation des tableaux 
		parcouru = { numero: infinity for numero,cellule in self.getCellules().items() }
		precedent = { numero: -1 for numero,cellule in self.getCellules().items() }


		parcouru[ depart.getNumero() ] = 0
		pasEncoreVu = list( self.getCellules().keys() ) 	# liste des numéro des cellules par encore vues


		# même chose que : pasEncoreVu != []
		while( pasEncoreVu ):

			# on recherche la cellule la plus proche
			# le_plus_proche est un NUMERO de cellule (ce n'est pas une cellule)
			le_plus_proche = min( pasEncoreVu , key=parcouru.get )
			cellule_la_plus_proche = self.getCellule( le_plus_proche )
			# on recherche le numéro dans pasEncoreVu
			# ayant la plus petite valeur de parcouru.get( cle )

			pasEncoreVu.remove( le_plus_proche )


			# voisin est une CELLULE
			for voisin in self.getVoisinsCellule( cellule_la_plus_proche ) :

				numero_voisin = voisin.getNumero()

				distance = self.getLiens().get( li.Lien.hachage(cellule_la_plus_proche,voisin) ).getDistance()

				if( parcouru[ numero_voisin ] > parcouru[ le_plus_proche ] + distance ):

					parcouru[ numero_voisin ] = parcouru[ le_plus_proche ] + distance 
					precedent[ numero_voisin ] = le_plus_proche


		# on récupère le chemin en parcourant le tableau depuis l'arrivée
		chemin = [] 
		n = arrivee.getNumero() 

		while( n != depart.getNumero() ):

			chemin.append( n )
			n = precedent[ n ]

		chemin.append( depart.getNumero() )

		chemin.reverse()

		return ( chemin , parcouru[ arrivee.getNumero() ] )


	# retourne le chemin depuis une cellule vers la cellule la plus proche selectionnée dans un ensemble
	# Cellule depart
	# List<Cellule> arrivees
	def getCheminVersCellulePlusProche( self, depart, arrivees ):
		
		infinity = float("inf")
		distance_min = infinity
		chemin_min = []
		
		for arrivee in arrivees :
			
			chemin, distance = self.dijkstra( depart, arrivee )
			
			if( distance < distance_min ):
				distance_min = distance
				chemin_min = chemin
		
		return chemin


	# retourne la cellule du graphe ayant le numéro associé
	# si la cellule correspondant à ce numéro n'est pas dans le terrain, une exception est lancée.
	# Int numero : le numéro de la cellule recherchée
	def getCellule(self, numero):
		try:
			return self.cellules[ numero ]
		except Exception:
			raise Exception( "il n'y a aucune cellule ayant ce numéro ({numero}) dans ce terrain".format(numero=numero) )


	# retourne la liste des cellules appartenant au joueur ayant la couleur donnée (un entier)
	def getCellulesJoueur(self, couleurJoueur):
		return [ cellule for numero, cellule in self.getCellules().items() if cellule.getCouleurJoueur() == couleurJoueur  ]
		

	# retourne la liste des cellules du terrain (sous forme d'un dictionnaire)
	def getCellules(self):
		return self.cellules


	# retourne la liste des voisins de la cellule donnée en paramètre
	# lance une exception si on entre autre chose qu'une Cellule
	# lance une exception si la cellule n'appartient pas à ce graphe
	def getVoisinsCellule( self, cellule ):
		
		if( not isinstance( cellule , ce.Cellule ) ):
			raise Exception("le paramètre entrée n'est pas une instance de l'objet Cellule")
		if( cellule not in self.getCellules().values() ):
			raise Exception("cette cellule n'est pas présente dasn ce terrain/graphe")
		
		return [ lien.getOtherCellule( cellule ) for numero,lien in self.getLiens().items() if lien.celluleAppartientAuLien(cellule) ]
			

	# retourne le lien du graohe ayant le numéro associé
	# ce numéro peut être calculer en utilisant la méthode Lien.hashage(cellule1,cellule2) 
	# Int numeroLien : le numéro unique identifiant le lien
	def getLien(self, numeroLien):
		try:
			return self.liens[ numeroLien ]
		except Exception:
			raise Exception("il n'y a aucun lien ayant ce numéro dans ce terrain")


	# retourne la liste des liens du terrain (sous forme d'un dictionnaire)
	def getLiens(self):
		return self.liens


	# retourne le nombre de cellules présentes dans le graphe
	def getNbCellules(self):
		return len(self.cellules)

	# retourne le nombre de liens présents dans le graphe
	def getNbLiens(self):
		return len(self.liens)


	def toString(self):

		chaine = "S = { "

		for numero_cellule, cellule in self.cellules.items():
			chaine += "\n( {numero}, {owner} ),".format( numero = cellule.getNumero(), owner = cellule.getCouleurJoueur() )


		chaine += "}" + "\n" + "A = { "

		for numero_lien, lien in self.liens.items():
			chaine += "\n" + lien.toString()

		return chaine + "\n}"
		

