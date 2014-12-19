
#from Cellule import *
#from Lien import *

import Cellule as ce 
import Lien as li 


# le terrain du jeu
# représente un graphe
class Terrain:

	def __init__( self ):

		# la liste des cellules du terrain (représentent des sommets)
		# comme un numéro de cellule n'identifie qu'une seule cellule, on l'utilise pour retrouver la cellule
		self.cellules = {}

		# la liste des liens du terrain (représentation des arêtes)
		self.liens = {}

		# on utilise ici des dictionnaires (équivalent des hashmap en python)



	# ajoute une cellule dans le graphe
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



	
	
	
	# retourne la liste des composantes du graphe, attention, cette liste est une liste de terrain.
	# return : List<Terrain>
	def getComposantesConnexes(self):

		# initialisation
		# au debut, à chaque sommet on fait correspondre un numéro de composante connexe différente
		composante_des_sommets = { cellule.getNumero(): cellule.getNumero() for cellule in self.getCellules().values() }

		# on parcourt tous les sommets
		for numero,cellule in self.getCellules().items():

			# on récupère les voisins de la cellule courante
			cesVoisins = self.getVoisinsCellule( cellule )

			# on change son numéro de composante connexe
			# car, comme elle est voisine avec cette cellule
			# elles sont toutes deux dans la même composante connexe
			for voisin in cesVoisins:

				if( voisin.getNumero() > numero ):
					composante_des_sommets[ voisin.getNumero() ] = numero

		# on inverse
		# pour chaque numéro de composantes connexes, on y fait correspondre les numéro des sommets qui y sont présents
		composantes = {}
		for key, value in composante_des_sommets.items():
			composantes.setdefault( value, [] ).append( self.getCellule(key) )

		# on retourne la liste des sous graphes ayant ces sommets
		# une composante est un sous graphe du graphe actuel
		return [ self.getSousGraphe(sommets_composante) for sommets_composante in composantes.values()  ]


	# retourne le sous graphe contenant les cellules données en paramètre
	# List<Cellule> listeCellules : la liste des cellules contenu dans le sous graphe
	def getSousGraphe(self, listeCellules):
		
		# on crée un nouveau terrain
		terrain = Terrain()

		# on ajoute les cellules dans ce nouveau terrain
		for cellule in listeCellules:
			terrain.ajouterCellule(cellule)

		# on ajoute les liens reliant les cellules du terrain
		for cellule in listeCellules:
			
			for lien in cellule.getLiens():

				if( lien.getOtherCellule( cellule ) in listeCellules ):
					terrain.ajouterLien(lien)

		return terrain


	# dijkstra ici





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
		liste = []
		for numero,cellule in self.getCellules().items() :
			if( cellule.getCouleurJoueur() == couleurJoueur ):
				liste.append( cellule )
		return liste


	# retourne la liste des cellules du terrain (sous forme d'un dictionnaire)
	def getCellules(self):
		return self.cellules


	# retourne la liste des voisins de la cellule donnée en paramètre
	# lance une exception si on n'enttre autre chose qu'une Cellule
	# lance une exception si la cellule n'appartient pas à ce graphe
	def getVoisinsCellule( self, cellule ):
		
		if( not isinstance( cellule , ce.Cellule ) ):
			raise Exception("le paramètre entrée n'est pas une instance de l'objet Cellule")
		if( cellule not in self.getCellules().values() ):
			raise Exception("cette cellule n'est aps présente dasn ce terrain/graphe")
			
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