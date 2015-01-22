
import tkinter as tk
import logging
import math

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
		self.mouvements_graphique = []

		self.fenetre = tk.Tk()
		self.canvas = tk.Canvas( self.fenetre, width=800, height=800, borderwidth=0, highlightthickness=0, bg="white" )
		self.canvas.pack()

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

		ux, uy = self.getTrueCoordonneeCellule( u )
		vx, vy = self.getTrueCoordonneeCellule( v )

		self.canvas.create_line( ux , uy , vx , vy, fill="black" )
	        
		pass




	def dessinerMouvements( self ):

		for id_mouv in self.mouvements_graphique:
			self.canvas.delete( id_mouv )

		for mouv in self.terrain.mouvements:
			self.dessinerMouvement( mouv )



	def dessinerMouvement( self, mouvement ):


		couleur = self.listeCouleur[ mouvement.getCouleurJoueur() ]

		

		xa, ya = self.getTrueCoordonneeCellule( mouvement.toCellule() )
		xb, yb = self.getTrueCoordonneeCellule( mouvement.fromCellule() )

		coeff = mouvement.getTempsRestant() / mouvement.getDistance()

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



