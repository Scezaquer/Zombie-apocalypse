#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       serveur.py
#
#       Copyright 2019 Aurélien Bück-Kaeffer
#
#
"""
Serveur
Executer pour host la partie
"""

__author__ = [ 'Aurélien Bück-Kaeffer' ]
__mail__ = 'aurelien.buck.kaeffer@gmail.com'
__version__ = '0.0.1'

################################################################IMPORTATIONS

import socket
import threading
from entites import *
from load import load_maps
import ast
import time
import pygame
import random
from math import atan, sqrt
import os


def main(args):

	# Création du serveur

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 1500))

        reboot = True
        #global liste_joueur, liste_zombies, liste_tirs (variables liste_joueur et liste_zombies superflues, A SUPPRIMER)
        liste_objets = { 'joueurs' : [], 'zombies' : [], 'tirs' : [], 'blood' : [], 'terrain' : [], 'spawner' : []} #dictionnaire contenant tous les objets
        
        num_de_la_map = 0
        
        liste_objets[ 'terrain' ], liste_objets[ 'spawner' ], taille_de_la_map  = load_maps( num_de_la_map, 75 ) #lecture du fichier de la map

	#################################################################THREAD CLIENT

        class ClientThread(threading.Thread):
                def __init__(self, ip, port, clientsocket):
                        threading.Thread.__init__(self)
                        self.ip = ip
                        self.port = port
                        self.clientsocket = clientsocket
                        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port, ))
		
                def run(self):
                        print("connexion de %s %s" % (self.ip, self.port, ))
			
                        with open("scoreboard.txt", "r") as scoreboard:
                                scoreboard = scoreboard.read().split('\n')
                                for x in range(0, len(scoreboard) ):
                                        if scoreboard[x] != '':
                                                scoreboard[x] = ast.literal_eval(scoreboard[x])
                                                scoreboard[x][ 'score' ] = int(scoreboard[x][ 'score' ])
                        
                        usable = "False"          #Vérif si pseudo déjà utilisé (j'utilise pas de booléens car ca fout la merde quand je les envoi, impossible des les convertir de string à bool)
                        while usable == "False":
                                pseudo = self.clientsocket.recv(2048).decode()
                                usable = "True"
                                for x in range(0, len(liste_objets[ 'joueurs' ])):
                                        if liste_objets[ 'joueurs' ][x].get_pseudo() == pseudo:
                                                usable = "False"
                                
                                spr = 0
                                for x in range(0, len(scoreboard)):
                                        try:
                                                if scoreboard[x-spr][ 'pseudo' ] == pseudo:
                                                        usable = "False"
                                        except:
                                                del scoreboard[x - spr]
                                                spr += 1
                                self.clientsocket.send(usable.encode())
                        #Creation des caracteristiques du joueur
                        type = 'player'
                        pos = { 'x' : 2925, 'y' : 1500 }
                        taille = {'x' : 45, 'y' : 45}
                        taille_wall = {'x' : 75, 'y' : 75}
                        image = "player"
                        vitesse = 10
                        hitbox = pygame.Rect( pos[ 'x' ]+2, pos[ 'y' ]+2, taille[ 'x' ]-2, taille[ 'y' ]-2 )
                        health = 1000
                        SCREEN_SIZE = ast.literal_eval( self.clientsocket.recv(2048).decode() ) #Récupération de la taille de l'écran client
                        liste_objets[ 'joueurs' ].append( player( pseudo, type, pos, image, vitesse, hitbox, health, len(liste_objets[ 'joueurs' ]), SCREEN_SIZE ) ) #Création du joueur
                        T_temps = 0
                        cooldown = 1
                        error = 0
                        
                        self.clientsocket.send(str(num_de_la_map).encode())
			
                        #######################################################BOUCLE PRINCIPALE Joueur
                        
                        while reboot:
                                data = self.clientsocket.recv(16384).decode().split("|") #Récupération des input coté client
                                if data != ["reboot"]:
                                        data[5] = int(data[5])
                                        data[6] = int(data[6])
                                        
                                        error = 0
                                        send_data = ""
                                        
                                        for x in range( 0, len(liste_objets[ 'joueurs' ]) ):
                                                if liste_objets[ 'joueurs' ][x].get_pseudo() == pseudo:
                                                        num = x
                                        list_collidable = []
                                        for x in range( 0, len(liste_objets[ 'joueurs' ]) ):
                                                if liste_objets[ 'joueurs' ][x].get_num() != num:
                                                        list_collidable.append(liste_objets[ 'joueurs' ][x])
                                        for x in range(0, len(liste_objets[ 'zombies' ]) ):
                                                list_collidable.append(liste_objets[ 'zombies' ][x])
                                        for x in range(0, len(liste_objets[ 'terrain' ]) ):
                                                if liste_objets[ 'terrain' ][x].get_solide():
                                                        list_collidable.append(liste_objets[ 'terrain' ][x])
                                        if not liste_objets[ 'joueurs' ][num].get_KO():
                                                liste_objets[ 'joueurs' ][num].mouv( data[0], data[1], data[2], data[3], list_collidable ) #Mouvements du joueur
                                        if data[4] == "True": #Si le joueur a L_click, fonction tirs
                                                if time.time() - T_temps > 0.2 and not liste_objets[ 'joueurs' ][num].get_KO(): #si dernier tir remonte a plus de 0.2s et que le joueur n'est pas KO
                                                        liste_terrain = []
                                                        for x in range(0, len(liste_objets[ 'terrain' ])):
                                                                if liste_objets[ 'terrain' ][x].get_pos()['x'] > liste_objets[ 'joueurs' ][num].get_pos()['x'] - 1000  and liste_objets[ 'terrain' ][x].get_pos()['x'] < liste_objets[ 'joueurs' ][num].get_pos()['x'] + 1000 and liste_objets[ 'terrain' ][x].get_pos()['y'] > liste_objets[ 'joueurs' ][num].get_pos()['y'] - 1000 and liste_objets[ 'terrain' ][x].get_pos()['y'] < liste_objets[ 'joueurs' ][num].get_pos()['y'] + 1000:
                                                                        liste_terrain.append( liste_objets[ 'terrain' ][x] )
                                                        data_tir = liste_objets[ 'joueurs' ][num].tir( liste_objets[ 'zombies' ], (data[5], data[6]), 'gun', liste_terrain, taille )
                                                        liste_objets[ 'tirs' ].append( data_tir )
                                                        T_temps = time.time()
                                                        for x in range(0, len(data_tir[3])):
                                                                liste_objets[ str(data_tir[3][x][1]) ][data_tir[3][x][0]].set_health( liste_objets[ str(data_tir[3][x][1]) ][data_tir[3][x][0]].get_health() - 20 )
                                                                if data_tir[3][x][1] == 'zombies':
                                                                        liste_objets[ 'blood' ].append( ["blood_%s"%random.randint(0, 5), liste_objets[ 'zombies' ][data_tir[3][x][0]].get_pos(), time.time()] )

                                                        zombies_supprimes = 0
                                                        for x in range(0, len(data_tir[3])):
                                                                if data_tir[3][x][1] == 'zombies' and liste_objets[ 'zombies' ][ data_tir[3][x][0] - zombies_supprimes ].get_health() <= 0: #Supprime les zombies dont la vie < 0
                                                                        del liste_objets[ 'zombies' ][ data_tir[3][x][0] - zombies_supprimes ]
                                                                        zombies_supprimes += 1
                                                                        for y in range(len(liste_objets[ 'zombies' ])):
                                                                                liste_objets[ 'zombies' ][y].set_num( y )
                                                                        liste_objets[ 'joueurs' ][num].set_score(liste_objets[ 'joueurs' ][num].get_score()+1)
                                        
                                        blood_suppr = 0
                                        for x in range( 0, len(liste_objets[ 'blood' ]) ):
                                                if liste_objets[ 'blood' ][x - blood_suppr][2] + 20 <  time.time():
                                                        del liste_objets[ 'blood' ][x - blood_suppr]
                                                        blood_suppr += 1
                                        
                                        #Calcul de l'angle d'orientation du sprite
                                        if not liste_objets[ 'joueurs' ][num].get_KO():
                                                if liste_objets[ 'joueurs' ][num].get_SCREEN_SIZE()[ 'x' ]/2 - data[5] == 0:
                                                        if liste_objets[ 'joueurs' ][num].get_SCREEN_SIZE()[ 'y' ]/2 > data[6]:
                                                                angle = 270
                                                        else :
                                                                angle = 90
                                                else:
                                                        angle = -1 * atan( (liste_objets[ 'joueurs' ][num].get_SCREEN_SIZE()[ 'y' ]/2-data[6])/(liste_objets[ 'joueurs' ][num].get_SCREEN_SIZE()[ 'x' ]/2-data[5]) ) * 50

                                                        if liste_objets[ 'joueurs' ][num].get_SCREEN_SIZE()[ 'x' ]/2 < data[5]:
                                                                angle -= 180
                                        
                                        liste_objets[ 'joueurs' ][num].set_angle( angle )
                                        #Envoi des donnees au client
                                        send_data += str(taille) + ";" + str(taille_wall) + "|"
                                        for x in range(0, len(liste_objets[ 'blood' ]) ):
                                                send_data += liste_objets[ 'blood' ][x][0] + ";" + str( liste_objets[ 'blood' ][x][1] ) + ";" + str( liste_objets[ 'blood' ][x][2] ) + "|"
                                        for x in range(0, len(liste_objets[ 'joueurs' ])): #Info des joueurs
                                                send_data += str( liste_objets[ 'joueurs' ][x].get_type() ) + ";" + str( liste_objets[ 'joueurs' ][x].get_pos() ) + ";" + str( liste_objets[ 'joueurs' ][x].get_health() ) + ";" + str( liste_objets[ 'joueurs' ][x].get_pseudo() ) + ";" + str( liste_objets[ 'joueurs' ][x].get_angle() ) + ";" + str( liste_objets[ 'joueurs' ][x].get_image() ) + "|"
                                                for y in range(0, len(liste_objets[ 'joueurs' ])):
                                                        if liste_objets[ 'joueurs' ][y].get_KO() and sqrt( (liste_objets[ 'joueurs' ][x].get_pos()['x']-liste_objets[ 'joueurs' ][y].get_pos()['x'])**2 + (liste_objets[ 'joueurs' ][x].get_pos()['y']-liste_objets[ 'joueurs' ][y].get_pos()['y'])**2) <= 50:
                                                                send_data += 'R-button' + ';' + str( {'x' : liste_objets[ 'joueurs' ][x].get_pos()['x'] + 30, 'y' : liste_objets[ 'joueurs' ][x].get_pos()['y'] - 16} ) + ';' + str({ 'x' : 16, 'y' : 16}) + ';' + "R_button" + '|'
                                        for x in range(0, len(liste_objets[ 'zombies' ])): #Info des zombies
                                                if abs(liste_objets[ 'zombies' ][x].get_pos()['x']) > liste_objets[ 'joueurs' ][num].get_pos()['x'] - liste_objets[ 'joueurs' ][num].get_SCREEN_SIZE()['x']/2 - 75 and abs(liste_objets[ 'zombies' ][x].get_pos()['x']) < liste_objets[ 'joueurs' ][num].get_pos()['x'] + liste_objets[ 'joueurs' ][num].get_SCREEN_SIZE()['x']/2  and abs(liste_objets[ 'zombies' ][x].get_pos()['y']) > liste_objets[ 'joueurs' ][num].get_pos()['y'] - liste_objets[ 'joueurs' ][num].get_SCREEN_SIZE()['y']/2 - 75 and abs(liste_objets[ 'zombies' ][x].get_pos()['y']) < liste_objets[ 'joueurs' ][num].get_pos()['y'] + liste_objets[ 'joueurs' ][num].get_SCREEN_SIZE()['y']/2:
                                                        send_data += str( liste_objets[ 'zombies' ][x].get_type() ) + ";" + str( liste_objets[ 'zombies' ][x].get_pos() ) + ";" + ";" + ";" + str( liste_objets[ 'zombies' ][x].get_angle() ) + ";" + str( liste_objets[ 'zombies' ][x].get_image() ) + "|"
                                                        if liste_objets[ 'zombies' ][x].get_health() != 100: #Barres de vies des zombies
                                                                send_data += "health" + ";" + str( liste_objets[ 'zombies' ][x].get_pos() ) + ";" + str( liste_objets[ 'zombies' ][x].get_health()/2 ) + "|"
                                        for x in range(0, len(liste_objets[ 'tirs' ])): #Info des tirs
                                                send_data += str(liste_objets[ 'tirs' ][0][0]) + ';' + str(liste_objets[ 'tirs' ][0][1]) + ';' + str(liste_objets[ 'tirs' ][0][2]) + ';' + str(liste_objets[ 'tirs' ][0][3]) + ";" + "0" + "|"
                                                del liste_objets[ 'tirs' ][0]
                                        for x in range(0, len(liste_objets[ 'terrain' ])): #Elements du terrain
                                                if abs(liste_objets[ 'terrain' ][x].get_pos()['x']) > liste_objets[ 'joueurs' ][num].get_pos()['x'] - liste_objets[ 'joueurs' ][num].get_SCREEN_SIZE()['x']/2 - 75 and abs(liste_objets[ 'terrain' ][x].get_pos()['x']) < liste_objets[ 'joueurs' ][num].get_pos()['x'] + liste_objets[ 'joueurs' ][num].get_SCREEN_SIZE()['x']/2  and abs(liste_objets[ 'terrain' ][x].get_pos()['y']) > liste_objets[ 'joueurs' ][num].get_pos()['y'] - liste_objets[ 'joueurs' ][num].get_SCREEN_SIZE()['y']/2 - 75 and abs(liste_objets[ 'terrain' ][x].get_pos()['y']) < liste_objets[ 'joueurs' ][num].get_pos()['y'] + liste_objets[ 'joueurs' ][num].get_SCREEN_SIZE()['y']/2:
                                                        if liste_objets[ 'terrain' ][x].get_type() == "dark":
                                                                liste_opaque = []
                                                                for y in range(0, len(liste_objets[ 'terrain' ]) ):
                                                                        if liste_objets[ 'terrain' ][y].get_type() != "dark":
                                                                                liste_opaque.append(liste_objets[ 'terrain' ][y])
                                                                if liste_objets[ 'terrain' ][x].get_visible(liste_objets[ 'joueurs' ][num].get_pos(), liste_opaque):
                                                                        send_data += str(liste_objets[ 'terrain' ][x].get_type() ) + ";" + str(liste_objets[ 'terrain' ][x].get_pos() ) + ";" + str(liste_objets[ 'terrain' ][x].get_image() ) + "|"
                                                        else:
                                                                send_data += str(liste_objets[ 'terrain' ][x].get_type() ) + ";" + str(liste_objets[ 'terrain' ][x].get_pos() ) + ";" + str(liste_objets[ 'terrain' ][x].get_image() ) + "|"
                                        self.clientsocket.send( send_data.encode() )
                                else:
                                        with open("scoreboard.txt", "a") as scoreboard:
                                                scoreboard.write('\n' + str({ 'pseudo' : liste_objets[ 'joueurs' ][num].get_pseudo(), 'score' : liste_objets[ 'joueurs' ][num].get_score()}) )
                                        for x in range(0, len(liste_objets[ 'joueurs' ])):
                                                liste_objets[ 'joueurs' ][x].set_num( liste_objets[ 'joueurs' ][x].get_num() - 1)
                                        del liste_objets[ 'joueurs' ][num]
                                        print("YEEEEEEEEEEEEEEES")
                                        return False
        
        #################################################################THREAD ZOMBIES
        
        class ZombiesThread(threading.Thread):
                def __init__( self ):
                        threading.Thread.__init__(self)
		
                def run(self):
                        M_temps = 0
                        
                        FPS_MAX = 60			#Limitation des FPS
                        clock = pygame.time.Clock()
                        
                        while reboot: ###BOUCLE PRINCIPALE zombies
                                clock.tick( FPS_MAX )
                                if len(liste_objets[ 'joueurs' ]) != 0:
                                        if time.time() - M_temps > 1 and len(liste_objets[ 'zombies' ])<10:#Si le dernier zombie a spawn il y plus de 1s
                                                M_temps = time.time()
                                                spaw = False #permission de spawn
                                                for x in range(0, len(liste_objets[ 'spawner' ])):
                                                        a = random.randint(0, len(liste_objets[ 'spawner' ])-1 ) #choix d'un spawner aleatoire
                                                        if liste_objets[ 'spawner' ][a].spawn_( liste_objets[ 'zombies' ], liste_objets[ 'joueurs' ] ):
                                                                pos = liste_objets[ 'spawner' ][a].get_pos()
                                                                x = len(liste_objets[ 'spawner' ])
                                                                spawn = True
                                                if spawn: #si un spawner dispo a ete trouve
                                                        #caracteristiques du zombie
                                                        type = 'zombie'
                                                        taille = { 'x' : 45, 'y' : 45}
                                                        image = "zombies"
                                                        vitesse = 5
                                                        hitbox = pygame.Rect( pos[ 'x' ]+2, pos[ 'y' ]+2, taille[ 'x' ]-2, taille[ 'y' ]-2 )
                                                        health = 100
                                                        trigger_range = 2000
                                                        num = len(liste_objets[ 'zombies' ])
                                                        #creation du zombie
                                                        liste_objets[ 'zombies' ].append( zombies( type, pos, image, vitesse, hitbox, health, num, trigger_range) )
                                        for x in range(0, len(liste_objets[ 'zombies' ])):
                                                list_collidable = []
                                                list_joueurs = []
                                                for y in range( 0, len(liste_objets[ 'joueurs' ]) ):
                                                        if liste_objets[ 'joueurs' ][y].get_KO()  == False:
                                                                list_joueurs.append(liste_objets[ 'joueurs' ][y])
                                                for y in range( 0, len(liste_objets[ 'joueurs' ]) ):
                                                        list_collidable.append(liste_objets[ 'joueurs' ][y])
                                                for y in range(0, len(liste_objets[ 'zombies' ]) ):
                                                        try:
                                                                if liste_objets[ 'zombies' ][y].get_num() != liste_objets[ 'zombies' ][x].get_num():
                                                                        list_collidable.append(liste_objets[ 'zombies' ][y])
                                                        except:
                                                                pass
                                                for y in range(0, len(liste_objets[ 'terrain' ]) ):
                                                        if liste_objets[ 'terrain' ][y].get_solide():
                                                                list_collidable.append(liste_objets[ 'terrain' ][y])
                                                try:
                                                        liste_objets[ 'zombies' ][x].mouv( list_joueurs, list_collidable ) #Deplacement des zombies
                                                        liste_objets[ 'zombies' ][x].orientation() #Orientation des sprites
                                                except:
                                                        pass
                                

	########################################################BOUCLE PRINCIPALE #1

        zombiethread = ZombiesThread() # Création du thread pour les zombies
        zombiethread.start()
                
        while reboot:
                server.listen() 				# Attente de clients
                print("En attente de clients...")
                (clientsocket, (ip, port)) = server.accept()
                

                print('yes')
                if liste_objets[ 'joueurs' ] == []:
                        liste_objets = { 'joueurs' : [], 'zombies' : [], 'tirs' : [], 'blood' : [], 'terrain' : [], 'spawner' : []} #dictionnaire contenant tous les objets
                        liste_objets[ 'terrain' ], liste_objets[ 'spawner' ], taille_de_la_map  = load_maps( num_de_la_map, 75 ) #lecture du fichier de la map
		
                newthread = ClientThread(ip, port, clientsocket) # Création du thread pour le nouveau client
                newthread.start()

        
        newthread.stop()
        zombiethread.stop()
        server.close()
	
        return False #Fin de la fonction principale


def run_server():
	import sys
	reboot = True
	while reboot:
		reboot = main(sys.argv)

if __name__ == "__main__":
	import sys
	reboot = True
	while reboot:
		reboot = main(sys.argv)
