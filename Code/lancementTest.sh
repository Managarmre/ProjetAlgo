#!/bin/bash


: '
 
 script bash permettant de lancer le serveur et les 4 bots en même temps
 
 les informations renvoyées serotn sauvegarder dans un dossier log
 
 
 $1 : le port sur lequel le serveur se lancera, si il nest pas précisé, on en choisira un aléatoirement
 
 
'

echo "ATTENTION !!!!! ==> ne marche pour l'instant qu'avec le paramètre 9876"
echo "ATTENTION !!!!! ==> ne marche pas si quelqu'un d'autre est déja en train d'écouter ce port ( si c'est le cas, on vera s'afficher 'ambiguous redirect' )"
echo "========================================================================="

# retoourne un nombre aléatoire entre min et max
# $1 : min
# $2 : max
function aleatoire() {
    
    #
    # verification des paramètres entrée
    #
    if [ -n "$2" ]
    then 
        max=$2
    else 
        max=100
    fi 
    
    if [ -n "$1" ]
    then
        min=$1
    else
        min=0
    fi
    
    # on retourne la valeur aléatoire
    echo $[($RANDOM % ($[$max - $min] + 1)) + $min]

}


# ===========================================
#   variables
# ===========================================


# nom du dossier des logs
dossier_logs=logs


# variables utilisé pour calculé aléatoirement le port ci nécéssaire
portMin=9800
portMax=9999


# numéro du port du serveur
# si il y a un port entrée en paramètre, on prend celui-ci, sinon on en recalcul un aléatoirement
if [ -n "$1" ]
then
    port=$1
else
    port=$(aleatoire $portMin $portMax)
fi


echo "le port de lancement du serveur est : $port"




# ===========================================
#   partie création du dossier des logs
# ===========================================

echo "création du dossiers des logs"
mkdir $dossier_logs 2> /dev/null




# ===========================================
#   partie supression des anciens processus
# ===========================================

echo "supression des anciens processus qui font ****"
kill `ps -aux | grep python3 | awk '{print $2}'` 2> /dev/null



# ===========================================
#   partie lancement des scripts
# ===========================================


# lance un bot (en arrière plan) à l'adresse du serveur avec un certain alias
# $1 : le nom du fichier contenant le bot
# $2 : l'alias du bot
function lancer_un_bot(){
    ./pooobot.py -s 127.0.0.1:$port -b $1 $2 &> ./$dossier_logs/log_$2.txt &
}


# lance 4 bots
function lancer_4_bot(){
    
    for i in 1 2 3 4 ; do
        lancer_un_bot lolipooo c$i
    done
}


# on attent 3 secondes avant de lancer les bots
echo "lancement des bots dans 3 secondes"
( sleep 3 ; lancer_4_bot )&


# lancement du serveur
coproc pp { python3 poooserver.py $port 2> ./$dossier_logs/log_serveur.txt ; echo "ok" ; } # 2> ./$dossier_logs/log_serveur.txt
echo "lancement du serveur"

# on attent 3 seconde, pour que les bots se connectent au serveur
# puis on initialise un match
sleep 3
echo "init" >&${pp[1]}

echo "initialisation d'un match"

echo "fin, regarde les fichiers de logs"
