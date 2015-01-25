
#from Cellule import *
#from Lien import *

import Cellule as ce 
import Lien as li 
from Exceptions import TerrainException

class Terrain:
	"""
	Le terrain du jeu représente un graphe
	"""

	def __init__( self ):
		"""
		Constructeur de la classe Terrain. Initialise un terrain vide, sans cellule, ni lien.
		"""

		# les cellules représentent des sommets
		# les liens représentent des arêtes

		self.cellules = {}
		self.liens = {}
		self.mouvements = []

		# on utilise ici des dictionnaires (équivalent des hashmaps en python)


	def ajouterCellule(self, cellule):
		"""
		Ajoute la cellule passée en paramètre dans le terrain
		
		:param :class:'Cellule' cellule: la cellule à ajouter
		"""

		if( not isinstance( cellule , ce.Cellule ) ):
			raise TerrainException("ce n'est pas une instance de l'objet Cellule")
		
		# comme un numéro de cellule n'identifie qu'une seule cellule, on l'utilise pour retrouver la cellule
		self.cellules[ cellule.getNumero() ] = cellule
	

	def ajouterLien(self, lien):
		"""
		Ajoute le lien passé en paramètre dans le terrain
		
		:param :class:'Lien' lien: Le lien à ajouter
		:raises :class'TerrainException': si au moins l'une des cellule du lien n'est pas présente dans le terrain
		"""
		
		if( not isinstance(lien, li.Lien ) ):
			raise TerrainException("le parametre lien n'est pas une instance de l'objet Lien ")
		if( lien.getU() not in self.getCellules().values() or lien.getV() not in self.getCellules().values() ):
			raise TerrainException("l'une des cellules (ou les deux) n'est pas présente dans le graphe")
			
		self.liens[ lien.hash() ] = lien


	def getComposantesConnexes(self):
		"""
		Retourne la liste des composantes connexes du graphe (le terrain se comporte comme un graphe).
		
		:returns: les composantes connexes du graphe.
		:rtype: list of :class:'Terrain'
		"""

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


	def getSousGraphe(self, listeCellules):
		"""
		Retourne le sous graphe contenant les cellules données en paramètre
		
		:param listeCellules: La liste des cellules
		:type listeCellules: list of :class:'Cellule'
		:returns: le sous graphe correspondant
		:rtype: Terrain
		"""

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


	def dijkstra( self, depart, arrivee ):
		"""
		Retourne le plus court chemin entre deux cellules passées en paramètre
		
		:param :class:'Cellule' depart: La cellule de départ
		:param :class:'Cellule' arrivee: La cellule d'arrivée
		:returns: le plus court chemin entre les deux cellules (une liste de numéro de cellule), et la distance totale à parcourir
		:rtype: ( List<int> , int ) 
		"""

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


	def getCheminVersCellulePlusProche( self, depart, arrivees ):
		"""
		Retourne le chemin depuis une cellule vers la cellule la plus proche selectionnée dans un ensemble
		
		:param :class:'Cellule' depart: La cellule de départ
		:param arrivees: L'ensemble des cellules d'arrivée
		:type arrivees: list of :class:'Cellule'
		:returns: le chemin le plus court entre la cellule de départ et la cellule d'arrivée la plus proche (correspond à la liste des numéro des cellules composant le chemin)
		:rtype: list of int
		"""

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
		"""
		Retourne la cellule du terrain ayant le numéro associé passé en paramètre
		
		:param int numero: Le numéro de la cellule recherchée
		:returns: la cellule associée au numéro
		:rtype: :class:'Cellule'
		:raises :class:'TerrainException': si il n'y a aucune cellule dans le terrain possédant ce numéro
		"""

		try:
			return self.cellules[ numero ]
		except Exception:
			raise TerrainException( "il n'y a aucune cellule ayant ce numéro ({numero}) dans ce terrain".format(numero=numero) )


	def getCellulesJoueur(self, couleurJoueur):
		"""
		Retourne la liste des cellules appartenant au joueur ayant la couleur passée en paramètre (-1 pour le neutre).
		
		:param int couleurJoueur: la couleur du joueur
		:returns: la liste des cellules de ce joueur
		:rtype: list of :class:'Cellule'
		"""
		return [ cellule for numero, cellule in self.getCellules().items() if cellule.aPourCouleur( couleurJoueur )  ]
		

	def getCellules(self):
		"""
		Retourne le dictionnaire contenant la liste de toutes les cellules du terrain
		
		:returns: le dictionnaire contenant les cellules du terrain
		:rtype: dict
		"""
		return self.cellules


	def getVoisinsCellule( self, cellule ):
		"""
		Retourne la liste des voisins de la cellule sur le terrain passée en paramètre
		
		:param :class:'Cellule' cellule: La cellule dont on veut récupérer la liste des voisins sur le terrain
		:returns: la liste des cellules voisine à celle passée en paramètre
		:rtype: list of :class:'Cellule'
		:raises :class:'TerrainException': si la cellule n'est pas présente sur le terrain
		"""

		if( not isinstance( cellule , ce.Cellule ) ):
			raise TerrainException("le paramètre entré n'est pas une instance de l'objet Cellule")
		if( cellule not in self.getCellules().values() ):
			raise TerrainException("cette cellule n'est pas présente dans ce terrain/graphe")
		
		return [ lien.getOtherCellule( cellule ) for numero,lien in self.getLiens().items() if lien.celluleAppartientAuLien(cellule) ]
			

	# retourne le lien du graohe ayant le numéro associé
	# ce numéro peut être calculer en utilisant la méthode Lien.hashage(cellule1,cellule2) 
	# Int numeroLien : le numéro unique identifiant le lien
	def getLien(self, numeroLien):
		"""
		Retourne le lien du terrain ayant le numéro associé passé en paramètre
		
		:param int numeroLien: Le numéro de le lien recherché
		:returns: le lien associée au numéro
		:rtype: :class:'Lien'
		:raises :class:'TerrainException': si il n'y a aucun Lien dans le terrain possédant ce numéro
		"""
		try:
			return self.liens[ numeroLien ]
		except Exception:
			raise TerrainException("il n'y a aucun lien ayant ce numéro dans ce terrain")


	def getLienEntreCellules(self, cellule_1, cellule_2 ):
		"""
		Retourne le lien sur le terrain entre les 2 cellules passées en paramètre
		
		:param :class:'Cellule' cellule_1: La première cellule
		:param :class:'Cellule' cellule_2: La deuxième cellule
		:returns: le lien entre les deux cellules
		:rtype: :class:'Lien'
		:raises :class:'TerrainException': si le lien n'est pas présent dans le terrain
		"""
		numero = li.Lien.hachage( cellule_1, cellule_2 )
		return self.getLien( numero )


	def getLiens(self):
		"""
		Retourne le dictionnaire contenant la liste de touts les liens du terrain
		
		:returns: le dictionnaire contenant les liens du terrain
		:rtype: dict
		"""
		return self.liens


	def getNbCellules(self):
		"""
		Retourne le nombre de cellules présentes dans le terrain
		
		:returns: le nombre de cellules sur le terrain
		:rtype: int
		"""
		return len(self.cellules)


	def getNbLiens(self):
		"""
		Retourne le nombre de liens présentes dans le terrain
		
		:returns: le nombre de liens sur le terrain
		:rtype: int
		"""
		return len(self.liens)


	def toString(self):
		"""
		Retourne sous forme de chaine une représentation textuelle du terrain
		
		:returns: le terrain sous forme de chaine de caractères
		:rtype: str
		"""

		chaine = "S = { "

		for numero_cellule, cellule in self.cellules.items():
			chaine += "\n( {numero}, {owner} ),".format( numero = cellule.getNumero(), owner = cellule.getCouleur() )


		chaine += "}" + "\n" + "A = { "

		for numero_lien, lien in self.liens.items():
			chaine += "\n" + lien.toString()

		return chaine + "\n}"
		
