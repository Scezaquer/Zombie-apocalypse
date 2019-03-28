#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       serveur.py
#
#       Copyright 2019 Aurélien Bück-Kaeffer
#
#
"""
Cote serveur
S'execute pour gerer les entites
"""

__author__ = [ 'Aurélien Bück-Kaeffer' ]
__mail__ = 'aurelien.buck.kaeffer@gmail.com'
__version__ = '0.0.1'

import pygame
from math import atan, sqrt
import time

class objet: #Classe mere regroupant fonctions et caracteristiques communes des classes heritieres
	def __init__ (self, type, pos, image, hitbox, health, num, angle = 0):
		self.type = type
		self.pos = { 'x' : pos[ 'x' ], 'y' : pos[ 'y' ] }
		self.image = image
		self.hitbox = hitbox
		self.health = health
		self.num = num
		self.angle = angle
	
	def set_type ( self, type ):
		"""definis la nature de l'objet"""
		self.type = type
	
	def get_type ( self ):
		"""renvoi la nature de l'objet"""
		return self.type
	
	def set_pos ( self, pos ):
		"""definis la position de l'objet"""
		self.pos = { 'x' : pos[ 'x' ], 'y' : pos[ 'y' ] }
		
	def get_pos ( self ):
		"""renvoie les coordonnes de l'objet"""
		return self.pos

	def set_image ( self, image ):
		"""definis le sprite de l'objet"""
		self.image = image

	def get_image ( self ):
		"""renvoi le sprite de l'objet"""
		return self.image
	
	def set_hitbox ( self, hitbox ):
		"""definis la hitbox de l'objet"""
		self.hitbox = hitbox
		
	def get_hitbox ( self ):
		"""renvoi la hitbox de l'objet"""
		return self.hitbox
	
	def set_health( self, health ):
		"""definis la vie de l'objet"""
		self.health = health
	
	def get_health( self ):
		"""renvoi la vie de l'objet"""
		return self.health
	
	def set_num( self, num ):
		"""definis la pos de l'objet"""
		self.num = num
	
	def get_num( self ):
		"""renvoi la pos de l'objet"""
		return self.num
	
	def set_angle( self, angle ):
		"""definis l'angle de l'objet"""
		self.angle = angle
	
	def get_angle( self ):
		"""renvoi l'angle de l'objet"""
		return self.angle

