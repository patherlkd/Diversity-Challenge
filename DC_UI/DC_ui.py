import pygame

BLACK = [0, 0, 0]
WHITE = [255,255,255]


def setup(width,height):
	pygame.init()
	DISP_SIZE = width, height
	return pygame.display.set_mode(DISP_SIZE) ## return surface object

