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
<<<<<<< HEAD
        self.Fire = Fire(60,5,55,55,1)
        
    def createbomb(self):
        #make a list of bombs
        pass
    
=======
        

>>>>>>> a1b1bd9d5aaf4756946282199ec20507eaee6b2a
    def update(self):
        self.player.update()
        self.bomb.update()
        self.fire.update()

        
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
<<<<<<< HEAD
        
    def update(self):
        self.x += self.x
        self.y += self.y
        if player.x>=bomb.x-bomb.width and player.x<=bomb.x+bomb.width:
            player.lives-=1
            
        if player.y>=bomb.y-bomb.length and player.y<=bomb.y+bomb.length:
            player.lives-=1
=======
>>>>>>> a1b1bd9d5aaf4756946282199ec20507eaee6b2a
    
class Bomb:
    """ Encode the state of the bomb in the Playingwithfiremodel"""
    def __init__(self, x,y):
        self.x=x
        self.y=y
       
    # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
     
        # Upload Bomb Image, Resize, Set Background to Transparent
        self.image = pygame.image.load('bomb.jpg')
        self.image = pygame.transform.scale(self.image, (PLAYERSIZE, PLAYERSIZE))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    
    def update(self):
        
            
            
class feetpowerup:
    def __init__(self, x,y,):
        self.x=x
        self.y=y
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
     
        # Upload Bomb Image, Resize, Set Background to Transparent
        self.image = pygame.image.load('images/winged-foot.jpg')
        self.image = pygame.transform.scale(self.image, (PLAYERSIZE, PLAYERSIZE))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
            
        

    
class Fire:
    """Encodes the state of fire from bomb"""
    def __init__(self, x,y,width,length,units):
        self.x=x
        self.y=y
        self.width = width
        self.length = length
        self.units=units 
        
        
        
    
    def update(self):
        self.t+=1
        
        if t>3 and t<=8: #I don't know the notation for this.
            self.width+=units*width
            self.length+=units*length
        
        if t>8:
            #deactivates
            self.width = width
            self.length = length 
    

def __init__(self,x,y,bombs,lives):
        self.bombs=bombs
        self.lives=lives

        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
     
        # Upload Player Image, Resize, Set Background to Transparent
        self.image = pygame.image.load('images/player1.png')
        self.image = pygame.transform.scale(self.image, (PLAYERSIZE, PLAYERSIZE))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class PyGameKeyboardController:
    """ Manipulate game state based on keyboard input """
    def __init__(self, model):
        self.model = model
    
    def handle_pygame_event(self, event):
        
        if event.key == pygame.K_LEFT:
            self.model.player.x -= 55.0
        if event.key == pygame.K_RIGHT:
            self.model.player.x += 55.0
        if event.type == KEYDOWN:
            self.model.player.y += 55.0
        if event.type == KEYUP:
            self.model.player.y -= 55.0
        if event.key == pygame.K_KP_DIVIDE:
            self.model.player.bombs -= 1.0
            self.model.bomb=activate #I don't know the notation for this
            t=0                      # Makes t=0 and starts counting
            self.model.bomb.x=player.x
            self.model.bomb.y=player.y
            
            
            
if __name__ == '__main__':
    pygame.init()

<<<<<<< HEAD
    size = (640,480)
=======
    size = (1028,720)
>>>>>>> a1b1bd9d5aaf4756946282199ec20507eaee6b2a
    screen = pygame.display.set_mode(size)

    model = BrickBreakerModel()
    view = PyGameBrickBreakerView(model,screen)
    controller = PyGameKeyboardController(model)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_pygame_event(event)
        model.update()
        view.draw()
        time.sleep(.001)

    pygame.quit()
<<<<<<< HEAD

=======
     
            
            
>>>>>>> a1b1bd9d5aaf4756946282199ec20507eaee6b2a
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            