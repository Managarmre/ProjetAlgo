
from Cellule import *
from Lien import *


# le terrain du jeu
# représente un graphe
class Terrain:

	def __init__( self ):

		# la liste des cellules du terrain (représentent des sommets)
		# comme un numéro de cellule n'identifie qu'une seule cellule, on l'utilise pour retrouver la cellule
		self.cellules = {}

		# la liste des liens du terrain (représentent des arêtes)
		self.liens = {}

		# on utilise ici des dictionnaires (équivalent des hashmap en python)



	# ajoute une cellule dans le graphe
	# Cellule cellule : la cellule à ajouter
	def ajouterCellule(self, cellule):
		# comme un numéro de cellule n'identifie qu'une seule cellule, on l'utilise pour retrouver la cellule
		self.cellules[ cellule.getNumero() ] = cellule
	

	# ajoute un lien entre deux cellules
	# Cellule cellule1
	# Cellule cellule2
	# Int distance
	def ajouterLien(self, cellule1, cellule2, distance = 1):
		lien = Lien( cellule1, cellule2, distance )
		self.liens[ lien.hash() ] = lien



	def getSousGraphe(self, listeCellules):
		terrain = Terrain()

		for cellule in listeCellules:
			terrain.ajouterCellule(cellule)

		# => il manque les liens des cellules

		return terrain


	# dijkstra ici


	# ????????????????????????????? ==> problème si la cellule n'est pas dans le graphe
	# retourne la cellule du graphe ayant le numéro associé
	# Int numero : le numéro de la cellule recherchée
	def getCellule(self, numero):
		return self.cellules[ numero ]


	def getCellulesJoueur(self, couleurJoueur):
		liste = []
		for cellule in self.getCellules():
			if( cellule.getCouleurJoueur() == couleurJoueur ):
				liste.append( cellule )
		return liste

	# retourne la liste des cellules du terrain
	def getCellules(self):
		return self.cellules.values()

	# retourne la liste des liens du terrain
	def getLiens(self):
		return self.liens.values()


	def getNbCellules(self):
		return len(self.cellules)

	def getNbLiens(self):
		return len(self.liens)



	def toString(self):

		chaine = "S = { "

		for numero_cellule, cellule in self.cellules.items():
			chaine += str(numero_cellule) + " ; "

		chaine += "}" + "\n" + "A = { "

		for numero_lien, lien in self.liens.items():
			chaine += "\n" + lien.toString()

		return chaine + "\n}"