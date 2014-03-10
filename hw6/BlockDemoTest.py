# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 20:44:17 2014

@author: jwei

Wall Collision Code Adapted from:
http://programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py


"""

import sys
import os
import pygame
 
pygame.init()
 
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
 
class MenuItem(pygame.font.Font):
    """Menu for the game"""
    def __init__(self, text, font=None, font_size=30,
                 font_color=WHITE, (pos_x, pos_y)=(0, 0)):
 
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.dimensions = (self.width, self.height)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = pos_x, pos_y
 
    def is_mouse_selection(self, (posx, posy)):
        if (posx >= self.pos_x and posx <= self.pos_x + self.width) and \
            (posy >= self.pos_y and posy <= self.pos_y + self.height):
                return True
        return False
 
    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y
 
    def set_font_color(self, rgb_tuple):
        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)
 
class GameMenu():
    def __init__(self, screen, items, funcs, bg_color=BLACK, font=None, font_size=30,
                 font_color=WHITE):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
 
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()
 
        self.funcs = funcs
        self.items = []
        for index, item in enumerate(items):
            menu_item = MenuItem(item, font, font_size, font_color)
 
            # t_h: total height of text block
            t_h = len(items) * menu_item.height
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            pos_y = (self.scr_height / 2) - (t_h / 2) + (index * menu_item.height)
 
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)
 
        self.mouse_is_visible = True
        self.cur_item = None
 
    def set_mouse_visibility(self):
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)
 
    def set_keyboard_selection(self, key):
        """
        Marks the MenuItem chosen via up and down keys.
        """
        for item in self.items:
            # Return all to neutral
            item.set_italic(False)
            item.set_font_color(WHITE)
 
        if self.cur_item is None:
            self.cur_item = 0
        else:
            # Find the chosen item
            if key == pygame.K_UP and \
                    self.cur_item > 0:
                self.cur_item -= 1
            elif key == pygame.K_UP and \
                    self.cur_item == 0:
                self.cur_item = len(self.items) - 1
            elif key == pygame.K_DOWN and \
                    self.cur_item < len(self.items) - 1:
                self.cur_item += 1
            elif key == pygame.K_DOWN and \
                    self.cur_item == len(self.items) - 1:
                self.cur_item = 0
 
        self.items[self.cur_item].set_italic(True)
        self.items[self.cur_item].set_font_color(RED)
 
        # Finally check if Enter or Space is pressed
        if key == pygame.K_SPACE or key == pygame.K_RETURN:
            text = self.items[self.cur_item].text
            self.funcs[text]()
 
    def set_mouse_selection(self, item, mpos):
        """Marks the MenuItem the mouse cursor hovers on."""
        if item.is_mouse_selection(mpos):
            item.set_font_color(RED)
            item.set_italic(True)
        else:
            item.set_font_color(WHITE)
            item.set_italic(False)
 
    def run(self):
        mainloop = True
        while mainloop:
            # Limit frame speed to 50 FPS
            self.clock.tick(50)
 
            mpos = pygame.mouse.get_pos()
 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                if event.type == pygame.KEYDOWN:
                    self.mouse_is_visible = False
                    self.set_keyboard_selection(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self.items:
                        if item.is_mouse_selection(mpos):
                            self.funcs[item.text]()
 
            if pygame.mouse.get_rel() != (0, 0):
                self.mouse_is_visible = True
                self.cur_item = None
 
            self.set_mouse_visibility()
 
            # Redraw the background
            self.screen.fill(self.bg_color)
 
            for item in self.items:
                if self.mouse_is_visible:
                    self.set_mouse_selection(item, mpos)
                self.screen.blit(item.label, item.position)
 
            pygame.display.flip()
 








import pygame
from pygame.locals import *
import random
import math
import time

# --- Set Constants
WIDTH = 1140
HEIGHT = 780
SQUARELENGTH = 60
PLAYERSIZE = 60
WHITE = (255, 255, 255)
GRAY = (117, 117, 117)
MOVE = SQUARELENGTH
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
        block_hit_list = pygame.sprite.spritecollide(self,self.blocks,True)
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
    def __init__(self, x,y,time_to_detonate, playeri):
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

            self.kill() 
            # Fireup=Fire(model.bomb.x,model.bomb.y-SQUARELENGTH)
            # Firedown=Fire(model.bomb.x,model.bomb.y+SQUARELENGTH)
            # Fireleft=Fire(model.bomb.x-SQUARELENGTH,model.bomb.y)
            # Fireright=Fire(model.bomb.x+SQUARELENGTH,model.bomb.y)
            # for fire in [Fireup, Firedown, Fireleft, Fireright]:
            #     self.model.fires.add(fire)
            #     self.model.everything.add(fire)
            # bomb.kill()

class Fire(pygame.sprite.Sprite):
    #set up a group for the fires after shooter and target sprites set up:
    fires = pygame.sprite.RenderUpdates()
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
    def __init__ (self,start_pointx,start_pointy,direction):
        """direction: str ('N', 'S', 'E', 'W') """

        pygame.sprite.Sprite.__init__(self)
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        self.direction = direction
        
        self.image = pygame.image.load('images/bomb.png')
        self.image = pygame.transform.scale(self.image,(60,60))
        self.rect = self.image.get_rect()
        self.rect.x = start_pointx
        self.rect.y = start_pointy
#        self.rect.x = start_pointx - (SQUARELENGTH/4) - 5
#        self.rect.y = start_pointy - (SQUARELENGTH/2) + 5
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

class PWFController:
        def __init__(self,model):
           self.model = model

        def handle_keyboard_event(self,event):
         """ Handles the keyboard input for Playing with Fire """
         
         if event.type == pygame.KEYDOWN:
             # Bomb Detonation
                
            if event.key == K_BOMB_TIMER:
                self.model.fires.update()
            

            # Player 1 Actions
            if event.key == pygame.K_LEFT:
                self.model.player1.changespeed(-MOVE,0)
            elif event.key == pygame.K_RIGHT:
                self.model.player1.changespeed(MOVE,0)
            elif event.key == pygame.K_UP:
                self.model.player1.changespeed(0,-MOVE)
            elif event.key == pygame.K_DOWN:
                self.model.player1.changespeed(0,MOVE)
            elif event.key == pygame.K_SLASH:
                if self.model.player1.bombs>0:
                    self.model.player1.bombs -= 1.0
                
                    bomb = Bomb(self.model.player1.rect.x, self.model.player1.rect.y,13000,1)
                    self.model.bombs.add(bomb)
                    self.model.everything.add(bomb)

            
                
             # Player 2 Actions
            if event.key == pygame.K_a:
                 self.model.player2.changespeed(-MOVE,0)
            elif event.key == pygame.K_d:
                 self.model.player2.changespeed(MOVE,0)
            elif event.key == pygame.K_w:
                 self.model.player2.changespeed(0,-MOVE)
            elif event.key == pygame.K_s:
                 self.model.player2.changespeed(0,MOVE)
            elif event.key == pygame.K_e:
                 if self.model.player2.bombs>0:
                     self.model.player2.bombs -= 1.0
                    

                     bomb = Bomb(self.model.player2.rect.x, self.model.player2.rect.y,13000,2)
                     self.model.bombs.add(bomb)
                     self.model.everything.add(bomb)


         elif event.type == pygame.KEYUP:
            # Player 1 Reverse Actions
            if event.key == pygame.K_LEFT:
                self.model.player1.changespeed(MOVE,0)
            elif event.key == pygame.K_RIGHT:
                self.model.player1.changespeed(-MOVE,0)
            elif event.key == pygame.K_UP:
                self.model.player1.changespeed(0,MOVE)
            elif event.key == pygame.K_DOWN:
                self.model.player1.changespeed(0,-MOVE)

            # Player 2 Reverse Actions
            if event.key == pygame.K_a:
                self.model.player2.changespeed(MOVE,0)
            elif event.key == pygame.K_d:
                self.model.player2.changespeed(-MOVE,0)
            elif event.key == pygame.K_w:
                self.model.player2.changespeed(0,MOVE)
            elif event.key == pygame.K_s:
                self.model.player2.changespeed(0,-MOVE)

                


         elif event.type == pygame.KEYUP:
             # Player 1 Reverse Actions
             if event.key == pygame.K_LEFT:
                 self.model.player1.changespeed(MOVE,0)
             elif event.key == pygame.K_RIGHT:
                 self.model.player1.changespeed(-MOVE,0)
             elif event.key == pygame.K_UP:
                 self.model.player1.changespeed(0,MOVE)
             elif event.key == pygame.K_DOWN:
                 self.model.player1.changespeed(0,-MOVE)

             # Player 2 Reverse Actions
             if event.key == pygame.K_a:
                 self.model.player2.changespeed(MOVE,0)
             elif event.key == pygame.K_d:
                 self.model.player2.changespeed(-MOVE,0)
             elif event.key == pygame.K_w:
                 self.model.player2.changespeed(0,MOVE)
             elif event.key == pygame.K_s:
                 self.model.player2.changespeed(0,-MOVE)

        
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
                                Fireup=Fire(model.bomb.x,model.bomb.y-SQUARELENGTH)
                                Firedown=Fire(model.bomb.x,model.bomb.y+SQUARELENGTH)
                                Fireleft=Fire(model.bomb.x-SQUARELENGTH,model.bomb.y)
                                Fireright=Fire(model.bomb.x+SQUARELENGTH,model.bomb.y)
                                for fire in [Fireup, Firedown, Fireleft, Fireright]:
                                    model.fires.add(fire)
                                    model.everything.add(fire)
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
                            
                            bomb = Bomb(model.player1.rect.x, model.player1.rect.y,13000,1)
                            model.bombs.add(bomb)
                            model.everything.add(bomb)
                            Fireup=Fire(bomb.rect.x,bomb.rect.y-SQUARELENGTH, 'N')
                            Firedown=Fire(bomb.rect.x,bomb.rect.y+SQUARELENGTH, 'S')
                            Fireleft=Fire(bomb.rect.x-SQUARELENGTH,bomb.rect.y, 'W')
                            Fireright=Fire(bomb.rect.x+SQUARELENGTH,bomb.rect.y, 'E')
                            for fire in [Fireup, Firedown, Fireleft, Fireright]:
                                model.fires.add(fire)
                                model.everything.add(fire)
                        
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
                            
                            bomb = Bomb(model.player2.rect.x, model.player2.rect.y,13000,2)
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


    
if __name__ == "__main__":
    
    # Creating the screen
    screen = pygame.display.set_mode((640, 480), 0, 32)
 
    menu_items = ('Start', 'Quit')
    funcs = {'Start': main,
             'Quit': sys.exit}
 
    pygame.display.set_caption('PLAYING WITH FIRE')
    gm = GameMenu(screen, funcs.keys(), funcs)
    gm.run()

    