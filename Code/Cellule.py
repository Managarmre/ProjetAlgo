
import Lien as li
from Exceptions import CelluleException




class Cellule:
	"""
	Une cellule du jeu. Elle peut être représentée par un sommet dans un graphe.
	"""

	def __init__(self, numero, attaque, defense, attaqueMax, defenseMax, production, couleur, x, y, rayon):
		"""
		Constructeur de la classe Cellule

		:param int numero: le numéro identifiant la cellule (unique pour chaque cellule)
		:param int attaque: le nombre d'unités attaquantes sur la cellule actuellement
		:param int defense: le nombre d'unités defensives sur la cellule actuellement
		:param int attaqueMax: le nombre d'unités attaquantes maximal sur la cellule
		:param int defenseMax: le nombre d'unités defensives maximal sur la cellule
		:param in production: vitesse de production des unités attaquantes de la cellule
		:param int couleur: couleur du joueur à qui appartient la cellule (-1 si neutre)
		:param int x: la coordonnée x de la cellule sur le terrain (graphique)
		:param int y: la coordonnée y de la cellule sur le terrain (graphique)
		:param int rayon: le rayon de la cellule (graphique)

		:returns: une cellule 
		:rtype: class'Cellule'
		:raises :class:'CelluleException': si l'attaque est inférieur à 0 ou supérieur à l'attaque maximale
		:raises :class:'CelluleException': si la défense est inférieur à 0 ou supérieur à la défense maximale
		"""

		# on vérifie les paramètres entrés pour la création de la cellule
		noms = [ "numero", "attaque", "defense", "attaqueMax", "defenseMax", "production", "couleur", "x", "y", "rayon" ]
		valeurs = [ numero, attaque, defense, attaqueMax, defenseMax, production, couleur, x, y, rayon ]
		
		params = { 
				"numero" : numero, 
				"attaque": attaque, 
				"defense": defense, 
				"attaqueMax": attaqueMax, 
				"defenseMax": defenseMax, 
				"production": production, 
				"couleur": couleur, 
				"x": x, 
				"y": y 
		}
		
		for nom_param, valeur_param in params.items():
			if( not isinstance( valeur_param , int ) ):
				raise CelluleException("le paramètre '" + nom_param + "' doit être un entier")
			
			if( nom_param not in [ "x", "y", "couleur" ] and valeur_param < 0 ):
				raise CelluleException("le paramètre '" + nom_param + "' ne peut pas être inférieur à 0")
		
		
		if( attaque > attaqueMax ):
			raise CelluleException("l'attaque de la cellule ne peut pas être supérieure à l'attaque maximale de la cellule")
			
		if( defense > defenseMax ):
			raise CelluleException("la defense de la cellule ne peut pas être supérieure à la defense maximale de la cellule")



		self.numero = numero
		
		self.attaque = attaque
		self.defense = defense
		self.attaqueMax = attaqueMax
		self.defenseMax = defenseMax
		self.production = production
		
		self.couleur = couleur

		# attributs 'graphiques' de la cellule
		self.x = x
		self.y = y
		self.rayon = rayon
		
		# la listes des liens sur cette cellule
		self.liens = []

	
	def getNumero(self):
		"""
		Retourne le numéro unique identifiant la cellule
		
		:returns: le numéro de la cellule
		:rtype: int
		"""
		return self.numero

	def getAttaque(self):
		"""
		Retourne l'attaque actuelle de la cellule.
		
		:returns: l'attaque de la cellule
		:rtype: int
		"""
		return self.attaque 

	def getDefense(self):
		"""
		Retourne la défense actuelle de la cellule.
		
		:returns: la défense de la cellule
		:rtype: int
		"""
		return self.defense 


	def getProduction(self):
		"""
		Retourne la valeur de la cadence de production de la cellule
		
		:returns: la cadence de production de la cellule
		:rtype: int
		"""
		return self.production


	def getCouleur(self):
		"""
		Retourne la couleur de la cellule. Cette couleur correspond à un numéro de joueur supérieur ou égale à -1 (-1 étant la couleur du neutre).
		Cette couleur permet de définir à quel joueur appartient la cellule.

		:returns: la couleur de la cellule
		:rtype: int
		"""
		return self.couleur 


	def getAttaqueMax(self):
		"""
		Retourne la quantité maximale d'unités offensives que la cellule peut contenir
		
		:returns: l'attaque maximale de la cellule
		:rtype: int
		"""
		return self.attaqueMax 


	def getDefenseMax(self):
		"""
		Retourne la quantité maximale d'unités défensives que la cellule peut contenir
		
		:returns: la défense maximale de la cellule
		:rtype: int
		"""
		return self.defenseMax 


	def getLiens(self):
		"""
		Retourne les liens dont cette cellule est lune des extrémités.
		
		:returns: la liste des liens 
		:rtype: liste de :class:'Lien'
        """
		return self.liens

	
	def getVoisins(self):
		"""
		Retourne la liste des cellules voisines à celle-ci.

		ATTENTION, peut renvoyer un résultat différent de la méthode Terrain.getVoisinsCellule( cellule )
		car on ne modifiera jamais la liste des liens de la cellules, 
		contrairement au terrain, ou l'on pourra ne considérer qu'une partie du terrain (un sous graphe), et donc qu'une partie des liens.
		
		:returns: la liste des cellules voisines 
		:rtype: liste de :class:'Cellule'
		"""
		# comme chaque cellule n'est relié qu'au plus 1 seule fois à chaques cellules, pas besoin de vérifier les doublons ici
		return [ lien.getOtherCellule(self) for lien in self.getLiens() ]
	
	
	# retourne la liste des voisins ennemis
	def getVoisinsEnnemis( self ):
		"""
		Retourne la liste des cellules ennemies de cette cellule, c'est à dire celle qui n'ont pas la même couleur que celle de cette cellule.

		:returns: la liste des cellules ennemies de cette cellule 
		:rtype: liste de :class:'Cellule'
		"""
		return [ lien.getOtherCellule(self) for lien in self.getLiens() if not lien.getOtherCellule(self).aPourCouleur( self.getCouleur() ) ]
	

	def getVoisinsAllies( self ):
		"""
		Retourne la liste des cellules alliés de cette cellule, c'est à dire celle qui ont la même couleur que celle de cette cellule.

		:returns: la liste des cellules alliés de cette cellule 
		:rtype: liste de :class:'Cellule'
		"""
		return [ lien.getOtherCellule(self) for lien in self.getLiens() if lien.getOtherCellule(self).aPourCouleur( self.getCouleur() ) ]
	
	
	def getCout(self):
		"""
		Retourne le coût de base de la cellule pour être conquise, c'est à dire le nombre d'unités nécéssaire pour la capturée ( attaque + défense ).
		On ne prends pas en compte les unités présentes sur les liens.
		
		:returns: le coût de la cellule
		:rtype: int
		"""
		return self.getAttaque() + self.getDefense() 
	
	
	def getPourcentageAttaque( self ):
		"""
		Retourne à combien de pourcentage la cellule est pleine.
		1 si l'attaque de la cellule est égale à l'attaque maximale.
		
		:returns: le pourcentage de l'attaque de la cellule
		:rtype: int
		"""
		return self.getAttaque() / self.getAttaqueMax()
	
	
	# ==> a voir avec la production !!!
	def getExcedent( self ):
		"""
		Retourne l'excédent de la cellule. 
		L'excédent correspond au trop plein d'unités que la cellule va produire ou recevoir, et perdre (car elle aura déjà atteint son attaque maximale).
		Seules les unités des mouvements arrivant vers cette cellules avec un temps restant inférieur à 1000 sont prises en comptes.

		:returns: le nombre d'unités excédent
		:rtype: int
		"""

		somme = sum( [ mouvement.getNbUnites() for mouvement in self.getMouvementsVersCellule() if mouvement.aPourCouleur( self.getCouleur() ) and mouvement.getTempsRestant() < 1000 ] )
		
		cellules_produites = self.getProduction()	
		
		if( somme + self.getAttaque() + cellules_produites > self.getAttaqueMax() ):
			
			excedent = somme + self.getAttaque() + cellules_produites - self.getAttaqueMax()
			
			if( excedent > self.getAttaque() ):
				return self.getAttaque()
			else:
				return excedent
			
		else:
			return 0


	def setAttaque(self, attaque):
		"""
		Affecte la valeur de la variable attaque actuelle.
		La nouvelle valeur de l'attaque ne peut pas être inférieur à 0, ni excéder l'attaque maximale de la cellule.
		
		:param int attaque: la nouvelle valeur de l'attaque actuelle de la cellule 
		:raises CelluleException: si l'attaque entrée en paramètre est inférieure à 0 ou supérieur à l'attaque maximale
		"""

		if( not isinstance( attaque , int ) ):
			raise CelluleException("la valeur entrée n'est pas un entier")
			
		elif( self.getAttaqueMax() < attaque ):
			raise CelluleException("la valeur de l'attaque donnée (" , str(attaque) ,") est trop grande pour cette cellule (setAttaque), elle doit être inférieure à " + str(self.getAttaqueMax()) ) 
			
		elif( attaque < 0 ):
			raise CelluleException("la valeur entrée doit être supérieure ou égale à zéro")
			
		self.attaque = attaque
		

	def setDefense(self, defense):
		"""
		Affecte la valeur de la variable defense actuelle.
		La nouvelle valeur de la défense ne peut pas être inférieur à 0, ni excéder la défense maximale de la cellule.
		
		:param int defense: la nouvelle valeur de la défense actuelle de la cellule 
		:raises CelluleException: si la défense entrée en paramètre est inférieure à 0 ou supérieur à la défense maximale
		"""

		if( not isinstance( defense , int ) ):
			raise CelluleException("la valeur entrée n'est pas un entier")
			
		elif( self.getDefenseMax() < defense ):
			raise CelluleException("la valeur de la defense donnée (" , str(defense) ,") est trop grande pour cette cellule (setDefense), elle doit être inférieure à " + str( self.getDefenseMax() ) )
			
		elif( defense < 0 ):
			raise CelluleException("la valeur entrée doit être suppérieure ou égale à 0")
			
		self.defense = defense 
		

	def setCouleur(self, couleur):
		"""
		Affecte la valeur de la variable couleur (la cellule change de propriétaire). 
		Cette couleur doit être supérieur ou égale à -1, -1 étant la couleur du joueur neutre.
		
		:param int couleur: la nouvelle couleur de la cellule.
		:raises :class:'CelluleException': si la couleur n'est pas supérieur ou égale à -1. 
		"""

		if( not isinstance( couleur, int ) ):
			raise CelluleException("la couleur d'un joueur doit être un entier")
			
		elif( couleur < -1 ):
			raise CelluleException("la couleur d'un joueur doit être suppérieure ou égale à -1")
			
		self.couleur = couleur


	def ajouterLien(self, lien):
		"""
		Ajoute un lien reliant cette cellule à une autre. 
		
		:param :class:'Lien' lien: le lien à ajouter
		:raises :class:'CelluleException': si cette cellule n'est pas l'une des cellules aux extrémités du lien.
		"""

		if( not isinstance( lien, li.Lien ) ):
			raise CelluleException("la valeur entrée n'est pas une instance de l'objet Lien")
		
		if( not lien.celluleAppartientAuLien( self ) ):
			raise CelluleException( "cette cellule n'est pas dans ce lien (ajouterLien)" )
			
		self.liens.append(lien)

	
	def aPourCouleur( self, couleur ):
		"""
		Retourne vrai si la cellule possède la couleur passée en paramètre, et faux sinon.
		Autrement dit, elle retourne vrai si la cellule appartient au joueur ayant la couleur passée en paramètre.

		:param int couleur: la couleur à vérifier 

		:returns: retourne vrai si la cellule a bien pour couleur la couleur donnée en paramètre, faux sinon.
		:rtype: boolean 
		"""
		return self.couleur == couleur


	def getMouvementsVersCellule( self ):
		"""
		Méthode qui retourne la liste de tous les mouvements allant vers cette cellule.

		:returns: la liste de tous les mouvements allant vers cette cellule.
		:rtype: liste de :class:'Mouvement'
		"""

		liste = []
		for lien in self.getLiens() :
			liste += lien.getMouvementsVersCellule(self)
		return liste


	def _getCoutTotal( self ):
		"""
		Calcul le cout totale de la cellule, c'est à dire le cout actuelle ( attaque + defense ),
		plus toutes les unités des mouvements du joueur propriétaire de cette cellule vers celle-ci,
		moins toutes les unités de tous les autres unités des mouvements vers cette cellule.

		:returns: retourne le cout totale de la cellule
		:rtype: int 
		"""

		couleurCellule = self.getCouleur()
        
		coutTotal = self.getCout()

		for mouvement in self.getMouvementsVersCellule() :

			couleurMouvement = mouvement.getCouleur()

			if( mouvement.aPourCouleur(couleurCellule) ):
				coutTotal += mouvement.getNbUnites()

			else:
				coutTotal -= mouvement.getNbUnites()

		return coutTotal


	def vaEtrePrise( self ):
		"""
		vérifie si la cellule va être conquise par un autre joueur (elle va changer de propriétaire).
		Si c'est le cas, elle retourne True, False sinon.

		:returns: retourne vrai si cette cellule va être conquise par un autre joueur, faux sinon
		:rtype: boolean 
		"""
		return self._getCoutTotal() <= 0


	def toString(self):
		"""
		Représente l'objet sous forme de chaine

		:returns: retourne une chaine de caractère représentant la cellule
		:rtype: str
		"""
		return str( self.getNumero() )
