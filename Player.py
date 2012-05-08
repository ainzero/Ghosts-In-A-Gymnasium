import pygame
import math    
from numpy import *
#from Ghostman import Ghostman

class Player(pygame.sprite.Sprite):

    def __init__(self,name,xy):
        
        # Initialize the pygame sprite part
        pygame.sprite.Sprite.__init__(self)

        # Everyone has a name ;)
        self.name = name

        # Movement related flags
        
        self.moving = False
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False

        self.attacking = False

        # Getting animation sprites
        self.animationmotiondict = {"walk":[[],[],[],[]],"stand":[[],[],[],[]], "attack":[[],[],[],[]]}
        self.animationframenumber = 0
        
        try:
            directions = ["up","down","left","right"]
            motions = ["stand","walk","attack"]
            for motion in motions:
                directionlist  = self.animationmotiondict[motion]
                for index,direction in enumerate(directions):

                    if (motion == 'walk'):
                        numberofframes  = range (0,5)
                    if (motion == 'stand'):
                        numberofframes = [0]
                    if (motion == 'attack'):
                        numberofframes = range(0,4)
                
                    for x in numberofframes:
                        directionlist[index].append(pygame.image.load("data/sprites/player/" + motion 
                            + "/" + direction + "/" + "player" + str(x) + ".png").convert_alpha())
                    self.animationmotiondict[motion] = directionlist


                self.rect = self.animationmotiondict[motion][0][0].get_rect()
                self.image = self.animationmotiondict[motion][0][0]
                self.hitmask = pygame.mask.from_surface(self.image,127)

        except:
            print "An error has occured loading Sprites. Check there location,existence, or number."
            raise Exception("Error!")
        
        # Sets player position
        self.rect.topleft = xy
        
        # collision rect
        self.collision_rect = pygame.Rect(self.rect.left,self.rect.top + 75,63,10)
      
        
        self.position = array([self.rect.left,self.rect.top])
        self.blank = 0

        # for per pixel collision detection
       
        self.hit_top_bound = False
        self.hit_bottom_bound = False
        
        self.bounding_x_left = 0.0
        self.hit_left_bound = False
        
        self.bounding_x_right = 0.0
        self.hit_right_bound = False

        # Keeps track of passed time since last update call
        self.elapsed = 0.0
        
        #number of attack frames drawn
        self.aframes = 0
        
    def move(self,keypress):
        
        self.detect_court_collisions()
        
        
    def detect_court_collisions(self):
                # [233,211]      [907 211]
        #
        #    Basketball Court
        #
        # [10 672]       [1128 672]
        # Linear interpolation of left side of court (Player bounding)
        # Thanks to Jeff Sullivan!!
        
        chi = ((self.collision_rect.top - 211) / 461.0)
        self.bounding_x_left = (chi * -223.0) + 270.0
            
            # Left Court
        if self.collision_rect.left <= math.ceil(self.bounding_x_left): #or self.collision_rect.left == math.floor(self.bounding_x_left):
                self.hit_left_bound = True
                #self.collision_rect.left = self.collision_rect.left + (self.collision_rect.width / 2)
                left_difference = (math.fabs(self.collision_rect.left - self.bounding_x_left) / 4)
                self.rect = self.rect.move(left_difference, 0)
                self.collision_rect = self.collision_rect.move(left_difference, 0)

        else:
                self.hit_left_bound = False
            
                self.bounding_x_right = (chi * 221) + 907         
            
                 # Right Court
        if self.collision_rect.left >= math.ceil(self.bounding_x_right): # or self.collision_rect.left == math.floor(self.bounding_x_right):
            
            right_difference = (math.fabs(self.collision_rect.right - self.bounding_x_right) / 4)
            self.rect = self.rect.move(-right_difference, 0)
            self.collision_rect = self.collision_rect.move(-right_difference, 0)
            
            #self.hit_right_bound = True
            #self.collision_rect.left = self.collision_rect.left + - (self.collision_rect.width / 2)
 
        else:
            self.hit_right_bound = False
            
            # Bottom Court
            
        if self.collision_rect.bottom >= 755:

              #  self.collision_rect.top = self.collision_rect.top - (self.collision_rect.height / 2)
                self.hit_bottom_bound = True
        else:
                self.hit_bottom_bound = False
            
            #Top Court
        if self.collision_rect.top <= 298:

                #self.collision_rect.top = self.collision_rect.top + (self.collision_rect.height / 2)
                self.hit_top_bound = True
        else:
                self.hit_top_bound = False
       
    # assigned_movement is False
    def animate(self,time):
    
        directions  = {'up':0,'down':1,'left':2,'right':3}

  
        if self.moving:
            movement = 'walk'
        else:
            movement = 'stand'

        # pygame's y axis is positive in the 'downward' direction    
        #print "In Animate"
      
        direction = ""
        if self.move_down:
            direction = 'down'
        elif self.move_up:
            direction = 'up'
        elif self.move_right:
            direction = 'right'
        elif self.move_left:
            direction = 'left'
        else:
            direction = 'right'
 
        # set correct collision rectangle
        if movement == 'walk':
            self.collision_rect = pygame.Rect(self.rect.left,self.rect.top + 75,38,10)
        else:
            self.collision_rect = pygame.Rect(self.rect.left,self.rect.top + 75,63,10)
 
 
        self.animationframenumber += 1
        if self.animationframenumber >= 4 and movement == 'walk':
            self.animationframenumber = 0
        if self.animationframenumber > 0 and movement == 'stand':
            self.animationframenumber = 0
        
  
        if (time > 167): # number of milliseconds over 60fps before we flip a frame. This flips animation frames 10 times a second
            self.image = self.animationmotiondict[movement][directions[direction]][self.animationframenumber]
            pos = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = pos
            self.hitmask = pygame.mask.from_surface(self.image,127)
            return True
            # must update depending on animation, temp disabling
       
        return False
    
    def attack_animation(self,animation_time):
        directions  = {'up':0,'down':1,'left':2,'right':3}
        
        movement = 'attack'
        direction = ""
        if self.move_down:
            direction = 'down'
        elif self.move_up:
            direction = 'up'
        elif self.move_right:
            direction = 'right'
        elif self.move_left:
            direction = 'left'
        else:
            direction = 'right'
            
        self.animationframenumber += 1
        if self.animationframenumber >= 4:
            self.animationframenumber = 0
    
        if animation_time > 167:
            self.aframes += 1
            if self.aframes == 4:
                self.aframes = 0
            self.image = self.animationmotiondict[movement][directions[direction]][self.animationframenumber]
            pos = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = pos
            self.hitmask = pygame.mask.from_surface(self.image,127)
            return True
        return False
        
    
    def update(self,frametime,animationtime,target):
        
        if not self.attacking:
            changedanimationframe = self.animate(animationtime)
        else:
            changedanimationframe = self.attack_animation(animationtime)
        
        if changedanimationframe:
            return True
        else:
            return False
        
        return False
