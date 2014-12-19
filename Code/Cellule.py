
import Lien as li


# une cellule du jeu
# représente un sommet d'un graphe
class Cellule:

	"""
		Int numero : le numéro identifiant la cellule (unique pour chaque cellule)
		Int attaque : le nombre d'unités attaquantes sur la cellule actuellement
		Int defense : le nombre d'unités defensives sur la cellule actuellement
		Int attaqueMax : le nombre d'unités attaquantes maximal sur la cellule
		Int defenseMax : le nombre d'unités defensives maximal sur la cellule 
		Int production : vitesse de production des unités de la cellule
		Int couleurJoueur: couleur du joueur à qui appartient la cellule (-1 si neutre)
		Int x : la coordonnée x de la cellule sur le terrain (graphique)
		Int y : la coordonnée y de la cellule sur le terrain (graphique)
		Int rayon : le rayon de la cellule (graphique)
	"""
	def __init__(self, numero, attaque, defense, attaqueMax, defenseMax, production, couleurJoueur, x, y, rayon):
		
		# on vérifie les paramètres entrés pour la création de la cellule
		noms = [ "numero", "attaque", "defense", "attaqueMax", "defenseMax", "production", "couleurJoueur", "x", "y", "rayon" ]
		valeurs = [ numero, attaque, defense, attaqueMax, defenseMax, production, couleurJoueur, x, y, rayon ]
		
		params = { 
				"numero" : numero, 
				"attaque": attaque, 
				"defense": defense, 
				"attaqueMax": attaqueMax, 
				"defenseMax": defenseMax, 
				"production": production, 
				"couleurJoueur": couleurJoueur, 
				"x": x, 
				"y": y 
		}
		
		for nom_param, valeur_param in params.items():
			if( not isinstance( valeur_param , int ) ):
				raise Exception("le paramètre '" + nom_param + "' doit être un entier")
			
			if( nom_param not in [ "x", "y", "couleurJoueur" ] and valeur_param < 0 ):
				raise Exception("le paramètre '" + nom_param + "' ne peut pas être inférieur à 0")
		
		
		if( attaque > attaqueMax ):
			raise Exception("l'attaque de la cellule ne peut pas être supérieure à l'attaque maximale de la cellule")
			
		if( defense > defenseMax ):
			raise Exception("la defense de la cellule ne peut pas être supérieure à la defense maximale de la cellule")



		self.numero = numero
		
		self.attaque = attaque
		self.defense = defense
		self.attaqueMax = attaqueMax
		self.defenseMax = defenseMax
		self.production = production
		
		self.couleurJoueur = couleurJoueur

		# attributs 'graphiques' de la cellule
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

	"""
	# retourne la liste de cellules voisines de celle-ci
	def getVoisins(self):
		# comme chaque cellule n'est relié qu'au plus 1 seule fois à chaques cellules, pas besoin de vérifier les doublons ici
		return [ lien.getOtherCellule(self) for lien in self.getLiens() ]
	"""
	
	
	# non fini !!!!!!
	#
	#
	#
	#
	def getCout(self):
		cout_sur_liens = 0 
		
		for lien in self.getLiens():
			
			mouv_vers_cellule = lien.getMouvementVersCellule( self )
			
			for mouvement in mouv_vers_cellule:
				
				coeff = 1 if mouvement.getCouleurJoueur() == cellule.getCouleurJoueur()  else -1
				cout_sur_liens += mouvement.getNbUnites() * coeff
			
		return self.getAttaque() + self.getDefense() + cout_sur_liens + 1
	
	

	def setAttaque(self, attaque):
		
		if( not isinstance( attaque , int ) ):
			raise Exception("la valeur entrée n'est pas un entier")
			
		elif( self.getAttaqueMax() < attaque ):
			raise Exception("la valeur de l'attaque donnée (" , str(attaque) ,") est trop grande pour cette cellule (setAttaque), elle doit être inférieure à " + str(self.getAttaqueMax()) ) 
			
		elif( attaque < 0 ):
			raise Exception("la valeur entrée doit être supérieure ou égale à zéro")
			
		self.attaque = attaque



	def setDefense(self, defense):
		
		if( not isinstance( defense , int ) ):
			raise Exception("la valeur entrée n'est pas un entier")
			
		elif( self.getDefenseMax() < defense ):
			raise Exception("la valeur de la defense donnée (" , str(defense) ,") est trop grande pour cette cellule (setDefense), elle doit être inférieure à " + str( self.getDefenseMax() ) )
			
		elif( defense < 0 ):
			raise Exception("la valeur entrée doit être suppérieure ou égale à 0")
			
		self.defense = defense 



	def setCouleurJoueur(self, couleurJoueur):
		
		if( not isinstance( couleurJoueur, int ) ):
			raise Excpetion("la couleur d'un joueur doit être un entier")
			
		elif( couleurJoueur < 0 ):
			raise Exception("la couleur d'un joueur doit être suppérieure ou égale à 0")
			
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