#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       client.py
#
#       Copyright 2019 Aurélien Bück-Kaeffer
#
#
"""
Programme client
Executer apres avoir execute serveur.py pour s'y connecter
"""

__author__ = [ 'Aurélien Bück-Kaeffer' ]
__mail__ = 'aurelien.buck.kaeffer@gmail.com'
__version__ = '0.0.1'

################################################################ IMPORTATIONS

import socket
import threading
import pygame
import pygame.gfxdraw
from pygame.locals import *
from load import load_image, load_sounds
from tkinter import Tk
import ast
import time

def move (iter, from_, to):
    iter.insert (to, iter.pop (from_) ) 

def main(args):


	################################################################ VARIABLES

	k_up = False          #Variables de conroles du perso
	k_down = False
	k_right = False
	k_left = False
	k_r = False
	k_alt = False
	k_f4 = False
	k_LMouse = False

	reboot = True		#Variables de boucles
	usable = "False"
	usefull_variable = False
	
	with open("scoreboard.txt", "r") as scoreboard:
		scoreboard = scoreboard.read().split('\n')
		spr = 0
		for x in range(0, len(scoreboard) ):
			try:
				scoreboard[x - spr] = ast.literal_eval(scoreboard[x - spr])
				scoreboard[x - spr][ 'score' ] = int(scoreboard[x - spr][ 'score' ])
			except:
				del scoreboard[x - spr]
				spr += 1
		for a in range(0, len(scoreboard) ):
			for x in range(0, len(scoreboard) ):
				for y in range(0, len(scoreboard) ):
					if scoreboard[x] != '' and scoreboard[y] != '':
						if scoreboard[x]['score'] > scoreboard[y]['score']:
							move( scoreboard, x, y )
							y = len(scoreboard)

	############################################################### INTERFACE GRAPHIQUE

	tk = Tk()									#Récup de la taille de l'écran
	SCREEN_SIZE = { 'x' : tk.winfo_screenwidth(), 'y' : tk.winfo_screenheight() }
	
	if SCREEN_SIZE[ 'x' ] > SCREEN_SIZE[ 'y' ]:
		render_distance = SCREEN_SIZE[ 'x' ] #Variables de gameplay
	else:
		SCREEN_SIZE[ 'y' ]
        
	pygame.init()	#Initialisation de pygame
	canvas = pygame.display.set_mode( (SCREEN_SIZE[ 'x' ], SCREEN_SIZE[ 'y' ]), FULLSCREEN )
	pygame.display.flip()

	image = load_image( SCREEN_SIZE )
	sounds = load_sounds()
	
	liste_tirs = []

	FPS_MAX = 60			#Limitation des FPS
	clock = pygame.time.Clock()
	
	font = pygame.font.Font( "Textures/freesansbold.ttf", 20 )
	
	canvas.blit( image[ 'fond' ], (0, 0) ) #Fond
	canvas.blit( image[ 'fond_menu' ], (0, 0) ) #Fond
	pygame.display.flip()
	
	############################################################### Connexion au serveur

	server  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.connect(("127.0.0.1", 1500))
	
	############################################################### RECUP PSEUDO

	while usable != "True":   #Choix pseudo + vérif si utilisé (coté serv) (j'utilise pas de booléens car ca fout la merde quand je les envoi)
		pseudo = ""
		key = ""
		qwerty = "qwertyuiopasdfghjkl;zxcvbnm" # Variables servant à transformer les     #
		azerty = "azertyuiopqsdfghjklmwxcvbn," # input qwerty recup par pygame en azerty #
		conversion = str.maketrans( qwerty, azerty )
		shift = False

		while key != "\n":
			canvas.blit( image[ 'fond' ], (0, 0) ) #Fond
			canvas.blit( image[ 'fond_menu' ], (0, 0) ) #Fond
			canvas.blit( font.render( "Entrez votre pseudo : " + pseudo , 1, ( 0, 0, 0 ) ),  ( round(SCREEN_SIZE[ 'x' ]/2 - (70 + 5*len(pseudo) ) ), round(SCREEN_SIZE[ 'y' ]/2) ) )
			canvas.blit( font.render("Auteur: Aurélien Bück-Kaeffer, seconde 2", 1, (0,0,0)), (round(SCREEN_SIZE['x']/2-250), round(SCREEN_SIZE['y']-30)) )
			canvas.blit( font.render("Ce jeu a été entièrement réalisé, que ce soit la programmation ou les graphismes,", 1, (0,0,0)), (round(SCREEN_SIZE['x']/2 - 400),round(SCREEN_SIZE['y']*4/5) ) )
			canvas.blit( font.render("par un élève de seconde, bénévolement et durant son temps libre. Soyez indulgents!", 1, (0,0,0)), (round(SCREEN_SIZE['x']/2 - 400),round(SCREEN_SIZE['y']*4/5+20) ) )
			for x in range(0, min(len(scoreboard), 5) ):
				canvas.blit( font.render("%s: %s : %s kills"%( x + 1, scoreboard[x]['pseudo'], scoreboard[x]['score'] ) , 1, (0,0,0)), (round(SCREEN_SIZE[ 'x' ]*2/5), round(SCREEN_SIZE[ 'y' ]*2/3 + 20*x) ) )
			if usable == "False" and usefull_variable:
				canvas.blit( font.render( "Votre pseudo est déjà utilisé, veuillez en choisir un autre" , 1, ( 255, 0, 0 ) ),  ( round(SCREEN_SIZE[ 'x' ]/2 - 295 ), round(SCREEN_SIZE[ 'y' ]/2 + 100) ) )
			pygame.display.flip()
			for event in pygame.event.get(): #Recup des input
				if event.type == pygame.KEYDOWN:
					key = pygame.key.name(event.key)
					#Transformation des input en ce qu'ils sont supposes etre
					if key == "space":
						key = " "
					elif key == "backspace":
						key = ""
						pseudo = pseudo[:-1]
					elif key == "return":
						key = "\n"
					elif key == "left shift" or key == "right shift":
						key = ""
						shift = True
					else:
						key = str.translate( key, conversion )
						if shift:
							key = key.upper() #Met en majuscule si shift appuye
					pseudo += key
				if event.type == pygame.KEYUP:
					if pygame.key.name(event.key) == "left shift" or pygame.key.name(event.key) == "right shift":
						shift = False 
		pseudo = pseudo[:-1] #Enleve le "\n" a la fin du pseudo
		if pseudo != "":
			server.send(pseudo.encode())
			usable = server.recv(2048).decode()
			usefull_variable = True
	print("OK")
	
	server.send(str(SCREEN_SIZE).encode())
	num_de_la_map = int(server.recv(2048).decode())
	

	################################################################### BOUCLE PRINCIPALE

	while reboot:           #Boucle principale

		clock.tick( FPS_MAX )   #Limitation des FPS
		
		##################################################### EVENEMENT
		
		for  event  in  pygame.event.get():
				
			if event.type == KEYDOWN:       #       touche appuyee
				if event.key == K_UP or event.key == K_w:
					k_up = True
				if event.key == K_LEFT or event.key == K_a:
					k_left = True
				if event.key == K_DOWN or event.key == K_s:
					k_down = True
				if event.key == K_RIGHT or event.key == K_d:
					k_right = True
				if event.key == K_r:
					k_r = True
				if event.key == K_LALT or event.key == K_RALT:
					k_alt = True
				if event.key == K_F4:
					k_f4 = True
						
			if event.type == MOUSEBUTTONDOWN: # boutton souris appuye
				if event.button == 1:
					k_LMouse = True

			if event.type == KEYUP: #       touche relachee
				if event.key == K_UP or event.key == K_w:
					k_up = False
				if event.key == K_LEFT or event.key == K_a:
					k_left = False
				if event.key == K_DOWN or event.key == K_s:
					k_down = False
				if event.key == K_RIGHT or event.key == K_d:
					k_right = False
				if event.key == K_r:
					k_r = False
				if event.key == K_LALT or event.key == K_RALT:
					k_alt = False
				if event.key == K_F4:
					k_f4 = False
						
				
			if event.type == MOUSEBUTTONUP:# boutton souris relachee
				if event.button == 1:
					k_LMouse = False
						
				
			if event.type == QUIT:  #       fin du programme
				reboot = False
				continue
				
			if k_f4 == True and k_alt == True:
				reboot = False
				continue
		
		############################################################## ENVOI DES INPUT
		
		data = str(k_up) + "|" + str(k_left) + "|" + str(k_down) + "|" + str(k_right) + "|" + str(k_LMouse) + "|" + str(pygame.mouse.get_pos()[0]) + "|" + str(pygame.mouse.get_pos()[1]) + "|" + str(K_r)
		if reboot == False:
			data = "reboot"
		server.send( data.encode() ) 
		
		data = server.recv(327680).decode().split("|") #Récéption des données
		
		######################## Traitement des données recues pour les rendre utilisables
		
		utility_variable_0 = 0
		data[0] = data[0].split(";")
		try:
			size_ent = ast.literal_eval(data[0][0])
			size_wall = ast.literal_eval(data[0][1])
			data = data[:-1]
		except:pass
		
		for x in range( 1, len(data) ): #decoupe les donnees recues
			data[x] = data[x].split(";")
			#traite les donnees differamment en fonction de l'objet qu'elles definissent
			try:
				if data[x][0] != "health": 
					data[x][1] = ast.literal_eval( data[x][1] ) #ast.literal.eval() transforme un string avec le bon format en dictionnaire
				else:
					data[x][1] = ast.literal_eval( data[x][1] )
					data[x][2] = float(data[x][2])
				if data[x][0] == "gun":
					data[x][2] = ast.literal_eval( data[x][2] )
				if data[x][0] == "player":
					data[x][2] = float( data[x][2] )
				if data[x][0] == "player" or data[x][0] == "zombie":
					data[x][4] = float(data[x][4])
				if data[x][0] == 'player' and data[x][3] == pseudo:
					self_ = data[x]
			except:pass
		
		########################################################## AFFICHAGE
		
		
		canvas.blit( image[ 'fond' ], (0, 0) ) #Fond blanc en dessous de tout au cas ou
		#canvas.blit( image[ 'fond_%s'%num_de_la_map ], ( 0  - self_[1][ 'x' ] + SCREEN_SIZE[ 'x' ]/2, 0 - self_[1][ 'y' ] + SCREEN_SIZE[ 'y' ]/2 ) )
		
		supp = 0
		for x in range(1, len(liste_tirs) ): #Affiche les tirs recuperes a la frame precedente
			try:
				if liste_tirs[x][0][4] == "0":
					sounds[ 'hand_gun' ].play()
					liste_tirs[x][0][4] = "1"
				if time.time() > liste_tirs[x - supp][1] + 0.1: #test pour combien de temps ils ont etes affiches, les supprime apres 0.1s
					del liste_tirs[x - supp]
					supp += 1
				else:
					pygame.gfxdraw.line( canvas, round( liste_tirs[x - supp][0][1][ 'x' ] - self_[1][ 'x' ] + SCREEN_SIZE[ 'x' ]/2 ), round( liste_tirs[x - supp][0][1][ 'y' ] - self_[1][ 'y' ] + SCREEN_SIZE[ 'y' ]/2 ), round( liste_tirs[x - supp][0][2][ 'x' ] - self_[1][ 'x' ] + SCREEN_SIZE[ 'x' ]/2 ), round( liste_tirs[x - supp][0][2][ 'y' ] - self_[1][ 'y' ] + SCREEN_SIZE[ 'y' ]/2 ) , [0,0,0] )
			except:pass
		
		for x in range(1, len(data)):
			try:
				if abs( ( data[x][1][ 'x' ] - self_[1][ 'x' ] )**2 + ( data[x][1][ 'y' ] - self_[1][ 'y' ] )**2 ) <= render_distance**2:
					if data[x][0] == 'zombie' or data[x][0] == 'player': #zombies et joueur
						img = pygame.transform.rotate( pygame.transform.scale( image[ data[x][5] ], ( size_ent[ 'x' ], size_ent[ 'y' ] ) ), data[x][4] )
						img_size = img.get_size()
						canvas.blit( img, ( round(data[x][1][ 'x' ] - self_[1][ 'x' ] + SCREEN_SIZE[ 'x' ]/2) - (img_size[0] - round(size_ent[ 'x' ]))/2, round(data[x][1][ 'y' ] - self_[1][ 'y' ] + SCREEN_SIZE[ 'y' ]/2) - (img_size[1] - round(size_ent[ 'y' ]))/2 ) )
					if data[x][0] == 'gun': #tirs
						liste_tirs.append( [data[x], time.time()] )
					if data[x][0] == 'health': #barre de vie PNJ
						pygame.draw.rect( canvas, ( 255-round( data[x][2] * (255/50) ), round( data[x][2] * (255/50) ), 0 ), ( round(data[x][1][ 'x' ] - self_[1][ 'x' ] + SCREEN_SIZE[ 'x' ]/2), round(data[x][1][ 'y' ] - self_[1][ 'y' ] + SCREEN_SIZE[ 'y' ]/2) - 4, round(data[x][2]), 4 ) )
					for y in range(0, 6):
						if data[x][0] == 'blood_%s'%y :
							canvas.blit( pygame.transform.scale( image[ data[x][0] ], ( size_ent[ 'x' ], size_ent[ 'y' ] ) ), ( round(data[x][1][ 'x' ] - self_[1][ 'x' ] + SCREEN_SIZE[ 'x' ]/2), round(data[x][1][ 'y' ] - self_[1][ 'y' ] + SCREEN_SIZE[ 'y' ]/2) ) )
					if data[x][0] == "wall" or data[x][0] == "dark":
						canvas.blit( pygame.transform.scale( image[ data[x][2] ], ( size_wall[ 'x' ], size_wall[ 'y' ] ) ), ( round(data[x][1][ 'x' ] - self_[1][ 'x' ] + SCREEN_SIZE[ 'x' ]/2), round(data[x][1][ 'y' ] - self_[1][ 'y' ] + SCREEN_SIZE[ 'y' ]/2) ) )
			except:pass
		
		#Affichage des barres de vie player et du "GAME OVER"
		
		nbr_player = 0
		
		for x in range(1, len(data)):
			try:
				if data[x][0] == 'player':
					nbr_player += 1
					if data[x][2] <= 0:
						canvas.blit( font.render( data[x][3] , 1, ( 200, 0, 0 ) ),  ( 55, 25 * nbr_player + 2 ) ) #Si un joueur est mort, afficher son pseudo en rouge
						if data[x][3] == pseudo:
							canvas.blit( image[ 'game_over' ], ( round(SCREEN_SIZE[ 'x' ]/4), round(SCREEN_SIZE[ 'y' ]/4) ) ) #Affichage du game over si joueur mort = ce client
							canvas.blit( image[ 'retour_menu' ], ( round(SCREEN_SIZE[ 'x' ]/2  - image[ 'retour_menu' ].get_size()[0]/2), round(SCREEN_SIZE[ 'y' ]*4/5) ) )
							if k_LMouse == True and pygame.mouse.get_pos()[0] > SCREEN_SIZE[ 'x' ]/2  - image[ 'retour_menu' ].get_size()[0]/2 and pygame.mouse.get_pos()[1] > SCREEN_SIZE[ 'y' ]*4/5 and pygame.mouse.get_pos()[0] < SCREEN_SIZE[ 'x' ]/2  - image[ 'retour_menu' ].get_size()[0]/2 + image[ 'retour_menu' ].get_size()[0] and pygame.mouse.get_pos()[1] < SCREEN_SIZE[ 'y' ]*4/5 + image[ 'retour_menu' ].get_size()[1]:
								server.send( "reboot".encode() )
								time.sleep(0.5)
								server.close()
								return True
					else: #Sinon, affichage normal de la barre de vie et du pseudo
						pygame.draw.rect( canvas, ( 255-round( data[x][2] * (255/1000) ), round( data[x][2] * (255/1000) ), 0 ), ( 50, 25 * nbr_player, round(data[x][2]/5), 20 ) )
						canvas.blit( font.render( data[x][3] , 1, ( 0, 0, 0 ) ),  ( 55, 25 * nbr_player + 2 ) )
			except:pass
		pygame.display.flip()
	return False #fin de la fonction main

def run_client():
	import sys
	reboot = True
	while reboot:
		reboot = main(sys.argv)

if __name__ == "__main__":
	import sys
	reboot = True
	while reboot:
		reboot = main(sys.argv)
