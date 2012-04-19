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
        self.animationmotiondict = {"walk":[[],[],[],[]],"stand":[[],[],[],[]]}
        self.animationframenumber = 0
        try:
            directions = ["up","down","left","right"]
            motions = ["stand"]
            for motion in motions:
                directionlist  = self.animationmotiondict[motion]
                for index,direction in enumerate(directions):

                    if (motion == 'walk'):
                        numberofframes  = range (0,7)
                    else:
                        numberofframes = range (0,1)

                    for x in numberofframes:
    
                        directionlist[index].append(pygame.image.load("data/sprites/player/" + motion 
                            + "/" + direction + "/" + "player" + str(x) + ".png").convert_alpha())
                    self.animationmotiondict[motion] = directionlist


                self.rect = self.animationmotiondict[motion][0][0].get_rect()
                
                self.image = self.animationmotiondict[motion][0][0]
                self.hitmask = pygame.surfarray.array_colorkey(self.image)

        except:
            print "An error has occured loading Sprites. Check there location,existence, or number."

        # Sets player position
        self.rect.move_ip(xy[0],xy[1])
        

        #self.rect.inflate_ip(-135,-35)
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
       
                
                
                
    
    def animate(self,time):
    
        directions  = {'up':0,'down':1,'left':2,'right':3}

        # Are we moving?
        if False:
            movement = 'walk'
            # How are we orientated?
            orient = (180 * math.atan2(self.velocity[1],-self.velocity[0])) / math.pi # results in deg.
        else:
            movement = 'stand'
            orient = 145 # stand right by default
        
        '''
        # pygame's y axis is positive in the 'downward' direction    
        if orient >= 45 and orient <= 135:
            direction = 'down'
        elif orient <= -45 and orient >= -135:
            direction = 'up'
        elif orient > 135 or orient < -135:
            direction = 'right'
        else:
            direction = 'left'  
        '''
        direction = 'right'


        if (time > 167): # number of milliseconds over 60fps before we flip a frame. This flips animation frames 10 times a second
            self.image = self.animationmotiondict[movement][directions[direction]][self.animationframenumber]
            
            # must update depending on animation, temp disabling
            '''
            if self.animationframenumber == 1:
                self.animationframenumber = 0
            else:
                self.animationframenumber = 1
            return True
        else:
            return False
            '''
            return True
    
    def update(self,frametime,animationtime,target):
        
        changedanimationframe = self.animate(animationtime)
        #print self.position
        if changedanimationframe:
            return True
        else:
            return False
    def get_full_hitmask(self, image, rect):
        """returns a completely full hitmask that fits the image,
        without referencing the images colorkey or alpha."""
        mask=[]
        for x in range(rect.width):
            mask.append([])
            for y in range(rect.height):
                mask[x].append(True)
        return mask
    def get_alpha_hitmask(image, rect, alpha=0):
        """returns a hitmask using an image's alpha.
       image->pygame Surface,
       rect->pygame Rect that fits image,
       alpha->the alpha amount that is invisible in collisions"""
        mask=[]
        for x in range(rect.width):
            mask.append([])
        for y in range(rect.height):
            mask[x].append(not image.get_at((x,y))[3]==alpha)
        return mask