class player(objet):
	def __init__ (self, pseudo, type, pos, image, vitesse, hitbox, health, num, SCREEN_SIZE, v_up = 0, v_side = 0, KO = False, score = 0):
		objet.__init__(self, type, pos, image, hitbox, health, num)
		self.pseudo = pseudo
		self.vitesse = vitesse
		self.v_up = v_up
		self.v_side = v_side
		self.SCREEN_SIZE = SCREEN_SIZE
		self.KO = KO
		self.score = 0
                
	def set_pseudo ( self, pseudo ):
		"""definis le pseudo du joueur"""
		self.pseudo = pseudo
	
	def get_pseudo ( self ):
		"""renvoi le pseudo du joueur"""
		return self.pseudo
	
	def set_vitesse( self, vitesse ):
		"""definis la vitesse du joueur"""
		self.vitesse = vitesse
		
	def get_vitesse ( self ):
		"""renvoi la vitesse du joueur"""
		return self.vitesse
	
	def set_SCREEN_SIZE( self, SCREEN_SIZE ):
		"""definis la taille de l'ecran du joueur"""
		self.SCREEN_SIZE = SCREEN_SIZE
	
	def get_SCREEN_SIZE( self ):
		"""renvoi la taille de l'ecran du joueur"""
		return self.SCREEN_SIZE
	
	def set_KO( self, time ):
		"""definis l'etat du joueur"""
		self.KO = time
	
	def get_KO( self ):
		"""renvoi le moment ou il a ete mis KO si le joueur est KO, False sinon"""
		return self.KO
	
	def set_score( self, score ):
		"""definis le score"""
		self.score = score
	
	def get_score( self ):
		"""renvoi le score"""
		return self.score
	
	def damage( self, damage ):
		"""diminue la vie du joueur de la valeur entrée"""
		self.health -= damage
		if self.health <= 0:
			self.set_KO( time.time() )
			self.set_image( 'player_dead' )
		
	def mouv ( self, k_up, k_left, k_down, k_right, list_collidable):
		"""fonction de la classe Joueur
		s'occupe des déplacements"""
		pos = self.get_pos()
		#       haut
		if k_up == "True":
			if self.v_up > -1 * self.vitesse:
				self.v_up -= self.vitesse/20
		else:
			if self.v_up < 0:
				self.v_up += self.vitesse/40
			
                #       gauche
		if k_left == "True":
			if self.v_side > -1 * self.vitesse:
				self.v_side -= self.vitesse/20
		else:
			if self.v_side < 0:
				self.v_side += self.vitesse/40
			
                #       bas
		if k_down == "True":
			if self.v_up < self.vitesse:
				self.v_up += self.vitesse/20
		else:
			if self.v_up > 0:
				self.v_up -= self.vitesse/40
			
                #       droite
		if k_right == "True":
			if self.v_side < self.vitesse:
				self.v_side += self.vitesse/20
		else:
			if self.v_side > 0:
				self.v_side -= self.vitesse/40
		
		collision_x = False
		collision_y = False
		#Test de colision de la position future X pour determiner si le deplacement est autorise
		futur_pos_x = self.hitbox.move( round(self.v_side), 0 ) 
		for a in range( 0, len( list_collidable ) ):
				if futur_pos_x.colliderect( list_collidable[a].get_hitbox() ):#Test des collisions avec les zombies
					collision_x = True
					self.v_side = 0
		
		if collision_x == False:#Deplacement si il n'y a pas collision
			self.set_pos( { 'x' : self.pos[ 'x' ] + round(self.v_side), 'y' : self.pos[ 'y' ] } )
			self.hitbox = self.hitbox.move( round(self.v_side), 0 )
			
		#Test de colision de la position future Y pour determiner si le deplacement est autorise
		futur_pos_y = self.hitbox.move( 0, round(self.v_up) )
		for a in range( 0, len( list_collidable ) ):
				if futur_pos_y.colliderect( list_collidable[a].get_hitbox() ):#Test des collisions avec les zombies
					collision_y = True
					self.v_up = 0
		
		if collision_y == False:#Deplacement si il n'y a pas collision
			self.set_pos( { 'x' : self.pos[ 'x' ], 'y' : self.pos[ 'y' ] + round(self.v_up) } )
			self.hitbox = self.hitbox.move( 0, round(self.v_up) )
		
	def tir ( self, liste_zombies, pos_souris, weapon, liste_walls, size_ent ):
		"""fonction de la classe joueur
		s'occupe des tirs"""
		
		if weapon == 'gun':
			portee = 1000
		else:
			portee = 0
		
		hitbox = pygame.Rect( self.pos[ 'x' ] + size_ent[ 'x' ]/2 , self.pos[ 'y' ] + size_ent[ 'y' ]/2 , 1, 1 )
		
		touche = False
		
		trajectoire = [0, 1]
		
		distance = ( ( pos_souris[ 0 ] - self.pos[ 'x' ] )**2 + ( pos_souris[ 1 ] - self.pos[ 'y' ] )**2 )**0.5
		trajectoire[0] = ( pos_souris[ 0 ] - ( round(self.get_SCREEN_SIZE()[ 'x' ]/2 + size_ent[ 'x' ]/2 ) ) ) / distance
		trajectoire[1] = ( pos_souris[ 1 ] - ( round(self.get_SCREEN_SIZE()[ 'y' ]/2 + size_ent[ 'y' ]/2 ) ) ) / distance
		
		trajX = self.pos[ 'x' ]
		trajY = self.pos[ 'y' ]
		
		while touche == False:
			trajX += trajectoire[0]*30
			trajY += trajectoire[1]*30
			hitbox = hitbox.move( round(trajX-hitbox.x), round(trajY-hitbox.y) )
			
			if ( ( hitbox.x - self.pos[ 'x' ] )**2 + ( hitbox.y - self.pos[ 'y' ] )**2 )**0.5 > portee :
				touche = True
			hit = []
			for x in range( 0, len( liste_zombies ) ):
				if hitbox.colliderect( liste_zombies[x].get_hitbox() ):
					hit.append([x, 'zombies'])
					touche = True
			for x in range( 0, len( liste_walls ) ):
				if hitbox.colliderect( liste_walls[x].get_hitbox() ) and liste_walls[x].get_solide():
					hit.append([x, 'terrain'])
					touche = True
		data = [ weapon, { 'x' : round( self.get_pos()[ 'x' ] + size_ent[ 'x' ]/2 ) , 'y' : round( self.get_pos()[ 'y' ] + size_ent[ 'y' ]/2 ) }, { 'x' : hitbox.x, 'y' : hitbox.y }, hit ]
		self.v_side -= trajectoire[0]*0.5 #recul
		self.v_up -= trajectoire[1]*0.5
		return data



