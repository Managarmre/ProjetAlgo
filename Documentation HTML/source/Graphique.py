
import tkinter as tk
import logging as logging
import math as math

import Lien as li

class Graphique:
	"""
	Représente L'interface graphique du jeu.

	:param robot: Le robot du jeu
	:type robot: Robot
	"""

	def __init__( self, robot ):

		self.robot = robot
		self.terrain = robot.getTerrain()

		self.listeCouleur = { 	-1 : "grey",
								0 : "green",
								1 : "red",
								2 : "blue",
								3 : "pink"
							}

		self.cellules_graphique = {}
		self.liens_graphique = {}
		self.mouvements_graphique = []


		self.fenetre = tk.Tk()
		self.canvas = tk.Canvas( self.fenetre, width=900, height=800, borderwidth=0, highlightthickness=0, bg="white" )
		self.canvas.pack()

		couleur = self.listeCouleur[ robot.getMaCouleur() ] 
		texte = "ma couleur : {c}".format( c =couleur )

		self.canvas.create_text( 100, 10, text=texte, fill=couleur )

		self.text_size = 20


	def create_circle( self, x, y, r, **kwargs):
		"""
		Créer un cercle dans le canvas

		:param x: La position en X du centre du cercle
		:type x: int
		:param y: La position en Y du centre du cercle
		:type y: int
		:param r: Le rayon du cercle
		:type r: int
		:param **kwargs: Paramètres facultatifs de tkinter pour créer un cercle

		"""
		return self.canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)


	def dessinerCellules( self ):
		"""
		Utilise la méthode "dessinerCellule" pour dessiner l'ensemble des cellules du jeu dans la fenêtre
		"""
		for cellule in self.terrain.getCellules().values():
			self.dessinerCellule( cellule )


	def dessinerCellule( self, cellule ):
		"""
		Permet de dessiner une cellule dans la fenêtre

		:param cellule: La cellule à dessiner
		:type cellule: Cellule
		"""

		x, y = self.getTrueCoordonneeCellule( cellule )

		r = self.getTrueRayonCellule( cellule )

		couleur = self.listeCouleur[ cellule.getCouleur() ]

		chaineNumero = "{num}".format( num=cellule.getNumero() )
		chaineAttaque = "{actuel} / {max}".format( actuel=cellule.getAttaque(), max=cellule.getAttaqueMax() )
		chaineDefense = "{actuel} / {max}".format( actuel=cellule.getDefense(), max=cellule.getDefenseMax() )
		chaineProduction = [ 'I' for _ in range(cellule.getProduction() )]

		cercle_graphique = self.create_circle( x, y, r, fill=couleur )

		numero_graphique = self.canvas.create_text( x, y-40, 	fill="white", text=chaineNumero )
		attaque_graphique = self.canvas.create_text( x, y-20, 	fill="white", text=chaineAttaque )
		defense_graphique = self.canvas.create_text( x, y, 		fill="white", text=chaineDefense )
		production_graphique = self.canvas.create_text( x, y+20, 	fill="white", text=chaineProduction )

		self.cellules_graphique[ cellule.getNumero() ] = { 	"cercle" : cercle_graphique,
													"attaque": attaque_graphique,
													"defense": defense_graphique
												}

		pass


	def dessinerLiens( self ):
		"""
		Utilise la méthode "dessinerLien" pour dessiner l'ensemble des liens sur la fenêtre
		"""
		for lien in self.terrain.getLiens().values():
			self.dessinerLien( lien )


	def dessinerLien( self, lien ):
		"""
		Permet de dessiner un lien dans la fenêtre.

		:param lien: Le lien à dessiner
		:type lien: Lien
		"""

		u = lien.getU()
		v = lien.getV()

		depart = self.decalage_centre_cercle( u, v )
		arrivee = self.decalage_centre_cercle( v, u )

		hachage = li.Lien.hachage(u,v)
		self.liens_graphique[ hachage ] = { u.getNumero() : (depart.x, depart.y),
											v.getNumero() : (arrivee.x, arrivee.y) }

		self.canvas.create_line( depart.x , depart.y , arrivee.x , arrivee.y, fill="black" )
		
		pass


	def decalage_centre_cercle( self,  u, v ):
		"""
		Permet de récupérer le point d'intersection entre le bord du cercle et le lien.

		:param u: La cellule de départ
		:type u: Cellule
		:param v: La cellule d'arrivée
		:type v: Cellule
		"""

		# 
		# AB.AC = ||AB|| x ||AC|| x cos( BAC )
		# 		= ( xb - xa )( yb - ya ) + ( xc - xa )( yb - ya )
		#
		# 
		xa, ya = self.getTrueCoordonneeCellule( u )
		xc, yc = self.getTrueCoordonneeCellule( v )

		rayon_u = self.getTrueRayonCellule( u ) 

		a = Point( xa, ya )
		b = Point( xa + 0 , ya + rayon_u )
		c = Point( xc, yc )

		ab = Vecteur( a, b )
		ac = Vecteur( a, c )

		scalaire_BAC = Vecteur.produitScalaireBAC( ab, ac ) 
		normes = ab.norme() * ac.norme()
		cos_angle_bac = scalaire_BAC / normes

		angle_bac = math.acos( cos_angle_bac )

		# selon si l'on tourne en sens trigo ou horaire
		angle_bac = -angle_bac if ac.x > 0 else angle_bac

		ab.rotation( angle_bac )
		depart = ab.translationPoint( a )

		return depart



	def dessinerMouvements( self ):
		"""
		Utilise la méthode "dessinerMouvement" pour dessiner tous les mouvements en cours du terrain
		"""

		for id_mouv in self.mouvements_graphique:
			self.canvas.delete( id_mouv )

		for mouv in self.terrain.mouvements:
			self.dessinerMouvement( mouv )



	def dessinerMouvement( self, mouvement ):
		"""
		Permet de dessiner un mouvement se déplaçant sur un lien

 		:param mouvement: le mouvement à dessiner
 		:type mouvement: Mouvement
 		"""

		u = mouvement.toCellule()
		v = mouvement.fromCellule() 
		hachage = li.Lien.hachage(u,v)
		xa, ya = self.liens_graphique[ hachage ][ u.getNumero() ]
		xb, yb = self.liens_graphique[ hachage ][ v.getNumero() ]

		couleur = self.listeCouleur[ mouvement.getCouleur() ]

		coeff = mouvement.getTempsRestant() / mouvement.getDistance()

		# vecteur directeur AB
		dist_x = xb - xa
		dist_y = yb - ya

		xm = xa + dist_x * coeff 
		ym = ya + dist_y * coeff 

		chaine = "{units}".format( units=mouvement.getNbUnites() )

		id_mouv = self.canvas.create_text( xm, ym, text=chaine, fill=couleur, font=("Purisa", self.text_size) )

		self.mouvements_graphique.append( id_mouv )

		pass


	def redessinerCellules( self ):
		"""
		Utilise la méthode "redessinerCellule" pour redessiner toutes les cellules suivant l'évolution du jeu.
		"""

		for cellule in self.terrain.getCellules().values():
			self.redessinerCellule( cellule ) 


	def redessinerCellule( self, cellule ):
		"""
 		Permet de redessiner une cellule

 		:param cellule: La cellule à redessiner
 		:type cellule: Cellule
 		"""

		numero = cellule.getNumero() 
		chaineAttaque = "{actuel} / {max}".format( actuel=cellule.getAttaque(), max=cellule.getAttaqueMax() )
		chaineDefense = "{actuel} / {max}".format( actuel=cellule.getDefense(), max=cellule.getDefenseMax() )

		couleur_graphique = self.listeCouleur[ cellule.getCouleur() ]
		cellule_graphique = self.cellules_graphique[ numero ]

		cercle_graphique = cellule_graphique[ "cercle" ]
		attaque_graphique = cellule_graphique[ "attaque" ]
		defense_graphique = cellule_graphique[ "defense" ]

		self.canvas.itemconfigure( cercle_graphique, fill=couleur_graphique )
		self.canvas.itemconfigure( attaque_graphique, text=chaineAttaque )
		self.canvas.itemconfigure( defense_graphique, text=chaineDefense )


	def getTrueCoordonneeCellule( self, cellule ):
		"""
 		Permet d'adapter les coordonnées de la cellule envoyées par le serveur en fonction des dimensions de la fenêtre

 		:param cellule: La cellule à adapter
 		:type cellule: Cellule
 		:rtype: float
 		"""
		return ( cellule.x/15 + 100 , cellule.y/15 + 100 )

	def getTrueRayonCellule( self, cellule ):
		"""
 		Permet d'adapter le rayon de la cellule envoyé par le serveur en fonction des dimensions de la fenêtre

 		:param cellule: La cellule à adapter
 		:type cellule: Cellule

 		:rtype: float
 		"""
		return cellule.rayon / 2.5



