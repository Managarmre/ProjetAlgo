
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

		# la liste des liens du terrain (représentent des arêtes)
		self.liens = {}

		# on utilise ici des dictionnaires (équivalent des hashmap en python)



	# ajoute une cellule dans le graphe
	# Cellule cellule : la cellule à ajouter
	def ajouterCellule(self, cellule):
		
		if( not isinstance( cellule , ce.Cellule ) ):
			raise Exception("ce n'est pas une instance de l'objet Cellule")
		
		# comme un numéro de cellule n'identifie qu'une seule cellule, on l'utilise pour retrouver la cellule
		self.cellules[ cellule.getNumero() ] = cellule
	

	# ajoute un lien entre deux cellules
	# Cellule cellule1
	# Cellule cellule2
	# Int distance
	def ajouterLien(self, cellule1, cellule2, distance = 1):
		lien = li.Lien( cellule1, cellule2, distance )
		self.liens[ lien.hash() ] = lien


	#
	#
	# ===>>> NON FINI !!!!!
	#
	#
	def getSousGraphe(self, listeCellules):
		terrain = Terrain()

		for cellule in listeCellules:
			terrain.ajouterCellule(cellule)

		# => il manque les liens des cellules

		return terrain


	# dijkstra ici


	# retourne la cellule du graphe ayant le numéro associé
	# si la cellule correspondant à ce numéro n'est pas dans le terrain, une exception est lancée.
	# Int numero : le numéro de la cellule recherchée
	def getCellule(self, numero):
		try:
			return self.cellules[ numero ]
		except Exception:
			raise Exception("il n'y a aucune cellule ayant ce numéro dans ce terrain")


	def getCellulesJoueur(self, couleurJoueur):
		liste = []
		for numero,cellule in self.getCellules().items() :
			if( cellule.getCouleurJoueur() == couleurJoueur ):
				liste.append( cellule )
		return liste

	# retourne la liste des cellules du terrain
	def getCellules(self):
		return self.cellules

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