class zombies(objet):
	def __init__ ( self, type, pos, image, vitesse, hitbox, health, num, trigger_range, v_up = 0, v_side = 0 ):
		objet.__init__(self, type, pos, image, hitbox, health, num)
		self.vitesse = vitesse
		self.v_up = v_up
		self.v_side = v_side
		self.trigger_range = trigger_range
	
	def set_vitesse( self, vitesse ):
		"""definis la vitesse de l'objet"""
		self.vitesse = vitesse
		
	def get_vitesse ( self ):
		"""renvoi la vitesse de l'objet"""
		return self.vitesse
		
	
	def set_trigger_range( self, trigger_range ):
		"""definis la distance de reperage de l'objet"""
		self.trigger_range = trigger_range
		
	def get_trigger_range( self ):
		"""renvoi la distance de reperage de l'objet"""
		return self.trigger_range
	
	def mouv ( self, list_player, list_collidable ):
		"""deplacement du zombie"""
		if len(list_player) != 0:
			player_pos = list_player[0].get_pos()
		else:
			player_pos = self.pos
		for x in range( 0, len(list_player) ):
			a = list_player[x].get_pos()[ 'y' ]
			if abs( ( list_player[x].get_pos()[ 'x' ] - self.pos[ 'x' ] )**2 + ( list_player[x].get_pos()[ 'y' ] - self.pos[ 'y' ] )**2 ) < abs( ( player_pos[ 'x' ] - self.pos[ 'x' ] )**2 + ( player_pos[ 'y' ] - self.pos[ 'y' ] )**2 ): #test pour determiner le joueur le plus proche
				player_pos = list_player[x].get_pos()
		
		if abs( ( player_pos[ 'x' ] - self.pos[ 'x' ] )**2 + ( player_pos[ 'y' ] - self.pos[ 'y' ] )**2 ) < self.trigger_range**2:
				
			if player_pos[ 'x' ] < self.pos[ 'x' ]: #si le joueur est sur la gauche
				if self.v_side > -1 * self.vitesse/100 * self.health:
					self.v_side -= self.vitesse/20
				else:
					self.v_side = -1 * self.vitesse/100 * self.health
			else:
				if self.v_side < 0:  #sinon ralentis progressivement
					self.v_side += self.vitesse/40
			
			if player_pos[ 'x' ] > self.pos[ 'x' ]:#si le joueur est sur la droite
				if self.v_side < self.vitesse/100 * self.health:
					self.v_side += self.vitesse/20
				else:
					self.v_side = self.vitesse/100 * self.health
			else:
				if self.v_side > 0:#sinon ralentis progressivement
					self.v_side -= self.vitesse/40
			
			if player_pos[ 'y' ] < self.pos[ 'y' ]:#si le joueur est au dessus
				if self.v_up >  -1 * self.vitesse/100 * self.health:
					self.v_up -= self.vitesse/20
				else:
					self.v_up = -1 * self.vitesse/100 * self.health
			else:
				if self.v_up < 0:#sinon ralentis progressivement
					self.v_up += self.vitesse/40
			
			if player_pos[ 'y' ] > self.pos[ 'y' ]:#si le joueur est au dessous
				if self.v_up < self.vitesse/100 * self.health:
					self.v_up += self.vitesse/20
				else:
					self.v_up = self.vitesse/100 * self.health
			else:
				if self.v_up > 0:#sinon ralentis progressivement
					self.v_up -= self.vitesse/40
			
			collision_x = False
			collision_y = False
			#Test de colision de la position future X pour determiner si le deplacement est autorise
			futur_pos_x = self.hitbox.move( round(self.v_side), 0 )
			for a in range( 0, len( list_collidable ) ):
				if futur_pos_x.colliderect( list_collidable[a].get_hitbox() ):#Test des collisions avec les zombies
					collision_x = True
					self.v_side = 0
					if list_collidable[a].get_image() == 'player':
						list_collidable[a].damage( 150 )
					
			if collision_x == False:#Deplacement si il n'y a pas collision
				self.set_pos( { 'x' : self.pos[ 'x' ] + round(self.v_side), 'y' : self.pos[ 'y' ] } )
				self.hitbox = self.hitbox.move( round(self.v_side), 0 )
			
			#Test de colision de la position future Y pour determiner si le deplacement est autorise
			futur_pos_y = self.hitbox.move( 0, round(self.v_up) )
			for a in range( 0, len( list_collidable ) ):
				if futur_pos_y.colliderect( list_collidable[a].get_hitbox() ):#Test des collisions avec les zombies
					collision_y = True
					self.v_up = 0
					if list_collidable[a].get_image() == 'player':
						list_collidable[a].damage( 50 )
			
			if collision_y == False:#Deplacement si il n'y a pas collision
				self.set_pos( { 'x' : self.pos[ 'x' ], 'y' : self.pos[ 'y' ] + round(self.v_up) } )
				self.hitbox = self.hitbox.move( 0, round(self.v_up) )
	def orientation( self ):
		"""orientation du zombie en fonction de sa vitesse x et y"""
		
		if round(self.v_side) == 0:
			if self.v_up > 0.5:
				self.set_angle( 90 )
			elif self.v_up < -0.5 :
				self.set_angle( 270 )
		
		else:
			self.set_angle( -1 * atan( round(self.v_up)/round(self.v_side) ) * 50 )

			if self.v_side > 0:
				self.set_angle( self.get_angle() - 180 )

