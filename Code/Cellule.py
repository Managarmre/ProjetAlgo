
import Lien as li


# une cellule du jeu
# représente un sommet d'un graphe
class Cellule:

	"""
		Int numero : le numéro identifiant la cellule (unique pour chaque cellule)
		Int attaque : le nombre d'unités attaquante sur la cellule actuellement
		Int defense : le nombre d'unités defensive sur la cellule actuellement
		Int attaqueMax : le nombre d'unités attaquante maximal sur la cellule
		Int defenseMax : le nombre d'unités defensive maximal sur la cellule 
		Int production : vitesse de production des unités de la cellule
		Int couleurJoueur: couleur du joueur à qui appartient la cellule (0 si neutre)
		Int x : la coordonnée x de la cellule sur le terrain (graphique)
		Int y : la coordonnée y de la cellule sur le terrain (graphique)
		Int rayon : le rayon de la cellule (graphique)
	"""
	def __init__(self, numero, attaque, defense, attaqueMax, defenseMax, production, couleurJoueur, x, y, rayon):

		

		self.numero = numero
		
		self.attaque = attaque
		self.defense = defense
		self.attaqueMax = attaqueMax
		self.defenseMax = defenseMax
		self.production = production
		
		self.couleurJoueur = couleurJoueur

		# attributs 'graphique' de la cellule
		self.x = x
		self.y = y
		self.rayon = rayon
		
		# la listes des liens sur cette cellule
		self.liens = []

	
	def getNumero(self):
		return self.numero

	def getAttaque(self):
		return self.attaque 

	def getDefense(self):
		return self.defense 

	def getProduction(self):
		return self.production

	def getCouleurJoueur(self):
		return self.couleurJoueur 

	def getAttaqueMax(self):
		return self.attaqueMax 

	def getDefenseMax(self):
		return self.defenseMax 


	def getLiens(self):
		return self.liens



	def setAttaque(self, attaque):
		
		if( not isinstance( attaque , int ) ):
			raise Exception("la valeur entrée n'est pas un entier")
			
		elif( self.getAttaqueMax() < attaque ):
			raise Exception("la valeur de l'attaque est trop grande pour cette cellule (setAttaque), elle doit être inférieur à " + str(self.getAttaqueMax()) ) 
			
		elif( attaque < 0 ):
			raise Exception("la valeur entrée doit être supérieur ou égale à zéro")
			
		self.attaque = attaque



	def setDefense(self, defense):
		
		if( not isinstance( defense , int ) ):
			raise Exception("la valeur entrée n'est pas un entier")
			
		elif( self.getDefenseMax() < defense ):
			raise Exception("la valeur de la defense est trop grande pour cette cellule (setDefense)")
			
		elif( defense < 0 ):
			raise Exception("la valeur entrée doit être suppérieur ou égale à 0")
			
		self.defense = defense 



	def setCouleurJoueur(self, couleurJoueur):
		
		if( not isinstance( couleurJoueur, int ) ):
			raise Excpetion("la couleur d'un joueur doit être un entier")
			
		elif( couleurJoueur < 0 ):
			raise Exception("la couleur d'un joueur doit être suppérieur ou égale à 0")
			
		self.couleurJoueur = couleurJoueur




	# ajoute un lien reliant cette cellule à une autre
	# Lien lien : le lien à ajouté
	def ajouterLien(self, lien):
		
		if( not isinstance( lien, li.Lien ) ):
			raise Exception("la valeur entrée n'est pas une instance de l'objet Lien")
		
		if( lien.getU() != self and lien.getV() != self ):
			raise Exception( "cette cellule n'est pas dans ce lien (ajouterLien)" )
			
		self.liens.append(lien)


	def toString(self):
		return str( self.getNumero() )