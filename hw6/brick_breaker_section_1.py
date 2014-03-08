# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 19:34:24 2014

@author: pruvolo
"""

import pygame
from pygame.locals import *
import random
import math
import time

class BrickBreakerModel:
    """ Encodes the game state of Brick Breaker """
    def __init__(self):
        self.number_of_lives = 3
        self.bricks = []
        for i in range(640/110):
            for j in range(240/30):              
                new_brick = Brick(10+110*i,10+30*j,100,20,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
                self.bricks.append(new_brick)
        self.paddle = Paddle(200,450,100,20)
    
    def update(self):
        self.paddle.update()
        
class Brick:
    """ Encodes the state of a brick in Brick Breaker """
    def __init__(self,x,y,width,height,color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    
class Paddle:
    """ Encode the state of the paddle in Brick Breaker """
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (255,255,255)
        self.vx = 0.0
    
    def update(self):
        self.x += self.vx

class PyGameBrickBreakerView:
    """ renders the BrickBreakerModel to a pygame window """
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
    
    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
        for brick in self.model.bricks:
            pygame.draw.rect(self.screen, pygame.Color(brick.color[0], brick.color[1], brick.color[2]), pygame.Rect(brick.x, brick.y, brick.width, brick.height))
        pygame.draw.rect(self.screen, pygame.Color(self.model.paddle.color[0], self.model.paddle.color[1], self.model.paddle.color[2]), pygame.Rect(self.model.paddle.x, self.model.paddle.y, self.model.paddle.width, self.model.paddle.height))
        pygame.display.update()

class PyGameKeyboardController:
    """ Manipulate game state based on keyboard input """
    def __init__(self, model):
        self.model = model
    
    def handle_pygame_event(self, event):
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_LEFT:
            self.model.paddle.vx += -1.0
        if event.key == pygame.K_RIGHT:
            self.model.paddle.vx += 1.0

if __name__ == '__main__':
    pygame.init()

    size = (640,480)
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
