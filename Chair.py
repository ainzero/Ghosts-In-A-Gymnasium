import pygame
import math
from numpy import *


class Chair(pygame.sprite.Sprite):

    def __init__(self,xy):

        # Initialize the pygame sprite part

        pygame.sprite.Sprite.__init__(self,)

        self.image = pygame.image.load("data/sprites/chair/6chairblock.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.hitmask = pygame.surfarray.array_colorkey(self.image)

        # Sets chair position    
        self.rect.center = xy
     
        #Court Collision Stuff
        self.hit_other_chair_top = False
        self.hit_other_chair_bottom = False
        self.hit_other_chair_left = False
        self.hit_other_chair_right = False
        
        
        self.hit_left_bound = False
        self.hit_right_bound = False
        self.hit_top_bound = False
        self.hit_bottom_bound = False

        self.blank = 0

  
  
