
#from Cellule import *
import Cellule as ce
import Mouvement as mouv

# les liens reliant les cellules du terrain
# représentent les arêtes du graphe
class Lien:

	# Cellule u : une cellule de l'un des bouts du lien
	# Cellule v : l'autre cellule au bout du lien
	# Int distance : la distance séparant les cellules u et v
	def __init__(self, u, v, distance):

		# on vérifie les paramètres
		
		if( not isinstance( u , ce.Cellule ) ):
			raise Exception("le parametre 'u' doit être une cellule")

		if( not isinstance( v , ce.Cellule ) ):
			raise Exception("le paramètre 'v' doit être une cellule")
			
		if( not isinstance( distance , int ) ):
			raise Exception("le paramètre 'distance' doit être de type Entier")
		


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


	# retourne la cellule enregistrée sous U
	# return : Cellule
	def getU(self):
		return self.u

	# retourne la cellule enregistrée sous V
	# return : Cellule
	def getV(self):
		return self.v

	# retourne la longueur du lien (la distance entre les deux cellules)
	# return : Integer
	def getDistance(self):
		return self.distance


	# retourne l'autre cellule, si l'on donne U, on retourne V, et vise et versa
	def getOtherCellule( self, cellule_inconnue ):
		if( cellule_inconnue == self.getU() ):
			return self.getV()
		elif( cellule_inconnue == self.getV() ):
			return self.getU() 
		else:
			raise Exception("Cette cellule n'est pas présente sur ce lien....")
			
		
	# ajoute un mouvement VERS la cellule enregistrée sous V
	# Mouvement mouvement : le mouvement à ajouter
	def ajouterMouvementVersV( self, mouvement ):
		self.vers_v.append( mouvement )
	
	# ajoute un mouvement VERS la cellule enregistrée sous U
	# Mouvement mouvement : le mouvement à ajouter
	def ajouterMouvementVersU( self, mouvement ):
		self.vers_u.append( mouvement )
	
	
	# ajoute un mouvement VERS la cellule spécifiée
	# si la cellule ne fait pas partie de ce lien, on lance une Exception
	# Cellule cellule : la cellule vers lequel le mouvement est en direction
	# Mouvement mouvement : le mouvement à ajouter
	def ajouterMouvementVersCellule( self, cellule , mouvement ):
		
		# on vérifie les types des paramètres entrés
		if( not isinstance( cellule , ce.Cellule ) ):
			raise Exception("le paramètre 'cellule' doit être une instance de l'objet Cellule")
		
		if( not isinstance( mouvement , mouv.Mouvement ) ):
			raise Exception("le parametre 'mouvement' doit petre une instance de l'objet Mouvement")
		
		
		# on vérifie que la cellule est bien l'un des bords du lien
		if( cellule == self.getU() ): 		# si c'est U
			self.ajouterMouvementVersU(mouvement)
			
		elif( cellule == self.getV() ): 	# si c'est V
			self.ajouterMouvementVersV(mouvement)
			
		else:
			raise Exception("la cellule spécifiée ne fait pas partie de ce lien (ajouterMouvementCellule)")
	

	
	
	
	# vide la liste des mouvements vers V
	def clearVersV( self ):
		self.vers_v = []
		
	# vide la liste des mouvements vers U
	def clearVersU( self ):
		self.vers_u = []
	
	# supprime tous les mouvements présents sur ce lien
	def clearAllMouvements( self ):
		self.clearVersU()
		self.clearVersV()
		
		
	
	

	def toString(self):
		return "( " + self.u.toString() + " ; " + self.v.toString() + " ; " + str(self.distance) + " )" 




	# utliser pour ranger les liens dans un dictionnaire
	def hash(self):
		return str( self.u.getNumero() ) + str( self.v.getNumero() )


	# détermine la valeur du hash d'un lien à partir de deux cellules
	# appel : Lien.hashage(...)
	# Cellule cellule1
	# Cellule cellule2
	def hashage(cellule1 , cellule2):
		
		if( not ( isinstance( cellule1 , ce.Cellule ) and isinstance( cellule2 , ce.Cellule ) ) ):
			raise Exception("les deux paramètres doivent être des instances de l'objet Cellule")
		
		n1, n2 = cellule1.getNumero(), cellule2.getNumero()
		if( n1 > n2 ):
			n1, n2 = n2, n1
		return str(n1) + str(n2)