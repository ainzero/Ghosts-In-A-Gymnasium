#import libraries that we need
import pygame,sys
from pygame.locals import *
from Ghostman import Ghostman
from Player import Player
from Mouse import Mouse
from Chair import Chair
import time
from numpy import *
from PixelPerfect import *
from TitleScreen import *
from Sandbox import Sandbox

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
        pygame.display.set_caption("Ghosts in a Gymnasium")
        
        # Create background same size as window
        
        self.background = pygame.image.load("data/sprites/background/bbcourt.png").convert_alpha()
        # Draw background in window
        
        self.window.blit(self.background, (0,0))
            
        # display new background
        pygame.display.flip()
 
        
        # Creates title screen
        title_on = True
        title_screen = TitleScreen(self.window)
      
        # checks to see if player advanced past title screen
        while title_on:
            title_on = title_screen.display_title()
        
        # clear events, clear screen
        pygame.event.pump()
        self.window.blit(self.background, (0,0))
        pygame.display.flip()
        
        # Let pygame know we want to listen to just three events
        pygame.event.set_allowed([QUIT,KEYDOWN,KEYUP,MOUSEBUTTONDOWN])
        # list of key presses by player
        self.player_key_list = [] 
        
        # Allow for repeats, 2 ms apart
        pygame.key.set_repeat(1,2) 

        ####### Code for Sandbox stage  #######
        in_sandbox = True
        self.sandbox_stage = Sandbox(self.window,self.clock)
        
        while in_sandbox:
            in_sandbox = self.sandbox_stage.play()
        
        # list of all chairs player placed
        self.chair_list = self.sandbox_stage.chair_sprites
        
        # Group containing all sprites
        self.sprites = pygame.sprite.RenderUpdates()   
        
        for c in self.chair_list:
            self.sprites.add(c)
    
        # blit orginal background and show
        self.window.blit(self.background, (0,0))
        pygame.display.flip()
    
    
         # Sprite setup and construction, boolean for if we did change
        # a frame of animation
        self.updated_animation = False
        
        
        # setup player,ghosts, and mice
        self.player = Player("Anthony",(945,650))
        self.sprites.add(self.player)
        
        self.ghostman_a = Ghostman("Melchoir",(75,650))
        self.sprites.add(self.ghostman_a)
        
        self.ghostman_b = Ghostman("Casper",(250,305))
        self.sprites.add(self.ghostman_b)
        
        self.mouse1 = Mouse("Mickey", (815,305))
        self.sprites.add(self.mouse1)
        self.mouse2 = Mouse("Mike", (830,305))
        self.sprites.add(self.mouse2)
        self.mouse3 = Mouse("Mort", (845,305))
        self.sprites.add(self.mouse3)
        
        
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
        
        
            # Collision Detection
            '''
            li = spritecollide_pp(self.player,self.chair_sprites,0)
            
            if len(li): # player collided with chair
                for chair in li:
                    if chair.hit_top_bound or chair.hit_bottom_bound or chair.hit_right_bound or chair.hit_left_bound:
                        self.chair_boundry_move(chair)
                    else:
                        self.chair_move(chair,self.player)
            
            '''

            for sprite in self.sprites:
                sprite.update(.0167,self.time_passed, self.player)  # 0.0166666 1/60
                
                
            if self.time_passed > 167:
                self.time_passed = 0
            
            
           
            
            
            # clear window
            self.sprites.clear(self.window, self.background) 
            # Calculates sprites that need to be redrawn
            redraw = self.sprites.draw(self.window)
            # blit areas of screen that need to be redrawn
            pygame.display.update(redraw)
            
            
            
    
    def handleEvents(self):
        # poll pygame for events,     return false to game loop to end game
        
        self.player_key_list = pygame.key.get_pressed()
        for event in pygame.event.get():
                dx = 0
                dy = 0
                print event.type
                self.player.moving = False
                if event.type == QUIT:
                    return False
                
                elif event.type == KEYDOWN:
                    self.player.detect_court_collisions()
                    if self.player_key_list[K_RCTRL] is 1:
                        self.player.animate(self.time_passed,True)
                        self.window.blit(self.player.image,self.player.rect)
                        pygame.display.flip()
                    if self.player_key_list[K_w] is 1 and not self.player.hit_top_bound:
                        dy = -1
                        self.player.move_up = True
                        self.player.move_down = False
                        self.player.move_left = False
                        self.player.move_right = False
                    if self.player_key_list[K_s] is 1 and not self.player.hit_bottom_bound:
                        dy  = 1
                        self.player.move_down = True
                        self.player.move_top = False
                        self.player.move_left = False
                        self.player.move_right = False
                    if self.player_key_list[K_a] is 1 and not self.player.hit_left_bound: 
                        dx  = -1
                        self.player.move_left = True
                        self.player.move_down = False
                        self.player.move_up = False
                        self.player.move_right = False
                    if self.player_key_list[K_d] is 1 and not self.player.hit_right_bound:
                        dx = 1
                        self.player.move_right = True
                        self.player.move_down = False
                        self.player.move_left = False
                        self.player.move_up = False
                    if self.player_key_list[K_g] is 1:
                        print self.player.position
                        print self.player.bounding_x_right
                    self.player.moving = True
                elif event.type == KEYUP:
                    if self.player_key_list[K_RCTRL] is 1:
                        pass
                        #self.player.animate(self.time_passed,True)
                    if self.player_key_list[K_w] is 1 and dy == -1:
                        dy=0
                    if self.player_key_list[K_s] is 1 and dy == 1:
                        dy=0
                    if self.player_key_list[K_a] is 1 and dx == -1: 
                        dx=0
                    if self.player_key_list[K_d] is 1 and dx == 1:
                        dx=0
                
                self.player.rect.left += dx
                self.player.rect.top += dy
                self.player.position = array([self.player.rect.left, self.player.rect.top])
        
        
        return True




if __name__ == "__main__":
    game = Game()
    game.run()
