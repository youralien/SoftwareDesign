# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 20:44:17 2014

@author: jwei

Wall Collision Code Adapted from:
http://programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py


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
PLAYERSIZE = 50
WHITE = (255, 255, 255)
GRAY = (117, 117, 117)
MOVE = 6
DETONATION_TICK = 100

# Set Event IDs
K_BOMB_TIMER = 25



class PWFModel:
    """This class encodes the game state"""
    
    player1 = None
    player2 = None
    player3 = None
    player4 = None

    def __init__ (self):
        self.bombs = pygame.sprite.Group()
        self.fires = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.everything = pygame.sprite.Group()
        
    
        self._populateBlocks()
        self._populatePlayers()

    def update(self):
        self.players.update()
        self.bombs.update()

    def _populateBlocks(self):
        # Populate Permanent Perimeter
        for x in range(0, WIDTH, SQUARELENGTH):
            # Side walls
            if x == 0 or x == WIDTH - SQUARELENGTH:
                for y in range(0, HEIGHT, SQUARELENGTH):
                    block = BlockPermanent(x, y)
                    self.blocks.add(block)
                    self.everything.add(block)
            # Top/bottom walls
            else:
                for y in [0, HEIGHT - SQUARELENGTH]:
                    block = BlockPermanent(x, y)
                    self.blocks.add(block)
                    self.everything.add(block)
        
        # Populate Permanent Mid Grid
        for x in range(2*SQUARELENGTH,WIDTH - 2*SQUARELENGTH,SQUARELENGTH):
            if x % (2*SQUARELENGTH) == SQUARELENGTH:
                continue
            for y in range(0,HEIGHT,SQUARELENGTH):
                if y % (2*SQUARELENGTH) == SQUARELENGTH:
                    continue
                block = BlockPermanent(x,y)
                self.blocks.add(block)
                self.everything.add(block)
                
        # Populate BlockDestroyable
        for x in range(2*SQUARELENGTH,WIDTH - 2*SQUARELENGTH,SQUARELENGTH):
            for y in range(2*SQUARELENGTH,HEIGHT-2*SQUARELENGTH,SQUARELENGTH):
                if x % (2*SQUARELENGTH) != SQUARELENGTH and y % (2*SQUARELENGTH) != SQUARELENGTH:
                    continue
            
                a=random.choice([True, False])
                if a==True:
                    block = BlockDestroyable(x,y)
                    self.blocks.add(block)
                    self.everything.add(block)
        
        # powerup
        powerup = FeetPowerUp(2*SQUARELENGTH, SQUARELENGTH)
        self.everything.add(powerup)

    def _populatePlayers(self):
        # player number determined by starting quadrant
        self.player1 = Player(WIDTH-2*SQUARELENGTH,SQUARELENGTH,bombs=1,lives=3,playeri=1)
        self.player2 = Player(SQUARELENGTH,SQUARELENGTH,bombs=1,lives=3,playeri=2)
        self.player3 = Player(SQUARELENGTH,HEIGHT-2*SQUARELENGTH,bombs=1,lives=3,playeri=3)
        self.player4 = Player(WIDTH-2*SQUARELENGTH,HEIGHT-2*SQUARELENGTH,bombs=1,lives=3,playeri=4)
        for player in [self.player1,self.player2,self.player3,self.player4]:
            self.players.add(player)
            self.everything.add(player)
            player.blocks = self.blocks

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
        self.image = pygame.image.load('images/woodenbox.jpg')
        self.image = pygame.transform.scale(self.image, (SQUARELENGTH, SQUARELENGTH))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(pygame.sprite.Sprite):
    
    # Set speed vector
    change_x = 0
    change_y = 0
    blocks = None

    def __init__(self,x,y,bombs,lives,playeri):
        """
        bombs: integer
        lives: integer
        playeri: 1,2,3, or 4
        """
        self.bombs=bombs
        self.lives=lives

        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
     
        # Upload Player Image, 
        self.image = pygame.image.load('images/p{}.png'.format(playeri))
        
        # Resize, Set Background to Transparent
        self.image = pygame.transform.scale(self.image, (PLAYERSIZE, PLAYERSIZE))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def changespeed(self, x, y):
        """ Change speed of the player """
        self.change_x += x 
        self.change_y += y

    def update(self):
        """ Update Player Position """

        # Move horizontally
        self.rect.x += self.change_x

        # Did the movement cause a collision with a block?
        block_hit_list = pygame.sprite.spritecollide(self,self.blocks,False)
        for block in block_hit_list:

            # Moving right
            if self.change_x > 0:
                self.rect.right = block.rect.left
            # Moving left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        # Move Vertically
        self.rect.y += self.change_y
        
        # Did the movement cause a collision with a block?
        block_hit_list = pygame.sprite.spritecollide(self,self.blocks,False)
        for block in block_hit_list:
            # Moving up
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            # Moving down
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

