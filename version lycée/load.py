#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       load.py
#
#       Copyright 2019 Aurélien Bück-Kaeffer
#
#
"""
Cote client
Charge les images
"""

__author__ = [ 'Aurélien Bück-Kaeffer' ]
__mail__ = 'aurelien.buck.kaeffer@gmail.com'
__version__ = '0.0.1'

import os
import pygame
from entites import *

def load_image( SCREEN_SIZE ):     #Importation des images
        image = {}
        
        image[ "fond" ] = pygame.transform.scale( pygame.image.load("Textures/Fond.gif").convert_alpha(), list( SCREEN_SIZE.values() ) )
        image[ "fond_gris" ] = pygame.transform.scale( pygame.image.load("Textures/Fond_gris.png").convert_alpha(), list( SCREEN_SIZE.values() ) )
        image[ "fond_noir" ] = pygame.transform.scale( pygame.image.load("Textures/Fond_noir.png").convert_alpha(), list( SCREEN_SIZE.values() ) )
        image[ "fond_menu" ] = pygame.transform.scale( pygame.image.load("Textures/Fond_menu.png").convert_alpha(), list( SCREEN_SIZE.values() ) )
        image[ "fond_0" ] = pygame.transform.scale( pygame.image.load("Textures/Fond_0.png").convert_alpha(), list( SCREEN_SIZE.values() ) )
        image[ "player" ] = pygame.image.load("Textures/player_.png").convert_alpha()
        image[ "player_dead" ] = pygame.image.load("Textures/player_dead.png").convert_alpha()
        image[ "zombies" ] = pygame.image.load("Textures/zombies.png").convert_alpha()
        image[ "game_over" ] = pygame.transform.scale( pygame.image.load("Textures/game_over.png").convert_alpha(), (round(SCREEN_SIZE[ 'x' ]/2), round(SCREEN_SIZE[ 'y' ]/2) ) )
        image[ 'mur' ] = pygame.transform.scale( pygame.image.load( "Textures/walls/mur.png" ).convert_alpha(), ( round( SCREEN_SIZE[ 'x' ] / 23 + 1 ), round( SCREEN_SIZE[ 'y' ] / 13 + 1 ) ) )
        image[ 'mur_bas' ] = pygame.transform.scale( pygame.image.load( "Textures/walls/mur_bas.png" ).convert_alpha(), ( round( SCREEN_SIZE[ 'x' ] / 23 + 1 ), round( SCREEN_SIZE[ 'y' ] / 13 + 1 ) ) )
        image[ 'mur_bas_droite' ] = pygame.transform.scale( pygame.image.load( "Textures/walls/mur_bas_droite.png" ).convert_alpha(), ( round( SCREEN_SIZE[ 'x' ] / 23 + 1 ), round( SCREEN_SIZE[ 'y' ] / 13 + 1 ) ) )
        image[ 'mur_bas_gauche' ] = pygame.transform.scale( pygame.image.load( "Textures/walls/mur_bas_gauche.png" ).convert_alpha(), ( round( SCREEN_SIZE[ 'x' ] / 23 + 1 ), round( SCREEN_SIZE[ 'y' ] / 13 + 1 ) ) )
        image[ 'mur_bas_droite_gauche' ] = pygame.transform.scale( pygame.image.load( "Textures/walls/mur_bas_droite_gauche.png" ).convert_alpha(), ( round( SCREEN_SIZE[ 'x' ] / 23 + 1 ), round( SCREEN_SIZE[ 'y' ] / 13 + 1 ) ) )
        image[ 'mur_droite' ] = pygame.transform.scale( pygame.image.load( "Textures/walls/mur_droite.png" ).convert_alpha(), ( round( SCREEN_SIZE[ 'x' ] / 23 + 1 ), round( SCREEN_SIZE[ 'y' ] / 13 + 1 ) ) )
        image[ 'mur_droite_gauche' ] = pygame.transform.scale( pygame.image.load( "Textures/walls/mur_droite_gauche.png" ).convert_alpha(), ( round( SCREEN_SIZE[ 'x' ] / 23 + 1 ), round( SCREEN_SIZE[ 'y' ] / 13 + 1 ) ) )
        image[ 'mur_gauche' ] = pygame.transform.scale( pygame.image.load( "Textures/walls/mur_gauche.png" ).convert_alpha(), ( round( SCREEN_SIZE[ 'x' ] / 23 + 1 ), round( SCREEN_SIZE[ 'y' ] / 13 + 1 ) ) )
        image[ 'mur_haut' ] = pygame.transform.scale( pygame.image.load( "Textures/walls/mur_haut.png" ).convert_alpha(), ( round( SCREEN_SIZE[ 'x' ] / 23 + 1 ), round( SCREEN_SIZE[ 'y' ] / 13 + 1 ) ) )
        image[ 'mur_haut_bas' ] = pygame.transform.scale( pygame.image.load( "Textures/walls/mur_haut_bas.png" ).convert_alpha(), ( round( SCREEN_SIZE[ 'x' ] / 23 + 1 ), round( SCREEN_SIZE[ 'y' ] / 13 + 1 ) ) )
        image[ 'mur_haut_bas_droite' ] = pygame.transform.scale( pygame.image.load( "Textures/walls/mur_haut_bas_droite.png" ).convert_alpha(), ( round( SCREEN_SIZE[ 'x' ] / 23 + 1 ), round( SCREEN_SIZE[ 'y' ] / 13 + 1 ) ) )
        image[ 'mur_haut_bas_droite_gauche' ] = pygame.transform.scale( pygame.image.load( "Textures/walls/mur_haut_bas_droite_gauche.png" ).convert_alpha(), ( round( SCREEN_SIZE[ 'x' ] / 23 + 1 ), round( SCREEN_SIZE[ 'y' ] / 13 + 1 ) ) )
        image[ 'mur_haut_bas_gauche' ] = pygame.transform.scale( pygame.image.load( "Textures/walls/mur_haut_bas_gauche.png" ).convert_alpha(), ( round( SCREEN_SIZE[ 'x' ] / 23 + 1 ), round( SCREEN_SIZE[ 'y' ] / 13 + 1 ) ) )
        image[ 'mur_haut_droite' ] = pygame.transform.scale( pygame.image.load( "Textures/walls/mur_haut_droite.png" ).convert_alpha(), ( round( SCREEN_SIZE[ 'x' ] / 23 + 1 ), round( SCREEN_SIZE[ 'y' ] / 13 + 1 ) ) )
        image[ 'mur_haut_droite_gauche' ] = pygame.transform.scale( pygame.image.load( "Textures/walls/mur_haut_droite_gauche.png" ).convert_alpha(), ( round( SCREEN_SIZE[ 'x' ] / 23 + 1 ), round( SCREEN_SIZE[ 'y' ] / 13 + 1 ) ) )
        image[ 'mur_haut_gauche' ] = pygame.transform.scale( pygame.image.load( "Textures/walls/mur_haut_gauche.png" ).convert_alpha(), ( round( SCREEN_SIZE[ 'x' ] / 23 + 1 ), round( SCREEN_SIZE[ 'y' ] / 13 + 1 ) ) )
        image[ "dark" ] = pygame.image.load("Textures/Fond_noir.png").convert_alpha()
        image[ 'R_button' ] = pygame.image.load("Textures/R_button.png").convert_alpha()
        image[ 'retour_menu' ] = pygame.image.load("Textures/retour_menu.png").convert_alpha()

        for x in range(0, 6):
                image[ "blood_%s"%x ] = pygame.image.load("Textures/blood/blood_%s.png"%x).convert_alpha()
        
        return image

