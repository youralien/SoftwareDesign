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
        
        self.Player = Player(5,5,50,50,1,3)
        self.Bomb = Bomb(5,5,50,50,100)
    
    def update(self):
        self.player.update()
        self.bomb.update()
        
class Player:
    """ Encode the state of the player in the Playingwithfiremodel"""
    def __init__(self,x,y,width,length,bombs,lives):
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.bombs=bombs
        self.lives=lives
        
    
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
            self.model.player.x += -50.0
        if event.key == pygame.K_RIGHT:
            self.model.player.x += 50.0
        if event.type == KEYDOWN:
            self.model.player.y += 50.0
        if event.type == KEYUP:
            self.model.player.y += -50.0
        if event.key == pygame.K_KP_DIVIDE:
            self.model.player.bombs += -1.0
            self.model.bomb=activate #I don't know the notation for this
            self.model.bomb.x=player.x
            self.model.bomb.y=player.y
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            