
import Strategie as st
import Mouvement as mv
import Lien as li

import logging

import random


class StrategieAnalyse( st.Strategie ):
    """
    Cette stratégie analyse le terrain afin de déduire où elle doit envoyer les unités des cellules.

    L'envoi des unités ainsi que leur destination sera déterminée après analyse du terrain.
    Les cellules seront réparties en deux groupes : les productrices et les attaquantes

    """

    def __init__( self, robot ):
        """
        Constructeur de la classe StrategieAleatoire

        :param :class:'Robot' robot: Le robot devant prendre une decision
        """
        st.Strategie.__init__( self, robot )
        
        
    
    def decider(self):
        """
        Retourne la liste des mouvements à effectuer après analyse du terrain pour la prise de décision.

        :returns: la liste des nouveaux mouvements à effectuer 
        :rtype: list of :class:'Mouvement'
        """
        
        terrain = self.getRobot().getTerrain()
        
        mouvements = []
        
        for composante in terrain.getSousGraphe( self.getMesCellules() ).getComposantesConnexes() :
            
            mesCellules = {}
            mesCellules[ "cellules" ] = composante.getCellules().values()
            mesCellules[ "productrices" ] = self.getCellulesProductrices( mesCellules[ "cellules" ] )
            mesCellules[ "attaquantes" ] = self.getCellulesAttaquantes( mesCellules[ "cellules" ] )
            mesCellules[ "attaquantesEnDanger" ] = self.getAttaquantesEnDanger( mesCellules[ "attaquantes" ] )
            mesCellules[ "attaquantesEnSurete" ] = self.getAttaquantesEnSurete( mesCellules[ "attaquantes" ] , mesCellules[ "attaquantesEnDanger" ]  )      
            
            StrategieAnalyse.afficherCellulesLogging( "cellules attaquantes" , mesCellules["attaquantes"] )
            """
            StrategieNormale.afficherCellulesLogging( "mes cellules" , mesCellules["cellules"] )
            StrategieNormale.afficherCellulesLogging( "cellules productrices" , mesCellules["productrices"] )
            StrategieNormale.afficherCellulesLogging( "cellules attaquantes en dangées" , mesCellules["attaquantesEnDanger"] )
            StrategieNormale.afficherCellulesLogging( "cellules attaquantes en suretées" , mesCellules["attaquantesEnSurete"] )
            """
            
            # on envoie les unités des productrices si on a au moins une cellule attaquante
            if( mesCellules[ "attaquantes" ] ):

                mouvements += self.envoyerUnitesProductrices( composante, mesCellules )

            mouvements += self.envoyerUnitesAttaquantes( composante, mesCellules )
                                        
        return mouvements
        

    def envoyerUnitesProductrices( self, composante, mesCellules ):
        """
        Retourne la liste des mouvements correspondant aux mouvements des unités des cellules productrices vers les cellules attaquantes les plus proches.

        :param :class:'Terrain' composante: la partie du terrain (sous graphe) où se trouvent nos cellules
        :param mesCellules: dictionnaire de liste de cellules
        :type mesCellules: dict of list of :class:'Cellule'
        :returns: la liste des mouvements des unités des cellules productrices vers les cellules attaquantes les plus proches.
        :rtype: list of :class:'Mouvement'
        """

        mouvements = []
        productrices = mesCellules[ "productrices" ]

        for productrice in productrices :
                    
            # si on a au moins 10% de la capacité d'attaque de la cellule, on envoie
            if( productrice.getPourcentageAttaque() > 0.10 ):
            
                # utilisation du tableau de dijsktra ici                
                destinations = mesCellules[ "attaquantesEnDanger"] if( mesCellules["attaquantesEnDanger"] ) else mesCellules["attaquantesEnSurete"]
                numero_vers = composante.getCheminVersCellulePlusProche( productrice , destinations )[1]
                    
                vers = composante.getCellule( numero_vers )
                
                nbUnites = productrice.getAttaque() 

                
                mouvement = self.envoyerUnites( productrice, vers, nbUnites )
                mouvements.append( mouvement )

            else:
                pass

        return mouvements


    def envoyerUnitesAttaquantes( self, composante, mesCellules ):
        """
        Retourne la liste des mouvements correspondant aux mouvements des unités des cellules attaquantes vers les cellules ennemies les plus prometteuses.

        :param :class:'Terrain' composante: la partie du terrain (sous graphe) où se trouvent nos cellules
        :param mesCellules: dictionnaire de liste de cellules
        :type mesCellules: dict of list of :class:'Cellule'
        :returns: la liste des mouvements des unités des cellules attaquantes vers les cellules ennemies les plus prometteuses.
        :rtype: list of :class:'Mouvement'
        """

        mouvements = [] 
        attaquantes = mesCellules[ "attaquantes" ]
        
        #   pour l'instant, pas de distinction entre les attaquants
        for attaquante in attaquantes:
    
            logging.info( "Strategie Attaque" )
    
            cellule_cible = self.determinerCible( attaquante )

            if( cellule_cible ):

                a_envoyer = self.nbUnitesAEnvoyer( attaquante, cellule_cible )
                
                logging.info( "{origin} attaque {cible} en envoyant {cell} !".format(origin=attaquante.getNumero(),cible=cellule_cible.getNumero(),cell=a_envoyer) )
        
                if( a_envoyer > 0 ):
                    mon_mouvement = self.envoyerUnites( attaquante, cellule_cible, a_envoyer )
                    mouvements.append( mon_mouvement )
            
        return mouvements 


    def determinerCible( self, attaquante ):
        """
        Dérermine la cible d'une cellule attaquante (en utilisant l'indice P sur tous les voisins ennemies de la cellule attaquante).

        :param :class:'Cellule' attaquante: la cellule attaquante cherchant une cible
        :returns: la cellule cible
        :rtype: :class:'Cellule'
        """

        # recherche de la cible    
        tableau_p = {}
        for ennemi in attaquante.getVoisinsEnnemis() :
            tableau_p.setdefault( self.indiceP(attaquante,ennemi), [] ).append( ennemi )    # calcul indice P de l'ennemie
            # tableau_p[ self.indiceP(ennemi) ] = [ ennemi.getNumero() , ... ]
        
        indice_p_max = max( tableau_p.keys() )
        cellules_possibles = tableau_p[ indice_p_max ]
        
        cellule_cible = cellules_possibles[ random.randint( 0 , len(cellules_possibles)-1 ) ]

        return cellule_cible


    def nbUnitesAEnvoyer( self, attaquante, cellule_cible ):
        """
        Détermine le nombre d'unités à envoyer de la cellule attaquante vers une cellule_cible en fonction de l'excédant de l'attaquant et du cout de la cible 
        Peut renvoyer 0, dans ce cas la, la cellule attaquante ne devra pas envoyer d'unités.

        :param :class:'Cellule' attaquante: la cellule de départ voulant déterminer le nombre d'unités à envoyer 
        :param :class:'Cellule' cellule_cible: la cellule ciblée 
        :returns: le nombre d'unités à envoyer vers la cellule ciblée
        :rtype: int 
        """

        cout_cellule = self.getCoutCellule( cellule_cible )
        excedent = attaquante.getExcedent()
        
        # au départ, aucune unité à envoyer
        a_envoyer = 0

        if( cout_cellule <= 0 ):
            
            if( excedent > 0 ):
                a_envoyer = excedent
            else:
                # cas ou la cellule n'a pas d'excédent
                pass
        
        else:
            
            if( cout_cellule < excedent ):
                a_envoyer = excedent
            
            elif( attaquante.getAttaque() < cout_cellule ):
                
                if( excedent > 0 ):
                    a_envoyer = excedent
                else:
                    logging.info( "j'attends d'être assez grand pour l'attaquer" )
                    # cas ou la cellule n'a pas d'excédent, et ne peut pas non plus attaquer la cellule cible
                    pass
                
            else:
                a_envoyer = cout_cellule

        logging.info( "{exce} {cout_cell} ".format(exce=excedent,cout_cell=cout_cellule) ) 

        return a_envoyer


    def indiceP( self, origine, cellule ):
        """
        Calcule l'indice P d'une cellule par rapport à la cellule d'origine voulant envoyer ses unités.
        
        :param :class:'Cellule' origine: La cellule d'origine
        :param :class:'Cellule' cellule: La cellule dont on veut calculer l'indice P
        :return: l'indice P de la cellule cible
        :rtype: float
        """

        cout = self.getCoutCellule( cellule )
        cout = 1 if cout == 0 else cout        # pour éviter une division par 0
        
        production = cellule.getProduction()
        
        nbVoisins = len( cellule.getVoisins() )
        
        distance = self.getRobot().getTerrain().getLienEntreCellules( origine, cellule ).getDistance()
        
        return production / ( cout * nbVoisins * distance )
    
    
    def getCoutCellule( self, cellule ):
        """
        Calcule le nombre d'unités que l'on doit envoyer sur une cellule ennemie afin de la capturer
        Ce cout peut est négatif si la cellule nous appartient déjà.

        :param :class:'Cellule' cellule: Cellule ennemie
        :eturn: le nombre d'unités nécéssaire à la capture de la cellule
        :rtype: int
        """

        maCouleur = self.getRobot().getMaCouleur()
        couleurCellule = cellule.getCouleur()
        
        coutTotal = cellule.getCout()
        
        for lien in cellule.getLiens():
            
            cellule_adjacente = lien.getOtherCellule(cellule)
            
            for mouvement in lien.getMouvementsVersCellule( cellule ):
                
                couleurMouvement = mouvement.getCouleur()
                
                if( mouvement.aPourCouleur(couleurCellule) ):
                    coutTotal += mouvement.getNbUnites()
                    
                elif( mouvement.aPourCouleur(maCouleur) ):
                    coutTotal -= mouvement.getNbUnites()
                    
                # cas ou plus de deux joueurs, incertain !!
                else:
                    coutTotal -= mouvement.getNbUnites()
                    coutTotal *= -1 if coutTotal < 0 else 1
            
            # si c'est une de mes cellules
            if( cellule_adjacente.aPourCouleur(maCouleur) ):
            
                for mouvement in lien.getMouvementsVersCellule( cellule_adjacente ):
                    
                    # si ce n'est pas l'un de mes mouvement, cela augmente le coût
                    if( not mouvement.aPourCouleur(maCouleur) ):
                        coutTotal += mouvement.getNbUnites()
        
        return coutTotal + 6




    ###### pour l'affichage
    def afficherCellulesLogging( message , cellules ):
        
        liste = [ cellule.getNumero() for cellule in cellules ]
        chaine = message + " : {liste}" 
        logging.info( chaine.format(liste=liste) )
        
        
    
    
    # ==============================================
    #   Fonctions permettant de récupérer mes 
    # cellules full-productrices, semi-productrices...
    # ==============================================
    
    # retourne la liste des cellules m'appartenant
    def getMesCellules( self ):
        """
        Retourne la liste des cellules nous appartenant
        
        :return: les cellules nous appartenant
        :rtype: list of :class:'Cellule'
        """
        return self.getRobot().getTerrain().getCellulesJoueur( self.getRobot().getMaCouleur() )
        
    
    def getCellulesProductrices( self, mesCellules ):
        """
        Retourne la liste des cellules productrices.
        Une cellule est productrice si elle n'est reliée à aucun ennemi.
        
        :param mesCellules: nos cellules productrices
        :type mesCellules: list of :class:'Cellule'
        :rtype: list of :class:'Cellule'
        """

        maCouleur = self.getRobot().getMaCouleur()
        return [ cellule for cellule in mesCellules if all( [ voisin.aPourCouleur( maCouleur ) for voisin in cellule.getVoisins() ] ) ]
    
    
    def getCellulesAttaquantes( self, mesCellules ):
        """
        Retourne la liste de nos cellules attaquantes.
        Une cellule est attaquante si elle est reliée à au moins un ennemi.
        
        :param mesCellules: nos cellules attaquantes
        :type mesCellules: list of :class:'Cellule'
        :rtype: list of :class:'Cellule'
        """
        # correspond à : mesCellules - productrices
        #return list( set(mesCellules) - set(productrices) )

        maCouleur = self.getRobot().getMaCouleur()
        return [ cellule for cellule in mesCellules if any( [ not voisin.aPourCouleur( maCouleur ) for voisin in cellule.getVoisins() ] ) ]
    
             
    def getSemiProductrices( self, productrices, attaquantes ):
        """
        Retourne la liste de nos cellules semi-productrices.
        Une cellule est semi-productrice si c'est une cellule productrice reliée à au moins une cellule attaquante
        
        :returns: nos cellules semi-productrice
        :rtype: list of :class:'Cellule'
        """
        return [ cellule for cellule in productrices if any( [ voisin in attaquantes for voisin in cellule.getVoisins() ]  ) ]
    

    def getFullProductrices( self, productrices, semi_productrices ):
        """
        Retourne la liste de nos cellules entièrement productrices (full-productrices).
        Une cellule est full-productrice si c'est une cellule productrice qui n'est reliée à aucune cellule attaquante.
        
        :rtype: list of :class:'Cellule'
        """
        return list( set(productrices) - set(semi_productrices) )
        
        
    def getAttaquantesEnDanger( self, attaquantes ):
        """
        Retourne la liste de nos cellules attaquantes en danger.
        Une cellule attaquante est en danger lorsqu'il y a des unités ennemies se dirigeant vers elle.
        
        :param attaquantes: la liste de toutes nos cellules attaquantes
        :type attaquantes: list of :class:'Cellule'
        :returns: nos cellules attaquantes en danger
        :rtype: list of :class:'Cellule'
        """

        maCouleur = self.getRobot().getMaCouleur()
        
        en_danger = set()
        for cellule in attaquantes:
            
            for lien in cellule.getLiens() :
                
                for mouvement in lien.getMouvementsVersCellule( cellule ) :
                
                    if( not mouvement.aPourCouleur( maCouleur ) ):
                        en_danger.add(cellule)
                
                 
                autre_cellule = lien.getOtherCellule( cellule )
                if( autre_cellule.getAttaque() > cellule.getCout() and not autre_cellule.aPourCouleur(maCouleur) and not autre_cellule.aPourCouleur(-1) ):
                    en_danger.add( cellule )
                
            
        return list( en_danger )
        
    
    def getAttaquantesEnSurete( self , attaquantes , attaquantes_en_dangers ):
        """
        Retourne la liste de nos cellules attaquantes en sûreté
        
        :rtype: list of :class:'Cellule'
        """
        return list( set(attaquantes) - set(attaquantes_en_dangers) )