# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 14:54:59 2014

@author: julian
"""


import pygame
from pygame.locals import *
import random
import math
import time

class Playingwithfiremodel:
    """ Encodes the game state of Brick Breaker """
    def __init__(self):
        
        self.Player = Player(5,5,55,55,1,3)
        self.Bomb = Bomb(5,5,55,55,100)
    
    def update(self):
        self.player.update()
        self.bomb.update()

        
class PlayerSprite(pygame.sprite.Sprite):
        
    def __init__(self,x,y,width,length,bombs,lives):
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.bombs=bombs
        self.lives=lives
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
     
        # Upload Player Image, Resize, Set Background to Transparent
        self.image = pygame.image.load('images/player1.png')
        self.image = pygame.transform.scale(self.image, (SQUARELENGTH, SQUARELENGTH))
        self.image.set_colorkey((255,255,255))

        self.rect = self.image.get_rect()
        
    def update(self):
        self.x += self.x
        self.y += self.y
    
class Bomb:
    """ Encode the state of the bomb in the Playingwithfiremodel"""
    def __init__(self, x,y,width,length,expradius):
        self.x=x
        self.y=y
        self.width = width
        self.length = length
        self.expradius=expradius
    
    def update(self):
        when t=0 to t=3: #I don't know the notation for this.
            self.width = width
            self.length = length
        when t>=3: #I don't know the notation for this.
            self.width+=expradius
            self.length+=expradius
        
        
    
class PyGameKeyboardController:
    """ Manipulate game state based on keyboard input """
    def __init__(self, model):
        self.model = model
    
    def handle_pygame_event(self, event):
        
        if event.key == pygame.K_LEFT:
            self.model.player.x += -55.0
        if event.key == pygame.K_RIGHT:
            self.model.player.x += 55.0
        if event.type == KEYDOWN:
            self.model.player.y += 55.0
        if event.type == KEYUP:
            self.model.player.y += -55.0
        if event.key == pygame.K_KP_DIVIDE:
            self.model.player.bombs += -1.0
            self.model.bomb=activate #I don't know the notation for this
            self.model.bomb.x=player.x
            self.model.bomb.y=player.y
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            