def load_sounds():      #importation des sons
        sounds = {}
        
        sounds[ 'hand_gun' ] = pygame.mixer.Sound("Sons/hand_gun.wav")
        
        return sounds

def load_maps( num_de_la_map, taille_cases ): #lis les fichiers de maps et les rends utilisables
                liste_objets = []
                liste_spawners = []
                with open("Maps\\map_%s.txt"%num_de_la_map, "r") as Map:
                        Map = Map.read()
                        Map = Map.split("\n")
                        for y in range( 0, len(Map) ):
                                for x in range( 0, len(Map[y]) ):
                                        pos = {'x' : taille_cases * x, 'y' : taille_cases * y} #position de l'element
                                        taille = { 'x' : taille_cases, 'y' : taille_cases} #taille de l'element
                                        hitbox = pygame.Rect( pos[ 'x' ], pos[ 'y' ], taille[ 'x' ], taille[ 'y' ] ) #hitbox de l'element
                                        if Map[y][x] == "0": # 0 = vide
                                                pass
                                        elif Map[y][x] == "D":
                                                liste_objets.append( terrain( "dark", pos, taille, "dark", hitbox, 1, len(liste_objets), False) )
                                        elif Map[y][x] == "S":
                                                liste_spawners.append( spawner( "spawner", pos, taille, "spawner", hitbox, 1, len(liste_spawners), False) )
                                        elif Map[y][x] == "W": # W = mur
                                                liste_objets.append( terrain( "wall", pos, taille, "walls", hitbox, 1000, len(liste_objets), True) )
                                                ###### Determine l'image du mur en fonction des elements environnents
                                                if x != len( Map[ y ] )-1 and Map[ y ][ x + 1] != 0 and Map[ y ][ x + 1] == 'W':
                                                        if x != 0 and Map[ y ][ x - 1] != 0 and Map[ y ][ x - 1] == 'W':
                                                                if y != len( Map )-1 and Map[ y + 1][ x ] != 0 and Map[ y + 1][ x ] == 'W':
                                                                        if y != 0 and Map[ y - 1][ x ] != 0 and Map[ y - 1][ x ] == 'W':
                                                                                liste_objets[len(liste_objets)-1].set_image( 'mur_haut_bas_droite_gauche' )
                                                                        else:
                                                                                liste_objets[len(liste_objets)-1].set_image( 'mur_bas_droite_gauche' )
                                                                else:
                                                                        if y != 0 and Map[ y - 1][ x ] != 0 and Map[ y - 1][ x ] == 'W':
                                                                                liste_objets[len(liste_objets)-1].set_image( 'mur_haut_droite_gauche' )
                                                                        else:
                                                                                liste_objets[len(liste_objets)-1].set_image( 'mur_droite_gauche' )
                                                        else:
                                                                if y != len( Map )-1 and Map[ y + 1][ x ] != 0 and Map[ y + 1][ x ] == 'W':
                                                                        if y != 0 and Map[ y - 1][ x ] != 0 and Map[ y - 1][ x ] == 'W':
                                                                                liste_objets[len(liste_objets)-1].set_image( 'mur_haut_bas_droite' )
                                                                        else:
                                                                                liste_objets[len(liste_objets)-1].set_image( 'mur_bas_droite' )
                                                                else:
                                                                        if y != 0 and Map[ y - 1][ x ] != 0 and Map[ y - 1][ x ] == 'W':
                                                                                liste_objets[len(liste_objets)-1].set_image( 'mur_haut_droite' )
                                                                        else:
                                                                                liste_objets[len(liste_objets)-1].set_image( 'mur_droite' )
                                                else:
                                                        if x != 0 and Map[ y ][ x - 1] != 0 and Map[ y ][ x - 1] == 'W':
                                                                if y != len( Map )-1 and Map[ y + 1][ x ] != 0 and Map[ y + 1][ x ] == 'W':
                                                                        if y != 0 and Map[ y - 1][ x ] != 0 and Map[ y - 1][ x ] == 'W':
                                                                                liste_objets[len(liste_objets)-1].set_image( 'mur_haut_bas_gauche' )
                                                                        else:
                                                                                liste_objets[len(liste_objets)-1].set_image( 'mur_bas_gauche' )
                                                                else:
                                                                        if y != 0 and Map[ y - 1][ x ] != 0 and Map[ y - 1][ x ] == 'W':
                                                                                liste_objets[len(liste_objets)-1].set_image('mur_haut_gauche' )
                                                                        else:
                                                                                liste_objets[len(liste_objets)-1].set_image('mur_gauche' )
                                                        else:
                                                                if y != len( Map )-1 and Map[ y + 1][ x ] != 0 and Map[ y + 1][ x ] == 'W':
                                                                        if y != 0 and Map[ y - 1][ x ] != 0 and Map[ y - 1][ x ] == 'W':
                                                                                liste_objets[len(liste_objets)-1].set_image( 'mur_haut_bas' )
                                                                        else:
                                                                                liste_objets[len(liste_objets)-1].set_image( 'mur_bas' )
                                                                else:
                                                                        if y != 0 and Map[ y - 1][ x ] != 0 and Map[ y - 1][ x ] == 'W':
                                                                                liste_objets[len(liste_objets)-1].set_image( 'mur_haut' )
                                                                        else:
                                                                                liste_objets[len(liste_objets)-1].set_image( 'mur' )
                return liste_objets, liste_spawners, {'x' : x*taille_cases, 'y' : y*taille_cases}
