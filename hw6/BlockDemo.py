# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 20:44:17 2014

@author: jwei
"""

import pygame
from pygame.locals import *
import random
import math
import time

# --- Set Constants
WIDTH = 1140
HEIGHT = 780
SQUARELENGTH = 60
WHITE = (255, 255, 255)


class PWFModel:
    """This class encodes the game state"""
     
    def __init__ (self):
        self.blocks = pygame.sprite.Group()
        self.everything = pygame.sprite.Group()
        
        self._populateBlocks()
        self._populatePlayers()

    def update(self):
        pass

    def _populateBlocks(self):
        # Populate Permanent Perimeter
        for x in range(0, WIDTH, SQUARELENGTH):
            # side walls
            if x == 0 or x == WIDTH - SQUARELENGTH:
                for y in range(0, HEIGHT, SQUARELENGTH):
                    block = BlockPermanent(x, y)
                    self.blocks.add(block)
                    self.everything.add(block)
            # top/bottom walls
            else:
                for y in [0, HEIGHT - SQUARELENGTH]:
                    block = BlockPermanent(x, y)
                    self.blocks.add(block)
                    self.everything.add(block)
        # Populate Permanent Mid Grid
        for x in range(2*SQUARELENGTH,WIDTH - 2*SQUARELENGTH,SQUARELENGTH):
            if x % (2*SQUARELENGTH) == SQUARELENGTH:
                continue
            for y in range(0,HEIGHT,60):
                if y % (2*SQUARELENGTH) == SQUARELENGTH:
                    continue
                block = BlockPermanent(x,y)
                self.blocks.add(block)
                self.everything.add(block)
    
    def _populatePlayers(self):
        # player number determined by starting quadrant
        self.player1 = Player(WIDTH-2*SQUARELENGTH,SQUARELENGTH,bombs=1,lives=3)
        self.player2 = Player(SQUARELENGTH,SQUARELENGTH,bombs=1,lives=3)
        self.player3 = Player(SQUARELENGTH,HEIGHT-2*SQUARELENGTH,bombs=1,lives=3)
        self.player4 = Player(WIDTH-2*SQUARELENGTH,HEIGHT-2*SQUARELENGTH,bombs=1,lives=3)
        for player in [self.player1,self.player2,self.player3,self.player4]:
            self.everything.add(player)

# --- Classes
class BlockPermanent(pygame.sprite.Sprite):
    """This class encodes the state of the block"""
    def __init__ (self,x,y):
        #Call the parent class (Sprite) constructor     
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/brickwall.jpg')
        self.image = pygame.transform.scale(self.image, (SQUARELENGTH, SQUARELENGTH))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class BlockDestroyable(pygame.sprite.Sprite):
    """This class encodes the state of the block"""
    def __init__ (self,x,y):
        #Call the parent class (Sprite) constructor     
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/brickwall.jpg')
        self.image = pygame.transform.scale(self.image, (SQUARELENGTH, SQUARELENGTH))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(pygame.sprite.Sprite):
        
    def __init__(self,x,y,bombs,lives):
        self.x = x
        self.y = y
        self.bombs=bombs
        self.lives=lives

        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
     
        # Upload Player Image, Resize, Set Background to Transparent
        self.image = pygame.image.load('images/player1.png')
        self.image = pygame.transform.scale(self.image, (SQUARELENGTH, SQUARELENGTH))
        self.image.set_colorkey((255,255,255))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
class PyGameWindowView:
    """View of Brickbreaker rendered in a PyGame Window"""
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
    
    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
        self.model.everything.draw(self.screen)   
        pygame.display.update()

class PWFController:
    def __init__(self,model):
        self.model = model

    def handle_keyboard_event(self,event):
        """ Handles the keyboard input for Playing with Fire 
        """        
        if event.type !=KEYDOWN:
            pass
        if event.key == pygame.K_LEFT:
            self.model.paddle.vx += -1.0
        if event.key == pygame.K_RIGHT:
            self.model.paddle.vx += 1.0       
if __name__ == '__main__':
    pygame.init()
    size = (WIDTH,HEIGHT)
    screen = pygame.display.set_mode(size)
    # initialize font; must be called after 'pygame.init()' 
    font = pygame.font.Font(None, 36)
    pygame.display.set_caption("PLAYING WITH FIRE")
    

    model = PWFModel()    
    view = PyGameWindowView(model,screen)   
    controller = PWFController(model)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                controller.handle_keyboard_event(event)
        model.update()
        view.draw()
        time.sleep(.001)
    text = font.render("Game Over", True,(255,255,255))
    pygame.quit()