
import Cellule as ce
import Mouvement as mouv
from Exceptions import LienException


class Lien:
	""" 
	Les liens reliant les cellules du terrain (représentent les arêtes du graphe).
	"""
	

	def __init__(self, u, v, distance):
		"""
		Constructeur de la classe Lien.
		On mettra toujours la cellule ayant le plus petit numéro dans l'attribut u.

		:param :class:'Cellule' u: Une cellule de l'une des extrémités du lien
		:param :class:'Cellule' v: L'autre cellule de l'une des extrémités du lien
		:param int distance: la distance séparant les cellules u et valeur
		:raises :class:'LienException': si la distance est inférieure ou égale à 0
		"""

		# on vérifie les paramètres
		if( not isinstance( u , ce.Cellule ) ):
			raise LienException("le parametre 'u' doit être une cellule")

		if( not isinstance( v , ce.Cellule ) ):
			raise LienException("le paramètre 'v' doit être une cellule")
			
		if( not isinstance( distance , int ) and distance <= 0 ):
			raise LienException("le paramètre 'distance' doit être de type Entier supérieur à 0")
		

		# on mettra toujours la cellule ayant le plus petit numéro en premier
		if( u.getNumero() > v.getNumero() ):
			u, v = v, u

		self.u = u
		self.v = v
		
		# on ajoute ce lien à la liste des liens des cellules
		self.u.ajouterLien( self )
		self.v.ajouterLien( self )
		
		
		self.distance = distance
		
		# liste de Mouvement
		self.vers_u = [] 		# mouvements de V vers U
		self.vers_v = []		# mouvements de U vers V


	def getU(self):
		"""
		Retourne la cellule enregistrée sous l'attribut U
		
		:returns: la cellule enregistrée dans U
		:rtype: :class:'Cellule'
		"""
		return self.u


	def getV(self):
		"""
		Retourne la cellule enregistrée sous l'attribut V
		
		:returns: la cellule enregistrée dans V
		:rtype: :class:'Cellule'
		"""
		return self.v


	def getDistance(self):
		"""
		Retourne la longueur du lien, c'est à dire la distance séparant les deux cellules aux extrémités du lien.
		
		:returns: la longueur du lien
		:rtype: int
		"""
		return self.distance


	# retourne l'autre cellule, si l'on donne U, on retourne V, et vise et versa
	def getOtherCellule( self, cellule_inconnue ):
		"""
		Selon la cellule donnée en paramètre, retourne l'autre cellule du lien (retourne U si on donne V et vice versa).
		
		:raises :class:'LienException': si la cellule inconnue n'appartient pas au lien
		:returns: l'autre cellule du lien
		:rtype: :class:'Cellule'
		"""
		if( cellule_inconnue == self.getU() ):
			return self.getV()
		elif( cellule_inconnue == self.getV() ):
			return self.getU() 
		else:
			raise LienException("Cette cellule n'est pas présente sur ce lien....")
			

	def ajouterMouvementVersV( self, mouvement ):
		"""
		Ajoute un mouvement vers la cellule enregistrée sous V
		
		:param :class:'Mouvement' mouvement: Le mouvement à ajouter.
		"""
		self.vers_v.append( mouvement )
	

	def ajouterMouvementVersU( self, mouvement ):
		"""
		Ajoute un mouvement vers la cellule enregistrée sous U
		
		:param :class:'Mouvement' mouvement: Le mouvement à ajouter
		"""
		self.vers_u.append( mouvement )
	
	
	def ajouterMouvementVersCellule( self, cellule , mouvement ):
		"""
		Ajoute le mouvement passé en paramètre vers la cellule passée en paramètre
		
		:param :class:'Cellule' cellule: La cellule à laquelle on ajoute le mouvement
		:param :class:'Mouvement' mouvement: Le mouvement à ajouter
		:raises :class:'LienException': si la cellule n'appartient pas au lien
		"""

		# on vérifie les types des paramètres entrés
		if( not isinstance( cellule , ce.Cellule ) ):
			raise LienException("le paramètre 'cellule' doit être une instance de l'objet Cellule")
		
		if( not isinstance( mouvement , mouv.Mouvement ) ):
			raise LienException("le parametre 'mouvement' doit petre une instance de l'objet Mouvement")

		
		# on vérifie que la cellule est bien l'un des bords du lien
		if( cellule == self.getU() ): 		# si c'est U
			self.ajouterMouvementVersU(mouvement)
			
		elif( cellule == self.getV() ): 	# si c'est V
			self.ajouterMouvementVersV(mouvement)
			
		else:
			raise LienException("la cellule spécifiée ne fait pas partie de ce lien (ajouterMouvementCellule)")
		
	
	def _clearVersV( self ):
		"""
		Vide la liste des mouvements vers V
		"""
		self.vers_v = []
		

	def _clearVersU( self ):
		"""
		Vide la liste des mouvements vers U
		"""
		self.vers_u = []
	

	def clearAllMouvements( self ):
		"""
		Supprime tous les mouvements présents sur le lien.
		"""
		self._clearVersU()
		self._clearVersV()
		
	
	def getMouvementsVersU(self):
		"""
		Retourne la liste des mouvements allant vers U

		:returns: la liste des mouvements allant vers U
		:rtype: list of :class:'Mouvement'
		"""
		return self.vers_u
	

	def getMouvementsVersV(self):
		"""
		Retourne la liste des mouvements allant vers V

		:returns: la liste des mouvements allant vers V
		:rtype: list of :class:'Mouvement'
		"""
		return self.vers_v
	

	def getMouvementsVersCellule( self, cellule ):
		"""
		Retourne la liste des mouvements allant vers la cellule passée en paramètre.
		
		:param :class:'Cellule' cellule: La cellule dont on veut récupérer les mouvements entrants
		:returns: la liste des mouvements allant vers cette cellule
		:rtype: list of :class:'Mouvement'
		:raises :class:'LienException': si la cellule n'appartient pas au lien
		"""
		# on vérifie les types des paramètres entrés
		if( not isinstance( cellule , ce.Cellule ) ):
			raise LienException("le paramètre 'cellule' doit être une instance de l'objet Cellule")
		
		# on vérifie que la cellule est bien l'un des bords du lien
		if( cellule == self.getU() ): 		# si c'est U
			return self.getMouvementsVersU()
			
		elif( cellule == self.getV() ): 	# si c'est V
			return self.getMouvementsVersV()
			
		else:
			raise LienException("la cellule spécifiée ne fait pas partie de ce lien (ajouterMouvementCellule)")
		

	def celluleAppartientAuLien( self, cellule ):
		"""
		Retourne vrai si la cellule passée en paramètre appartient au lien, faux sinon.
		
		:param :class:'Cellule' cellule: Cellule dont on veut savoir si elle appartient au lien
		:rtype: booleen
		"""
		return cellule == self.getU() or cellule == self.getV() 


	def toString(self):
		"""
		Retourne des informations textuelles sur le lien
		
		:returns: le lien sous forme d'une chaine de caractère
		:rtype: str
		"""
		return "( " + self.u.toString() + " ; " + self.v.toString() + " ; " + str(self.distance) + " )" 


	def hash(self):
		"""
		Utilisée pour ranger les liens dans un dictionnaire
		Retourne la valeur unique qui identifie le lien

		:returns: la valeur unique identifiant le lien.
		:rtype: int
		"""
		return int( str( self.u.getNumero() ) + str( self.v.getNumero() ) )


	def hachage(cellule1 , cellule2):
		"""
		Permet de calculer la valeur unique qui identifie un lien supposé entre deux cellules, 
		Retourne la valeur du hash d'un lien à partir de ces deux cellules.
		
		:param :class:'Cellule' cellule1: la première cellule
		:param :class:'Cellule' cellule2: la deuxième cellule
		:returns: l'identifiant du lien supposé entre les deux cellules
		:rtype: int
		"""

		if( not ( isinstance( cellule1 , ce.Cellule ) and isinstance( cellule2 , ce.Cellule ) ) ):
			raise LienException("les deux paramètres doivent être des instances de l'objet Cellule")
		
		nunero_1, numero_2 = cellule1.getNumero(), cellule2.getNumero()
		if( nunero_1 > numero_2 ):
			nunero_1, numero_2 = numero_2, nunero_1
		return int(  str(nunero_1) + str(numero_2) )
