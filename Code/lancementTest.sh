#!/bin/bash


#
#   ==> attention !!! 
#
#   ne marche pas lorsqu'il y a déja quelqu'un sur le port 9876 (donc ne marche pas très bien si on lance deux fois à la suite ce fichier)
#

# ===========================================
#   partie création du dossier des logs
# ===========================================

dossier_logs=logs
mkdir $dossier_logs 2> /dev/null


# ===========================================
#   partie supression des anciens processus
# ===========================================

kill `ps -aux | grep python3 | awk '{print $2}'` 2> /dev/null


# ===========================================
#   partie lancement des scripts
# ===========================================


# lance un bot (en arrière plan) à l'adresse du serveur avec un certain alias
# $1 : le nom du fichier contenant le bot
# $2 : l'alias du bot
function lancer_un_bot(){
    ./pooobot.py -s 127.0.0.1:9876 -b $1 $2 &> ./$dossier_logs/log_$2.txt &
}


# lance 4 bots
function lancer_4_bot(){
    
    for i in 1 2 3 4 ; do
        lancer_un_bot lolipooo c$i
    done
}


# on attent 3 secondes avant de lancer les bots
( sleep 3 ; lancer_4_bot )&


# lancement du serveur
#python3 poooserver.py

coproc pp { python3 poooserver.py 2> ./$dossier_logs/log_serveur.txt ; echo "ok" ; } # 2> ./$dossier_logs/log_serveur.txt

sleep 3
echo "init" >&${pp[1]}
