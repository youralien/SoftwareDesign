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

SQUARELENGTH = 50  

class PWFModel:
    """This class encodes the game state"""
     
    
    def __init__ (self):
        #self.bricks = []
        self.blocks = pygame.sprite.Group()
        self.everything = pygame.sprite.Group()
#        for x in range(10,530,110):
#            for y in range(10,240,30):
#                brick = Brick((random.randint(0,255),random.randint(0,255),random.randint(0,255)),20,100,x,y)
#                self.bricks.append(brick)
                
        for x in range(60,1000,60):
            for y in range(60,600,60):
                block = Block((195,25,25),SQUARELENGTH,SQUARELENGTH,x,y)
                self.blocks.add(block)
                self.everything.add(block)
        self.paddle = Paddle((255,255,255),20,100,200,450)
        
    def update(self):
        self.paddle.update()
        
### NEW CODE
class Block(pygame.sprite.Sprite):
    """This class encodes the state of the block"""
    def __init__ (self,color,width,height,x,y):
        #Call the parent class (Sprite) constructor     
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface([width,height])
        self.image = pygame.image.load('images/brickwall.jpg')
        #self.image.fill(color)
        self.image = pygame.transform.scale(self.image, (SQUARELENGTH, SQUARELENGTH))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
###

        # Upload Player Image, Resize, Set Background to Transparent
class Brick:
    """This class encodes the state of a brick in a game"""
    def __init__(self,color,height,width,x,y):
        self.color = color
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        
class Paddle:
    """This class encodes the state of the paddle"""
    def __init__(self,color,height,width,x,y):
        self.color = color
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
    
    def update(self):
        self.x += self.vx
        
class PyGameWindowView:
    """View of Brickbreaker rendered in a PyGame Window"""
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
    
    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
        #print len(self.model.bricks)
#        for brick in self.model.bricks:
#            pygame.draw.rect(self.screen,pygame.Color(brick.color[0],brick.color[1],brick.color[2]),pygame.Rect(brick.x,brick.y,brick.width,brick.height))
        #pygame.draw.rect(self.screen,pygame.Color(self.model.paddle.color[0],self.model.paddle.color[1],self.model.paddle.color[2]),pygame.Rect(self.model.paddle.x,self.model.paddle.y,self.model.paddle.width,self.model.paddle.height))
        self.model.everything.draw(self.screen)   
        pygame.display.update()

class PyGameKeyboardController:
    def __init__(self,model):
        self.model = model

    def handle_keyboard_event(self,event):
        """ Handles the keyboard input for brick breaker """        
        if event.type !=KEYDOWN:
            return
        if event.key == pygame.K_LEFT:
            self.model.paddle.vx += -1.0
        if event.key == pygame.K_RIGHT:
            self.model.paddle.vx += 1.0
                
if __name__ == '__main__':
    pygame.init()
    size = (1080,720)
    screen = pygame.display.set_mode(size)
    # initialize font; must be called after 'pygame.init()' 
    font = pygame.font.Font(None, 36)
    pygame.display.set_caption("PLAYING WITH FIRE")
    

    model = PWFModel()    
    view = PyGameWindowView(model,screen)   
    controller = PyGameKeyboardController(model)
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