import pygame
import math
from numpy import *
from Ghostman import Ghostman
import random
from time import time

class Mouse(pygame.sprite.Sprite):

    def __init__(self, name, xy):

        # Initialize the pygame sprite part

        pygame.sprite.Sprite.__init__(self)

        # Everyone has a name ;)
        self.name = name
        self.dead = False
        # Getting the number of animation sprites. 3 for a ghostman
        self.animationmotiondict = {"walk":[[], [], [], []], "stand":[[], [], [], []]}
        self.animationframenumber = 0
        try:
            directions = ["up", "down", "left", "right"]
            motions = ["walk","stand"]
            for motion in motions:
                directionlist = self.animationmotiondict[motion]
                           
                for index, direction in enumerate(directions):
                    
                    if motion == 'stand':
                        maxsprite = 1
                    else:
                        maxsprite = 4
                    for x in range(0, maxsprite):
                            
                            directionlist[index].append(pygame.image.load("data/sprites/mouse/" + motion + "/" +direction + "/" + "mouse" + str(x)+ ".png").convert_alpha())
                    self.animationmotiondict[motion] = directionlist
                 
                   
                self.rect = self.animationmotiondict[motion][0][0].get_rect()
                self.image = self.animationmotiondict[motion][0][0]
                self.hitmask = pygame.surfarray.array_colorkey(self.image)

        except:
            raise Exception("An error has occured loading Sprites. Check there location,existence, or number.")
           


        # Sets mouse position    
        self.rect.move_ip(xy[0], xy[1])
        self.position = array([float(self.rect.left), float(self.rect.top)]) # numpy array
       
        self.orientation = 0.0  # in radians, -pi/2 means oriented in positive y direction. #pi means positive 

        # Keeps track of passed time since last update call, stuff for waunder function
        self.elapsed = 0.0
        self.start_time = time()
        random.seed()
        self.random_time_check = random.randint(10,60)

        # Movement Related Attributes
        self.maxvelocity = array([random.uniform(1,32),random.uniform(1,32)])
        self.maxvelocitymagnitude = sqrt(vdot(self.maxvelocity, self.maxvelocity))
        self.velocity = array([random.uniform(-12,12),random.uniform(-12,12)])



    def animate(self, time):
        # print self.animationframenumber
        directions = {'up':0, 'down':1, 'left':2, 'right':3}

        # Are we moving?
        if self.velocity.any() > 0 or self.velocity.any() < 0:
            movement = 'walk'
        else:
            movement = 'stand'

        # How are we orientated?
        self.orientation = (180 * math.atan2(self.velocity[1], -self.velocity[0])) / math.pi 
        # results in deg.
        
        # pygame's y axis is positive in the 'downward' direction    
        if self.orientation >= 45 and self.orientation <= 135:
            direction = 'down'
        elif self.orientation <= -45 and self.orientation >= -135:
            direction = 'up'
        elif self.orientation > 135 or self.orientation < -135:
            direction = 'right'
        else:
            direction = 'left'

        #self.animationframenumber += 1
        if movement == 'stand' and self.animationframenumber > 0:
                self.animationframenumber = 0
        if movement == 'walk' and self.animationframenumber >= 3 :
                self.animationframenumber = 0
        self.animationframenumber += 1
        
        if (time > 167): 
        # number of milliseconds over 60fps before we flip a frame. 
        #This flips animation frames 10 times a second
            self.image = self.animationmotiondict[movement][directions[direction]][self.animationframenumber]
            pos = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = pos
            self.hitmask = pygame.mask.from_surface(self.image,127)
            return True
       
        
        return False


    def update(self, frametime, animationtime,target):
        
        if not self.dead:
            self.waunder(frametime,target)
            changedanimationframe = self.animate(animationtime)

            if changedanimationframe:
                return True
            else:
                return False
        return False

    def kill(self):
        
        self.image = pygame.image.load("data/sprites/mouse/dead/mouse0.png").convert_alpha()
        self.dead = True

    def detect_court_collisions(self):
                # [233,211]      [907 211]
        #
        #    Basketball Court
        #
        # [10 672]       [1128 672]
        # Linear interpolation of left side of court (Player bounding)
        # Thanks to Jeff Sullivan!!
        
        chi = ((self.rect.top - 309) / 436.0)
        self.bounding_x_left = (chi * -222.0) + 237.0
        
        # Left Court
        if self.rect.left == math.ceil(self.bounding_x_left) or self.rect.left == math.floor(self.bounding_x_left):
            self.velocity = array([-self.velocity[0],self.velocity[1]])

        chi = ((self.rect.top - 301) / 450.0)
        self.bounding_x_right = (chi * 222) + 959 #961       
        
        # Right Court
        if self.rect.left == math.ceil(self.bounding_x_right) or self.rect.left == math.floor(self.bounding_x_right):
            self.velocity = array([-self.velocity[0],self.velocity[1]])
    
        
        # Bottom Court
        if self.rect.top >= 748 and self.rect.top <= 750:
            self.velocity = array([self.velocity[0],-self.velocity[1]])
     
        
        #Top Court
        if self.rect.top >= 300 and self.rect.top <= 302:
            self.velocity = array([-self.velocity[0],-self.velocity[1]])
                    


    def waunder(self, timeframe, target):

        
        self.elapsed = time()

        if (self.elapsed - self.start_time) >= float(self.random_time_check):
            self.random_time_check = random.randint(10,60)
            self.start_time = self.elapsed
            self.velocity = array([random.uniform(-12,12),random.uniform(-12,12)])
               # updates position with direction
        self.detect_court_collisions()
        self.position += self.velocity * timeframe
        self.rect.topleft = (round(self.position[0]), round(self.position[1]))
        