class Bomb(pygame.sprite.Sprite):
    """ Encode the state of the bomb in the Playingwithfiremodel"""
    def __init__(self, x,y, playeri):
        self.x=x
        self.y=y
        self.time_to_detonate = 13 * 1000 # milliseconds
        self.playeri = playeri
        
       
    # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
     
        # Upload Bomb Image, Resize, Set Background to Transparent
        self.image = pygame.image.load('images/bomb.png')
        self.image = pygame.transform.scale(self.image, (PLAYERSIZE, PLAYERSIZE))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.time_to_detonate -= DETONATION_TICK
        if self.time_to_detonate <= 0:

            self.kill() # Remove Bomb from the Game

        
class FeetPowerUp(pygame.sprite.Sprite):
    """makes you faster"""
    def __init__(self, x,y,):
        self.x=x
        self.y=y
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
     
        # Upload Bomb Image, Resize, Set Background to Transparent
        self.image = pygame.image.load('images/wingedfootpowerup.jpg')
        self.image = pygame.transform.scale(self.image, (PLAYERSIZE, PLAYERSIZE))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        
class BombPowerUp(pygame.sprite.Sprite):
    """lets you plant more bombs"""
    def __init__(self, x,y,):
        self.x=x
        self.y=y
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
     
        # Upload Bomb Image, Resize, Set Background to Transparent
        self.image = pygame.image.load('images/bombpowerup.jpg')
        self.image = pygame.transform.scale(self.image, (PLAYERSIZE, PLAYERSIZE))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class LightningPowerUp(pygame.sprite.Sprite):
    """increases your bomb range"""
    def __init__(self, x,y,):
        self.x=x
        self.y=y
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
     
        # Upload Bomb Image, Resize, Set Background to Transparent
        self.image = pygame.image.load('images/lightningpowerup.jpg')
        self.image = pygame.transform.scale(self.image, (PLAYERSIZE, PLAYERSIZE))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class PWFView:
    """View of Brickbreaker rendered in a PyGame Window"""
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
    
    def draw(self):
        self.screen.fill(pygame.Color(64,64,64))
        self.model.everything.draw(self.screen)   
        pygame.display.update()

# class PWFController:
#     def __init__(self,model):
#         self.model = model

#     def handle_keyboard_event(self,event):
#         """ Handles the keyboard input for Playing with Fire 
#         """

#         if event.type == pygame.KEYDOWN:
#             # Bomb Detonation
#             if event.key == K_BOMB_TIMER:
#                 for bomb in
#                 self.model.fires.update()
            
#             # Player 1 Actions
#             if event.key == pygame.K_LEFT:
#                 self.model.player1.changespeed(-MOVE,0)
#             elif event.key == pygame.K_RIGHT:
#                 self.model.player1.changespeed(MOVE,0)
#             elif event.key == pygame.K_UP:
#                 self.model.player1.changespeed(0,-MOVE)
#             elif event.key == pygame.K_DOWN:
#                 self.modxel.player1.changespeed(0,MOVE)
#             elif event.key == pygame.K_SLASH:
#                 if self.model.player1.bombs>0:
#                     self.model.player1.bombs -= 1.0
                
#                     bomb = Bomb(self.model.player1.rect.x, self.model.player1.rect.y,playeri=1)
#                     self.model.bombs.add(bomb)
#                     self.model.everything.add(bomb)
            
                
#             # Player 2 Actions
#             if event.key == pygame.K_a:
#                 self.model.player2.changespeed(-MOVE,0)
#             elif event.key == pygame.K_d:
#                 self.model.player2.changespeed(MOVE,0)
#             elif event.key == pygame.K_w:
#                 self.model.player2.changespeed(0,-MOVE)
#             elif event.key == pygame.K_s:
#                 self.model.player2.changespeed(0,MOVE)
#             elif event.key == pygame.K_e:
#                 if self.model.player2.bombs>0:
#                     self.model.player2.bombs -= 1.0
                    
