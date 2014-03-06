import pygame
from pygame.locals import *

def main():
	screen = pygame.display.set_mode((1024, 768))
	# screen = pygame.display.set_mode((1024, 768), FULLSCREEN)
	
	car = pygame.image.load('player1.png')
	screen.blit(car, (50, 100))
	pygame.display.flip()
	hello = input("Press Enter to Exit")

if __name__ == '__main__':
	main()
