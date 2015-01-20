
import StrategieNormale as stn



class StrategiePrevision( stn.StrategieNormale ):
    
    def __init__( self, robot ):
        stn.StrategieNormale.__init__( self, robot )
        
        
        
    
    

    def envoyerUnitesAttaquantes( self, terrain, composante, mesCellules ):

        mouvements = [] 
        attaquantes = mesCellules[ "attaquantes" ]
        
        #
        #   pour l'instant, pas de distinction entre les attaquants
        # 
        #
        for attaquante in attaquantes:
            
            
            ########################################
            ########################################
            #### PUPUTE DEBUT
            ########################################
            ########################################
    
            #
            #  => recherche si pupute applicable ici
            # stratégie applicable pour les planètes attaquantes safe
            # ici on regarde si une planète voisine est sur le point de se faire prendre
            # si c'est le cas on entre en stratégie "prise de planète"
            
            # initialisation de variables
            dist_mini=-1
            cout_mini=-1
            couleur=-1
            cellule=""
            # pour chaque voisin on récupère le cout de la cellule et sa distance
            for ennemi in attaquante.getVoisinsEnnemis():
                cout_cellule=self.getCoutCellule(ennemi)
                dist_cellule=self.getRobot().getTerrain().getLien(li.Lien.hachage(attaquante,ennemi)).getDistance()
                # si c'est la première cellule que l'on regarde et qu'elle est sur le point de se faire prendre
                # on récupère ses coordonnées et son coût (-cout_cellule => pour le remettre en positif)
                if (dist_mini==-1 and cout_cellule<=0):
                    cout_mini=-cout_cellule
                    dist_mini=dist_cellule
                    couleur=ennemi.getCouleurJoueur()
                    cellule=ennemi
                # sinon on compare les distances
                # si la distance de la cellule est plus petite alors on récupère ses coordonnées et son coût
                # on privilégie la distance
                elif (dist_cellule<dist_mini and cout_cellule<=0):
                    dist_mini=dist_cellule
                    cout_mini=-cout_cellule
                    couleur=ennemi.getCouleurJoueur()
                    cellule=ennemi
                # si deux planètes qui vont se faire prendre sont à la même distance, on compare leur cout
                # on récupère le cout de la cellule la moins couteuse (pas besoin pour la distance car inchangée)
                elif (dist_cellule==dist_mini and (-cout_cellule)<cout_mini and cout_cellule<=0):
                    cout_mini=-cout_cellule
                    couleur=ennemi.getCouleurJoueur()
                    cellule=ennemi
            logging.info( "{exce} et dist mini {dist_mini} ".format(exce=attaquante.getAttaque(),dist_mini=dist_mini) ) 
            # Si on a trouvé un planète dans ce cas là
            if not (dist_mini==-1) and attaquante.getAttaque()>cout_mini:
                logging.info( "Stratégie Pupute" )
                # on récupère les liens de la cellule
                for lien in cellule.getLiens():
                    # on regarde le temps (temps_impact) avant que la planète soit prise 
                    # on récupère le temps le plus grand
                    temps_impact=-1
                    for mouvement in lien.getMouvementVersCellule(cellule):
                        temps_mouvement=mouvement.temps_restant
                        if not (mouvement.aPourCouleur(couleur) and mouvement.aPourCouleur(maCouleur)) and temps_impact<temps_mouvement:
                           temps_impact=temps_mouvement
                    # on compare ce temps avec le temps que nos troupes vont mettre pour atteindre la planète cible (dist_mini)
                    # si dist_mini > Temps_impact
                    if temps_impact<dist_mini and attaquante.getAttaque()>cout_mini:
                        # on envoie nos troupes pour prendre la planète
                        # on envoie le nombre de troupes attaquantes + 10%
                        a_envoyer=int(cout_mini+(cout_mini*30//100))
                        if a_envoyer>attaquante.getAttaque():
                            a_envoyer=attaquante.getAttaque()
                        elif a_envoyer==0:
                            a_envoyer=int(attaquante.getAttaque()//3)+1
    
                        logging.info( "{exce} {cout_cell} ".format(exce=a_envoyer,cout_cell=cout_mini) ) 
                        logging.info( "{origin} attaque {cible} en envoyant {cell} !".format(origin=attaquante.getNumero(),cible=cellule,cell=a_envoyer) )
                            
                        lien = terrain.getLien( li.Lien.hachage(cellule,attaquante) )
                        
                        mon_mouvement = mv.Mouvement( attaquante, cellule, a_envoyer, attaquante.getCouleurJoueur(), lien.getDistance() )
                        mouvements.append( mon_mouvement )
                        
                        lien.ajouterMouvementVersCellule( cellule , mon_mouvement )
                        attaquante.setAttaque( attaquante.getAttaque() - a_envoyer )
                        
                        # on réinitialise les variables
                        dist_mini=-1
                        cout_mini=-1
                        couleur=-1
                        cellule=""
                        
                    # sinon on passe
                    else:
                        pass 
                    
            elif not (dist_mini==-1) and attaquante.getAttaque()<cout_mini:
                pass
                
            ########################################
            ########################################
            #### PUPUTE FIN
            ########################################
            ########################################    
            
            
            elif dist_mini==-1:  
                logging.info( "Strategie Attaque" )
        
        
                # recherche de la cible    
                tableau_p = {}
                for ennemi in attaquante.getVoisinsEnnemis() :
                    tableau_p.setdefault( self.indiceP(attaquante,ennemi), [] ).append( ennemi.getNumero() )
                    # tableau_p[ self.indiceP(ennemi) ] = [ ennemi.getNumero() , ... ]
                
                indice_p_max = max( tableau_p.keys() )
                cellules_possibles = tableau_p[ indice_p_max ]
                
                num_cellule_choisie = cellules_possibles[ random.randint( 0 , len(cellules_possibles)-1 ) ]
                cellule_cible = terrain.getCellule(num_cellule_choisie)
        
                #
                # => si qu'un seul voisin ennemi, j'envoi tout sur lui ?
                #
                # sinon 
                
                cout_cellule = self.getCoutCellule( cellule_cible )
                excedent = attaquante.getExcedent()
                
                if( cout_cellule <= 0 ):
                    
                    if( excedent > 0 ):
                        a_envoyer = excedent
                    else:
                        continue
                
                else:
                    
                    if( cout_cellule < excedent ):
                        a_envoyer = excedent
                    
                    elif( attaquante.getAttaque() < cout_cellule ):
                        
                        if( excedent > 0 ):
                            a_envoyer = excedent
                        else:
                            logging.info( "j'attends d'être assez grand pour l'attaquer" )
                            continue
                        
                    else:
                        a_envoyer = cout_cellule
                    
                logging.info( "{exce} {cout_cell} ".format(exce=excedent,cout_cell=cout_cellule) ) 
                logging.info( "{origin} attaque {cible} en envoyant {cell} !".format(origin=attaquante.getNumero(),cible=num_cellule_choisie,cell=a_envoyer) )
    
                mon_mouvement = self.envoyerUnites( attaquante, cellule_cible, a_envoyer )
                mouvements.append( mon_mouvement )
        return mouvements 