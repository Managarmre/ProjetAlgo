
import tkinter as tk
import logging
import math

import Lien as li

class Graphique:

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
		self.canvas = tk.Canvas( self.fenetre, width=800, height=800, borderwidth=0, highlightthickness=0, bg="white" )
		self.canvas.pack()

		couleur = self.listeCouleur[ robot.getMaCouleur() ] 
		texte = "ma couleur : {c}".format( c =couleur )

		self.canvas.create_text( 100, 10, text=texte, fill=couleur )

		self.text_size = 20


	def create_circle( self, x, y, r, **kwargs):
	    return self.canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)



	def dessinerCellules( self ):
		for cellule in self.terrain.getCellules().values():
			self.dessinerCellule( cellule )


	def dessinerCellule( self, cellule ):

		x, y = self.getTrueCoordonneeCellule( cellule )

		r = cellule.rayon / 1.5

		couleur = self.listeCouleur[ cellule.getCouleurJoueur() ]

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
		for lien in self.terrain.getLiens().values():
			self.dessinerLien( lien )

	def dessinerLien( self, lien ):

		u = lien.getU()
		v = lien.getV()

		depart = self.XXXXX( u, v )
		arrivee = self.XXXXX( v, u )

		hachage = li.Lien.hachage(u,v)
		self.liens_graphique[ hachage ] = { u.getNumero() : (depart.x, depart.y),
											v.getNumero() : (arrivee.x, arrivee.y) }

		self.canvas.create_line( depart.x , depart.y , arrivee.x , arrivee.y, fill="black" )
	    
		pass


	def XXXXX( self,  u, v ):

		# 
		# AB.AC = ||AB|| x ||AC|| x cos( BAC )
		# 		= ( xb - xa )( yb - ya ) + ( xc - xa )( yb - ya )
		#
		# 
		xa, ya = self.getTrueCoordonneeCellule( u )
		xc, yc = self.getTrueCoordonneeCellule( v )

		rayon_u = u.rayon / 1.5

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
		depart = ab.placerSur( a )

		return depart



	def dessinerMouvements( self ):

		for id_mouv in self.mouvements_graphique:
			self.canvas.delete( id_mouv )

		for mouv in self.terrain.mouvements:
			self.dessinerMouvement( mouv )



	def dessinerMouvement( self, mouvement ):

		u = mouvement.toCellule()
		v = mouvement.fromCellule() 
		hachage = li.Lien.hachage(u,v)
		xa, ya = self.liens_graphique[ hachage ][ u.getNumero() ]
		xb, yb = self.liens_graphique[ hachage ][ v.getNumero() ]

		couleur = self.listeCouleur[ mouvement.getCouleurJoueur() ]

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
		for cellule in self.terrain.getCellules().values():
			self.redessinerCellule( cellule ) 


	def redessinerCellule( self, cellule ):

		numero = cellule.getNumero() 
		chaineAttaque = "{actuel} / {max}".format( actuel=cellule.getAttaque(), max=cellule.getAttaqueMax() )
		chaineDefense = "{actuel} / {max}".format( actuel=cellule.getDefense(), max=cellule.getDefenseMax() )

		couleur_graphique = self.listeCouleur[ cellule.getCouleurJoueur() ]
		cellule_graphique = self.cellules_graphique[ numero ]

		cercle_graphique = cellule_graphique[ "cercle" ]
		attaque_graphique = cellule_graphique[ "attaque" ]
		defense_graphique = cellule_graphique[ "defense" ]

		self.canvas.itemconfigure( cercle_graphique, fill=couleur_graphique )
		self.canvas.itemconfigure( attaque_graphique, text=chaineAttaque )
		self.canvas.itemconfigure( defense_graphique, text=chaineDefense )


	def getTrueCoordonneeCellule( self, cellule ):
		return ( cellule.x*60 + 100 , cellule.y*60 + 100 )




class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y


class Vecteur:

	#         ->
	# vecteur AB
	def __init__( self, a, b ):
		self.x = b.x - a.x
		self.y = b.y - a.y 

	def norme( self ):
		return math.sqrt( self.x * self.x + self.y * self.y )


	def rotation( self, angle ):

		cos = math.cos( angle )
		sin = math.sin( angle )

		x = self.x
		y = self.y

		self.x = x * cos - y * sin 
		self.y = x * sin + y * cos 


	def placerSur( self, point ):
		return Point( self.x + point.x , self.y + point.y )


	def produitScalaireBAC( ab, ac ):
		return ab.x*ac.x + ab.y*ac.y 


