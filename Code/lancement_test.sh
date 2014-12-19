#!/bin/bash

# après avoir lancer un bot ou le serveur, on récupère le pid du processus le lancant (avec $!)
# on le stock dans un fichier

# avant de lancer les bot et serveur, on regarde si on ne doit pas arrêter les anciens processus



# nom du fichier contenant les pid des anciens processus
nomfichier=log_savePID.txt



# ===========================================
#   partie supression des anciens processus
# ===========================================


# si le fichier existe
if [ -e $nomfichier ]
then

    # on tue les anciens processus s'ils sont encore en cours d'exécution
    for ligne in $(cat $nomfichier); do
        kill -9 ligne #2> /dev/null
    done

    # on vide le fichier
    #echo "" > $nomfichier

fi



# ===========================================
#   partie lancement des scripts
# ===========================================


# lance un bot (en arrière plan) à l'adresse du serveur avec un certain alias
# $1 : le nom du fichier contenant le bot
# $2 : l'alias du bot
function lancer_un_bot(){
    ./pooobot.py -s 127.0.0.1:9876 -b $1 $2 &> log_$2.txt &
    echo $!" " >> $nomfichier 
}


# lance 4 bots
function lancer_4_bot(){
    
    for i in 1 2 3 4 ; do
        lancer_un_bot lolipooo c$i
    done
}


# on attent 8 secondes avant de lancer les bots
( sleep 5 && lancer_4_bot )&



# lancement du serveur
python3 poooserver.py &> log_serveur.txt 
echo $$" " >> $nomfichier



# on attent 12 secondes avant d'écrit "init" et de lancer le match
sleep 8
echo "init"
