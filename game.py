#import libraries that we need
import pygame,sys
from pygame.locals import *
from Ghostman import Ghostman
from Player import Player
from Mouse import Mouse
from Chair import Chair

import random

SCREEN_WIDTH     = 1200
SCREEN_HEIGHT    = 800
	
class Game(object):
	# user set constants
	

	def __init__(self):
	
		# 284 may be where hit boxes lie
	
		# get pygame up and running
		pygame.init()
		
		# Create main window
		self.window = pygame.display.set_mode((SCREEN_WIDTH,
		              SCREEN_HEIGHT))
		
		# Clock for ticking, variable for time between frame draws, 
		self.clock = pygame.time.Clock()
		self.time_passed = 0
		
		# Set main window Caption
		pygame.display.set_caption("Ghosts in a Gym")
		
		# Create background same size as window
		
		self.background = pygame.image.load("data/sprites/background/bbcourt.png").convert_alpha()
		# Draw background in window
		
		self.window.blit(self.background, (0,0))
			
		

		# display new background
		pygame.display.flip()
 
		# Let pygame know we want to listen to two events. Hitting the
		# escape key to exit, and pressing the X button on a window to
		# exit
		pygame.event.set_allowed([QUIT,KEYDOWN,KEYUP])
		pygame.key.set_repeat(1,1) # Allow for repeats
		self.player_key_press = [] # list of key presses by player
		
		# Sprite setup and construction, boolean for if we did change
		# a frame of animation
		self.updated_animation = False
		self.sprites = pygame.sprite.RenderUpdates() # Group containing all sprites
		


		# Chairs are also broken for the moment
		#Setting up barriers (Chairs)!
		
		for y in [(490,400),(590,400),(490,500),(590,500), (690,500), (390,400),(290,400),(490,300), (390,300), (590,600)]:
			temp = Chair(y)
			self.sprites.add(temp);

	
		self.player = Player("Anthony",(800,400))
		self.sprites.add(self.player)
		
		#self.ghostman_a = Ghostman("Melchoir",(400,300))
		#self.sprites.add(self.ghostman_a)
		
		#self.ghostman_b = Ghostman("Casper",(400,500))
		#self.sprites.add(self.ghostman_b)
		
		#self.mouse = Mouse("Mickey", (500,400))
		#self.sprites.add(self.mouse)
		#self.mouse = Mouse("Mic", (475,400))
		#self.sprites.add(self.mouse)
		#self.mouse = Mouse("Mikey", (490,400))
		#self.sprites.add(self.mouse)
		
		
		for sprite in self.sprites:
			self.window.blit(sprite.image,sprite.rect.topleft)
	
	def run(self):
	# This defines each frame of the game, and the tasks we execute
	# for each frame. The time it takes to do each task relates to our FPS
	# if each iteration of the loop takes 100 ms, then the game outputs
	# at 10 FPS (better check your code ;))
	
		running = True
		
		while running:
		
			# tick game clock, pass int to limit the fps
			self.time_passed += self.clock.tick(60)

			# handles events (in this case if user closes game, stop running)
			running = self.handleEvents()
		
			# Update title bar with fps
			pygame.display.set_caption("Ghosts in a Gymnasium - %f fps" % int(round(self.clock.get_fps())))
			
			# Update sprites
			for sprite in self.sprites:

				# Some broken code for collision detection, a work in progress

				

				self.sprites.remove(sprite)  # Don't want collisions with self
				
				# checking collisions
				hit = pygame.sprite.spritecollideany(sprite, self.sprites);
				collision_list = []
				collision_list.append(hit)

				if hit:
					for s in collision_list:
						if s.__class__.__name__ == 'Chair':
							s.collision_detect(sprite,.0167)

				self.updatedAnimation = sprite.update(.0167,self.time_passed,self.player)  # 0.0166666 1/60
				self.sprites.add(sprite)
				
			if self.updatedAnimation:
				self.time_passed = 0
					
			# Render sprites section
			# clear window
			self.sprites.clear(self.window, self.background) 
			# Calculates sprites that need to be redrawn
			redraw = self.sprites.draw(self.window)
			# blit areas of screen that need to be redrawn
			pygame.display.update(redraw)
			
			
			
	
	def handleEvents(self):
		# poll pygame for events,	 return false to game loop to end game
		
		
		for event in pygame.event.get():
				if event.type == QUIT:
					return False
				if event.type == KEYDOWN:
					
					keylist = pygame.key.get_pressed()
					
					if keylist[K_w] is 1:
						self.player_key_press.append('w')
					if keylist[K_s] is 1:
						self.player_key_press.append('s')
					if keylist[K_a] is 1: 
						self.player_key_press.append('a')
					if keylist[K_d] is 1:
						self.player_key_press.append('d')
				
					if event.key == K_ESCAPE:
						return False
				if event.type == KEYUP:
					keylist = pygame.key.get_pressed()
					
					if keylist[K_w] is 1:
						self.player_key_press.append('w')
					if keylist[K_s] is 1:
						self.player_key_press.append('s')
					if keylist[K_a] is 1: 
						self.player_key_press.append('a')
					if keylist[K_d] is 1:
						self.player_key_press.append('d')
		
		
		#	if len(self.playerkeypress) > 0:
		self.player.move(self.player_key_press)
		self.player_key_press = []
		
		return True
		




if __name__ == "__main__":
	game = Game()
	game.run()