class terrain( objet ):
	def __init__( self, type, pos, taille, image, hitbox, health, num, solide ):
		objet.__init__(self, type, pos, image, hitbox, health, num)
		self.solide = solide
		self.taille = taille
	def set_solide( self, solide ):
		"""definis si l'objet est solide ou non"""
		self.solide = solide
	def get_solide( self ):
		"""renvoi True si l'objet est solide et False si il ne l'est pas"""
		return self.solide
	def set_taille ( self, taille ):
		"""definis la taille de l'objet"""
		self.taille = { 'x' : taille[ 'x' ], 'y' : taille[ 'y' ] }

	def get_taille ( self ):
		"""renvoi la taille de l'objet"""
		return self.taille
	def get_visible( self, pos_player, liste_opaque ):
		print(liste_opaque)
		hitbox = pygame.Rect( self.pos[ 'x' ] + self.taille[ 'x' ]/2 , self.pos[ 'y' ] + self.taille[ 'y' ]/2 , 1, 1 )
		
		visible = False
		touche = False
		
		trajectoire = [0, 1]
		
		distance = ( ( pos_player[ 'x' ] - self.pos[ 'x' ] )**2 + ( pos_player[ 'y' ] - self.pos[ 'y' ] )**2 )**0.5
		if distance < 1000:
			trajectoire[0] = ( pos_player[ 'x' ] + self.get_taille()[ 'x' ]/2 ) / distance
			trajectoire[1] = ( pos_player[ 'y' ] + self.get_taille()[ 'y' ]/2 ) / distance
			
			trajX = self.pos[ 'x' ]
			trajY = self.pos[ 'y' ]
			
			while not touche:
				trajX += trajectoire[0]*20
				trajY += trajectoire[1]*20
				hitbox = hitbox.move( round(trajX-hitbox.x), round(trajY-hitbox.y) )
				
				if ( ( hitbox.x - self.pos[ 'x' ] )**2 + ( hitbox.y - self.pos[ 'y' ] )**2 )**0.5 > distance :
					touche = True
					print(1)
				hit = []
				for x in range( 0, len( liste_opaque ) ):
					if hitbox.colliderect( liste_opaque[x].get_hitbox() ):
						visible = True
						touche = True
						print(2)
		return visible

class spawner( objet ):
	def __init__( self, type, pos, taille, image, hitbox, health, num, solide ):
		objet.__init__(self, type, pos, image, hitbox, health, num)
		self.taille = taille
	def set_taille ( self, taille ):
		"""definis la taille de l'objet"""
		self.taille = { 'x' : taille[ 'x' ], 'y' : taille[ 'y' ] }

	def get_taille ( self ):
		"""renvoi la taille de l'objet"""
		return self.taille
	def spawn_( self, list_zombies, list_player ):
		usable = True
		for x in range(0, len(list_zombies) ):
			if self.hitbox.colliderect( list_zombies[x].get_hitbox() ):
				usable = False
		for x in range(0, len(list_player) ):
			if sqrt(( list_player[x].get_pos()[ 'x' ] - self.pos[ 'x' ] )**2 + ( list_player[x].get_pos()[ 'y' ] - self.pos[ 'y' ] )**2 ) > 1500:
				usable = False
		return usable