class Point:
	"""
	Permet de créer un point aux coordonnées spécifiées en paramètre.
	"""
	def __init__(self, x, y):
		"""
		Constructeur de la classe Point

		:param x: La coordonnée en x du point
		:type x: int
		:param y: La coordonnée en y du point
		:type y: int
		"""
		self.x = x
		self.y = y


class Vecteur:
	"""
 	Permet de représenter un vecteur avec les coordonnées spécifiées en paramètre.
 	"""    

	#         ->
	# vecteur AB
	def __init__( self, a, b ):
		"""
		Constructeur de la classe Vecteur
		:param a: Le premier point du vecteur
		:type point: Point
		:param b: Le second point du vecteur
		:type b: Point
		"""
		self.x = b.x - a.x
		self.y = b.y - a.y 

	def norme( self ):
		"""
 		Calcule la norme du vecteur

 		:rtype: float
 		"""
		return math.sqrt( self.x * self.x + self.y * self.y )


	def rotation( self, angle ):
		"""
 		Rotation d'un vecteur de l'angle passé en paramètre

 		:param angle: l'angle de rotation à appliquer au vecteur (en radians)
 		:type angle: float
 		"""

		cos = math.cos( angle )
		sin = math.sin( angle )

		x = self.x
		y = self.y

		self.x = x * cos - y * sin 
		self.y = x * sin + y * cos 


	def translationPoint( self, point ):
		"""
 		Effectue une translation du point passé en paramètre par rapport au vecteur

 		:param point: Le point à translater
 		:type point: Point

 		:rtype: Point
 		"""
		return Point( self.x + point.x , self.y + point.y )


	def produitScalaireBAC( ab, ac ):
		"""
 		Retourne le produit scalaire des deux vecteurs passés en paramètre

 		:param ab: Le premier vecteur
 		:type ab: Vecteur
 		:param ac: Le second vecteur
 		:type ac: Vecteur
 		:rtype: float
 		"""
		return ab.x*ac.x + ab.y*ac.y 