#                     bomb = Bomb(self.model.player2.rect.x, self.model.player2.rect.y)
#                     self.model.bombs.add(bomb)
#                     self.model.everything.add(bomb)


#         elif event.type == pygame.KEYUP:
#             # Player 1 Reverse Actions
#             if event.key == pygame.K_LEFT:
#                 self.model.player1.changespeed(MOVE,0)
#             elif event.key == pygame.K_RIGHT:
#                 self.model.player1.changespeed(-MOVE,0)
#             elif event.key == pygame.K_UP:
#                 self.model.player1.changespeed(0,MOVE)
#             elif event.key == pygame.K_DOWN:
#                 self.model.player1.changespeed(0,-MOVE)

#             # Player 2 Reverse Actions
#             if event.key == pygame.K_a:
#                 self.model.player2.changespeed(MOVE,0)
#             elif event.key == pygame.K_d:
#                 self.model.player2.changespeed(-MOVE,0)
#             elif event.key == pygame.K_w:
#                 self.model.player2.changespeed(0,MOVE)
#             elif event.key == pygame.K_s:
#                 self.model.player2.changespeed(0,-MOVE)

        
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))

    # initialize font; must be called after 'pygame.init()' 
    font = pygame.font.Font(None, 36)
    pygame.display.set_caption("PLAYING WITH FIRE")

    # event is called every 100 milliseconds
    pygame.time.set_timer(K_BOMB_TIMER,DETONATION_TICK)

    model = PWFModel()    
    view = PWFView(model,screen)   
    # controller = PWFController(model)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            else:

                # --- Controller Logic

                if event.type == pygame.KEYDOWN:
                    # Bomb Detonation
                    if event.key == K_BOMB_TIMER:
                        for bomb in model.bombs:
                            # Count Down time_to_detonate
                            bomb.time_to_detonate -= DETONATION_TICK
                            # Time to Detonate is Now!
                            if bomb.time_to_detonate <= 0:
                                bomb.kill()
                    
                    # Player 1 Actions
                    if event.key == pygame.K_LEFT:
                        model.player1.changespeed(-MOVE,0)
                    elif event.key == pygame.K_RIGHT:
                        model.player1.changespeed(MOVE,0)
                    elif event.key == pygame.K_UP:
                        model.player1.changespeed(0,-MOVE)
                    elif event.key == pygame.K_DOWN:
                        model.player1.changespeed(0,MOVE)
                    elif event.key == pygame.K_SLASH:
                        if model.player1.bombs>0:
                            model.player1.bombs -= 1.0
                        
                            bomb = Bomb(model.player1.rect.x, model.player1.rect.y,playeri=1)
                            model.bombs.add(bomb)
                            model.everything.add(bomb)
                    
                        
                    # Player 2 Actions
                    if event.key == pygame.K_a:
                        model.player2.changespeed(-MOVE,0)
                    elif event.key == pygame.K_d:
                        model.player2.changespeed(MOVE,0)
                    elif event.key == pygame.K_w:
                        model.player2.changespeed(0,-MOVE)
                    elif event.key == pygame.K_s:
                        model.player2.changespeed(0,MOVE)
                    elif event.key == pygame.K_e:
                        if model.player2.bombs>0:
                            model.player2.bombs -= 1.0
                            
                            bomb = Bomb(model.player2.rect.x, model.player2.rect.y,playeri=2)
                            model.bombs.add(bomb)
                            model.everything.add(bomb)


                elif event.type == pygame.KEYUP:
                    # Player 1 Reverse Actions
                    if event.key == pygame.K_LEFT:
                        model.player1.changespeed(MOVE,0)
                    elif event.key == pygame.K_RIGHT:
                        model.player1.changespeed(-MOVE,0)
                    elif event.key == pygame.K_UP:
                        model.player1.changespeed(0,MOVE)
                    elif event.key == pygame.K_DOWN:
                        model.player1.changespeed(0,-MOVE)

                    # Player 2 Reverse Actions
                    if event.key == pygame.K_a:
                        model.player2.changespeed(MOVE,0)
                    elif event.key == pygame.K_d:
                        model.player2.changespeed(-MOVE,0)
                    elif event.key == pygame.K_w:
                        model.player2.changespeed(0,MOVE)
                    elif event.key == pygame.K_s:
                        model.player2.changespeed(0,-MOVE)

        model.update()
        view.draw()
        time.sleep(.001)
        
    text = font.render("Game Over", True,(255,255,255))
    pygame.quit()

if __name__ == '__main__':
    main()

    