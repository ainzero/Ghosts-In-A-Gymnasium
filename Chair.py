import pygame
import math
from numpy import *


class Chair(pygame.sprite.Sprite):

    def __init__(self,xy):

            # Initialize the pygame sprite part

        pygame.sprite.Sprite.__init__(self,)

          
        
        self.image = pygame.image.load("data/sprites/chair/6chairblock.png").convert_alpha()
        self.rect = self.image.get_rect()
        

        # Sets chair position    
        self.rect.move_ip(xy[0], xy[1])
        self.rect.inflate_ip(0,-5)
        self.position = array([self.rect.left,self.rect.top])
        self.maxvelocity = array([16.0,16.0])
        self.maxvelocitymagnitude = sqrt(vdot(self.maxvelocity, self.maxvelocity))

           #Court Collision Stuff

        self.hit_left_bound = False
        self.hit_right_bound = False
        self.hit_top_bound = False
        self.hit_bottom_bound = False



    def collision_detect(self,object2,time):

        direction = object2.position - self.position

        direction = array([(direction[0] / sqrt(vdot(direction, direction))), direction[1] / sqrt(vdot(direction, direction))])

        orientation = (math.atan2(direction[1], -direction[0])) * 57.29577

        print orientation

        
        if ((orientation <= -145 and orientation >= -180) or # right
            (orientation >= 145 and orientation <= 180)):
            self.position[0] += (-4.0 * time)
           
        elif (orientation >= 45 and orientation <= 145): # bottom
            self.position[1] += (-4.0 * time)
        elif (orientation <=-45 and orientation >= -145): #top
            self.position[1] += (100 * time)
        elif ((orientation <= 0 and orientation >= -45) or # left
             (orientation >= 0 and orientation <= 45)):
            self.position[0] += (100.0 * time)
            
            
        print self.position
        
        self.rect.topleft = (round(self.position[0]), round(self.position[1]))
        
        
    def update(self,frame_time,time_passed,target):
        self.detect_court_collisions()

    def detect_court_collisions(self):
                # [233,211]      [907 211]
        #
        #    Basketball Court
        #
        # [10 672]       [1128 672]
        # Linear interpolation of left side of court (Player bounding)
        # Thanks to Jeff Sullivan!!
        
        chi = ((self.rect.top - 211) / 461.0)
        self.bounding_x_left = (chi * -223.0) + 233.0
            
            # Left Court
        if self.rect.left == math.ceil(self.bounding_x_left) or self.rect.left == math.floor(self.bounding_x_left):
                self.hit_left_bound = True
                print "Left Hit!"
        else:
            self.hit_left_bound = False
            
            self.bounding_x_right = (chi * 221) + 907         
            
            # Right Court
            if self.rect.left == math.ceil(self.bounding_x_right) or self.rect.left == math.floor(self.bounding_x_right):
                self.hit_right_bound = True
                print "Right Hit!"
            else:
                self.hit_right_bound = False
            
            # Bottom Court
            
            if self.rect.top >= 671 and self.rect.top <= 673:
                    print "Hit Bottom"
                    self.hit_bottom_bound = True
            else:
                    self.hit_bottom_bound = False
            
            #Top Court
            if self.rect.top >= 210 and self.rect.top <= 212:
                    print "Hit Top"
                    self.hit_top_bound = True
            else:
                    self.hit_top_bound = False

    
        