
import unittest

from Cellule import *

# on en a besoin pour tester la fonction 'ajouterLien'
from Lien import *

class TestCellule(unittest.TestCase):
    
    # appelée avant chaque cas de test
    def setUp(self):
        
        # on crée la cellule qui sera testée
        self.cellule = Cellule( numero = 1, attaque = 0, defense = 0, attaqueMax = 10, defenseMax = 30, production = 3, couleurJoueur = 2, x = 100, y = 100, rayon = 50 )


    def test_init_1(self):
        
        pass
    
    
    
    
    
    # ---------------------- test de la fonction 'setAttaque' ---------------------- 
    
    # un fonctionnement normal
    def test_setAttaque_ok(self):
        valeur = 5
        self.cellule.setAttaque(valeur)
        self.assertEqual( self.cellule.getAttaque() , valeur )
    
    # entrée d'une valeur non entière
    # excpetion attendue
    def test_setAttaque_pasEntier(self):
        self.assertRaises( Exception, self.cellule.setAttaque, "Test" )
    
    # entrée d'une valeur négative
    # excpetion attendue
    def test_setAttaque_negatif(self):
        self.assertRaises( Exception, self.cellule.setAttaque, -1 )
        
    # entrée d'une valeur trop grande
    # excpetion attendue
    def test_setAttaque_tropGrand(self):
        valeur = self.cellule.getAttaqueMax() + 1
        self.assertRaises( Exception, self.cellule.setAttaque, valeur )
        
        
        
        
    
    # ---------------------- test de la fonction 'setDefence' ---------------------- 

    # un fonctionnement normal
    def test_setDefense_ok(self):
        valeur = 7
        self.cellule.setDefense(valeur)
        self.assertEqual( self.cellule.getDefense() , valeur )
    
    # entrée d'une valeur non entière
    # excpetion attendue
    def test_setDefense_pasEntier(self):
        self.assertRaises( Exception, self.cellule.setDefense, "Test autre" )
    
    # entrée d'une valeur négative
    # excpetion attendue
    def test_setDefense_negatif(self):
        self.assertRaises( Exception, self.cellule.setDefense, -10 )
        
    # entrée d'une valeur trop grande
    # excpetion attendue
    def test_setDefense_tropGrand(self):
        valeur = self.cellule.getDefenseMax() + 36
        self.assertRaises( Exception, self.cellule.setDefense, valeur )
      




    # ---------------------- test de la fonction 'setCouleurJoueur' ---------------------- 

    # un fonctionnement normal
    def test_setCouleurJoueur_ok(self):
        valeur = 2
        self.cellule.setCouleurJoueur(valeur)
        self.assertEqual( self.cellule.getCouleurJoueur() , valeur )

    # entrée d'une valeur non entière
    # excpetion attendue
    def test_setDefense_pasEntier(self):
        self.assertRaises( Exception, self.cellule.setCouleurJoueur, "pas une couleur" )
    
    # entrée d'une valeur négative
    # excpetion attendue
    def test_setDefense_negatif(self):
        self.assertRaises( Exception, self.cellule.setCouleurJoueur, -9 )




    # ---------------------- test de la fonction 'ajouterLien' ---------------------- 

    # un fonctionnement normale
    def test_ajouterLien_ok(self):
        
        cellule2 = Cellule( numero = 2, attaque = 10, defense = 5, attaqueMax = 20, defenseMax = 30, production = 2, couleurJoueur = 0, x = 10, y = 60, rayon = 40 )
        lien = Lien( self.cellule, cellule2, 666 )
        self.cellule.ajouterLien( lien )
        
        # on regarde si le lien ajouté est bien dans la liste des liens de la cellule
        self.assertIn( lien, self.cellule.liens )

    # ajout d'une valeur autre qu'un Lien
    # exception attendue
    def test_ajouterLien_pasLien(self):
        self.assertRaises( Exception, self.cellule.ajouterLien, "pas un lien" )
    
    # ajouter un lien à une cellule, et dont cette cellule ne fait pas partie de ce lien (donc pas l'un des bords de l'arête)
    # exception attendue
    def test_ajouterLien_pasCellule(self):
        cellule1 = Cellule( numero = 0, attaque = 0, defense = 5, attaqueMax = 25, defenseMax = 30, production = 2, couleurJoueur = 8, x = 10, y = 60, rayon = 45 )
        cellule2 = Cellule( numero = 2, attaque = 10, defense = 8, attaqueMax = 20, defenseMax = 36, production = 4, couleurJoueur = 0, x = 10, y = 60, rayon = 40 )
        lien = Lien( cellule1, cellule2, 99 )
        
        self.assertRaises( Exception, self.cellule.ajouterLien, lien )
    



# permet de voir les résultats des tests lorsque l'on lance ce fichier directement
if __name__ == '__main__':
    unittest.main()