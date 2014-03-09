# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 13:02:39 2014

@author: jwei
"""

import pygame
from pygame.locals import *
import random
import math
import time

SQUARELENGTH = 50

class Fire(pygame.sprite.Sprite):
    #set up a group for the fires after shooter and target sprites set up:
    fires = pygame.sprite.RenderUpdates()
    self.fires = pygame.sprite.Group()
    fire_range = SQUARELENGTH
    vN = -1
    vS = 1
    vW = -1
    vE = 1
    dN = 0
    dS = 0
    dW = 0
    dE = 0
    
    #may need to add a direction if the fire is treated as 4 different missiles
    def __init__ (self,imagefile,start_pointx,start_pointy,direction):
        """direction: str ('N', 'S', 'E', 'W') """

        pygame.sprite.Sprite.__init__(self)
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        self.direction = direction
        
        self.image = pygame.image.load(imagefile)
        self.rect = pygame.image.get_rect()
        #self.rect.x = start_point.x
        #self.rect.y = start_point.y
        self.rect.center = start_point
        self.speed = [0,1] #change trajectory by changing the speed
        
    def update(self,action):
        # Did the movement cause a collision with a block?
        block_hit_list = pygame.sprite.spritecollide(self,self.blocks,True)
        if self.direction == "N":
            if dN < fire_range:
                    self.rect.y += vN*SQUARELENGTH
                    dN+=SQUARELENGTH
            if self.direction == "S":
                if dS < fire_range:
                    self.rect.y += vN*SQUARELENGTH
                    dS+=SQUARELENGTH
            if self.direction == "W":
                if dW < fire_range:
                    self.rect.x += vW*SQUARELENGTH
                    dW+=SQUARELENGTH
            if self.direction == "E":
                if dE < fire_range:
                    self.rect.x += vE*SQUARELENGTH
                    dE+=SQUARELENGTH
                    
            if self.rect.left < 0 or self.rect.right > self.area.width or self.rect.top < 0 or self.rect.bottom > self.area.height:
                self.kill()
                
        for block in block_hit_list:
            if self.direction == "N":
                if self.rect.x  == block.rect.x and self.rect.y == block.rect.y + SQUARELENGTH:
                    if isinstance(block, BlockDestroyable):
                        block.kill()
                    else:
                        self.kill()
                    
            if self.direction == "S":
                if self.rect.x  == block.rect.x and self.rect.y == block.rect.y - SQUARELENGTH:
                    if isinstance(block, BlockDestroyable):
                        block.kill()
                    else:
                        self.kill()
                        
            if self.direction == "W":
                if self.rect.x  == block.rect.x + SQUARELENGTH and self.rect.y == block.rect.y:
                    if isinstance(block, BlockDestroyable):
                        block.kill()
                    else:
                        self.kill()
                        
            if self.direction == "E":
                if self.rect.x  == block.rect.x - SQUARELENGTH and self.rect.y == block.rect.y:
                    if isinstance(block, BlockDestroyable):
                        block.kill()
                    else:
                        self.kill()