import pygame
import math


class Chair(pygame.sprite.Sprite):

	def __init__(self,xy):

	        # Initialize the pygame sprite part

	   	pygame.sprite.Sprite.__init__(self,)

	      
		
		self.image = pygame.image.load("data/sprites/chair/6chairblock.png").convert_alpha()
		self.rect = self.image.get_rect()
				   

	    # Sets chair position	
	   	self.rect.move_ip(xy[0], xy[1])

	   	#Court Collision Stuff
	   	self.hit_left_bound = False
	   	self.hit_right_bound = False
	   	self.hit_top_bound = False
	   	self.hit_bottom_bound = False



	def collision_detect(self,collision_rect):
		
	
		if self.rect.midright > collision_rect.midleft and self.hit_left_bound is False:
			self.rect.topleft = (self.rect.left, self.rect.top + s )

		'''if self.rect.midtop < collision_rect.midbottom and self.hit_bottom_bound is False:
		'''	self.rect.topleft = (self.rect.left,self.rect.top + 1)
	

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


	def update(self,frame_time,time_passed,target):
		self.detect_court_collisions()