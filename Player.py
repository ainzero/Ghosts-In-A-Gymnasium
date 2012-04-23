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

        # Getting animation sprites
        
        
        self.animationmotiondict = {"walk":[[],[],[],[]],"stand":[[],[],[],[]],"attack":[[],[],[],[]]}
        self.animationframenumber = 0
        
        
        try:
            directions = ["up","down","left","right"]
            
            motions = ["stand","walk","attack"]
            for motion in motions:
                directionlist  = self.animationmotiondict[motion]
                for index,direction in enumerate(directions):

                    if (motion == 'walk' and (direction == 'up' or direction == 'down')):
                        numberofframes  = range(0,5)
                    if motion == 'walk' and (direction == 'left' or direction == 'right'):
                        numberofframes = range (0,5)
                    if motion == 'stand':
                        numberofframes = [0]
                    if motion == 'attack':
                        numberofframes = range(0,4)
                    
                    for x in numberofframes:
                        
                        directionlist[index].append(pygame.image.load("data/sprites/player/" + motion 
                            + "/" + direction + "/" + "player" + str(x) + ".png").convert_alpha())
                    self.animationmotiondict[motion] = directionlist


                self.rect = self.animationmotiondict[motion][0][0].get_rect()
                self.image = self.animationmotiondict[motion][0][0]
                self.hitmask = pygame.surfarray.array_colorkey(self.image)

        except:
            print "An error has occured loading Sprites. Check there location,existence, or number."
            raise Exception("Error!")

        self.hitmask = pygame.surfarray.array_colorkey(self.image)
        
        # Sets player position
        self.rect.move_ip(xy[0],xy[1])
        

        #self.rect.inflate_ip(-135,-35)
        self.position = array([self.rect.left,self.rect.top])

        # for per pixel collision detection
       
        self.touching_chair = False
        self.moving = False
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        
        self.hit_top_bound = False
        self.hit_bottom_bound = False
        
        self.bounding_x_left = 0.0
        self.hit_left_bound = False
        
        self.bounding_x_right = 0.0
        self.hit_right_bound = False

        # Keeps track of passed time since last update call
        self.elapsed = 0.0
            
    def detect_court_collisions(self):
                # [235,222]      [905 222]
        #
        #    Basketball Court
        #
        # [10 676]       [1126 676]
        # Linear interpolation of left side of court (Player bounding)
        # Thanks to Jeff Sullivan!!
        
        chi = ((self.rect.top - 222) / 465.0)
        self.bounding_x_left = (chi * -235.0) + 235.0
            
            # Left Court
        if self.rect.left <= math.ceil(self.bounding_x_left) and self.rect.left >= math.floor(self.bounding_x_left):
            self.hit_left_bound = True
            self.rect.topleft = (self.bounding_x_left + 1, self.rect.top)
            self.position = array([self.rect.left, self.rect.top])
            
        else:
                self.hit_left_bound = False
        
        chi = ((self.rect.top - 222) / 454.0)    
        self.bounding_x_right = (chi * 223) + 905          
        
                 # Right Court
        if self.rect.left <= math.ceil(self.bounding_x_right) and self.rect.left >= math.floor(self.bounding_x_right):
            self.hit_right_bound = True
            self.rect.topleft = (self.bounding_x_right - 1, self.rect.top)
            self.position = array([self.rect.left, self.rect.top])
        else:
            self.hit_right_bound = False
            
            # Bottom Court
            
        if self.rect.top >= 675 and self.rect.top <= 676:
                
                self.hit_bottom_bound = True
        else:
                self.hit_bottom_bound = False
            
            #Top Court
        if self.rect.top >= 221 and self.rect.top <= 222:
                
                self.hit_top_bound = True
        else:
                self.hit_top_bound = False
       
                
                
                
    
    def animate(self,time):
    
        directions  = {'up':0,'down':1,'left':2,'right':3}

        # Are we moving?
        
        if self.moving:
            movement = 'walk'
        else:
            movement = 'stand'
      
        direction = ""
        # pygame's y axis is positive in the 'downward' direction    
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
        if movement == 'walk' and self.animationframenumber > 4:
                self.animationframenumber = 0
        
        
        if movement == 'stand' and self.animationframenumber > 0:
           
                self.animationframenumber = 0
       
        if (time > 167): # number of milliseconds over 60fps before we flip a frame. This flips animation frames 10 times a second
            
            self.image = self.animationmotiondict[movement][directions[direction]][self.animationframenumber]
            
  
    def update(self,frametime,animationtime,target):

       self.animate(animationtime)
        
     
    
    
    def get_full_hitmask(self, image, rect):
        """returns a completely full hitmask that fits the image,
        without referencing the images colorkey or alpha."""
        mask=[]
        for x in range(rect.width):
            mask.append([])
            for y in range(rect.height):
                mask[x].append(True)
        return mask
  
