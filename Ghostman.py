import pygame
import math
from numpy import *
from Player import *

class Ghostman(Player):

	# xy is a tuple
	def __init__(self, name, xy):

		# Initialize the pygame sprite part

		pygame.sprite.Sprite.__init__(self)

		# Everyone has a name ;)
		self.name = name

		# Getting the number of animation sprites. 3 for a ghostman
		self.animationmotiondict = {"walk":[[], [], [], []], "stand":[[], [], [], []]}
		self.animationframenumber = 0
		try:
			directions = ["up", "down", "left", "right"]
			motions = ["walk"]
			for motion in motions:
				directionlist = self.animationmotiondict[motion]

				for index, direction in enumerate(directions):

					for x in range(0, 2):

						directionlist[index].append(pygame.image.load("data/sprites/ghostman/" + motion + "/" + direction + "/" + "ghostman" + str(x) + ".png").convert_alpha())
					self.animationmotiondict[motion] = directionlist


				self.rect = self.animationmotiondict[motion][0][0].get_rect()
				self.image = self.animationmotiondict[motion][0][0]

		except:
			print "An error has occured loading Sprites. Check there location,existence, or number."


		# Sets ghostman position	
		self.rect.move_ip(xy[0], xy[1])
		self.position = array([float(self.rect.left), float(self.rect.top)]) # numpy array
		
		self.orientation = 0.0  # in radians, -pi/2 means oriented in positive y direction. pi means positive 

		# Keeps track of passed time since last update call
		self.elapsed = 0.0

		# Movement Related Attributes
		self.maxvelocity = array([32.0, 32.0])
		self.maxvelocitymagnitude = sqrt(vdot(self.maxvelocity, self.maxvelocity))
		self.velocity = array([0.0, -1.0])
		
		# Ghostman court collision stuff
		self.hit_top_bound = False
		self.hit_bottom_bound = False
		
		self.bounding_x_left = 0.0
		self.hit_left_bound = False
		
		self.bounding_x_right = 0.0
		self.hit_right_bound = False



	def animate(self, time):

		directions = {'up':0, 'down':1, 'left':2, 'right':3}

		# Are we moving?
		if self.velocity.any() > 0 or self.velocity.any() < 0:
			movement = 'walk'
		else:
			movement = 'stand'

		# How are we orientated?
		self.orientation = (math.atan2(self.velocity[1], -self.velocity[0])) * 57.29577 # results in deg.
		
		# pygame's y axis is positive in the 'downward' direction    
		if self.orientation >= 45 and self.orientation <= 135:
		    direction = 'down'
		elif self.orientation <= -45 and self.orientation >= -135:
		    direction = 'up'
		elif self.orientation > 135 or self.orientation < -135:
		    direction = 'right'
		else:
		    direction = 'left'

		if (time > 167): # number of milliseconds over 60fps before we flip a frame. This flips animation frames 10 times a second
			self.image = self.animationmotiondict[movement][directions[direction]][self.animationframenumber]
			if self.animationframenumber == 1:
				self.animationframenumber = 0
			else:
				self.animationframenumber = 1
			return True
		else:
			return False


	def update(self, frametime, animationtime, target):

		changedanimationframe = self.animate(animationtime)
		
                self.seekTarget(target,frametime)

		if changedanimationframe:
			return True
		else:
			return False

	def seekTarget(self, target, time):


                self.detect_court_collisions()

		direction = target.position - self.position
		#normalize direction
		direction = array([(direction[0] / sqrt(vdot(direction, direction))), direction[1] / sqrt(vdot(direction, direction))])

		#apply max speed
		direction *= self.maxvelocity
		self.velocity = direction
		
		# updates position with direction
		self.position += (direction * time)

		self.rect.topleft = (round(self.position[0]), round(self.position[1]))

		
		if sqrt(vdot(self.velocity,self.velocity)) > self.maxvelocitymagnitude:
			# normalize velocity vector
			self.velocity = array([velocity[0] / sqrt(vdot(self.velocity,self.velocity)),velocity[1] / sqrt(vdot(self.velocity,self.velocity))])
			#multiply by max acceleration
			self.velocity *= self.maxvelocity
		


	
