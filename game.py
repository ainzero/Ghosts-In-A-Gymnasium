#!/usr/bin/python
#import libraries that we need
import pygame,sys
from pygame.locals import *
from Ghostman import Ghostman
from Player import Player
from Mouse import Mouse
from Chair import *
from numpy import *
from PixelPerfect import *
from TitleScreen import *
from Sandbox import Sandbox
from Scoreboard import Scoreboard
import random


SCREEN_WIDTH     = 1200
SCREEN_HEIGHT    = 800
    
class Game(object):
    # user set constants
    

    def __init__(self):
    
        # 284 may be where hit boxes lie
    
        # get pygame up and running
        pygame.init()
        pygame.display.init()
        
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
        
        # Group containing just mice
        self.mice_group = pygame.sprite.RenderUpdates() 
        
        # Group containing just Ghosts
        self.ghost_group = pygame.sprite.RenderUpdates()
        
        for c in self.chair_list:
            self.sprites.add(c)
    
        # blit orginal background and show
        self.window.blit(self.background, (0,0))
        pygame.display.flip()
    
    
         # Sprite setup and construction, boolean for if we did change
        # a frame of animation
        self.updated_animation = False
        
        
        self.eating_time = 60
        
        # setup player,ghosts, and mice
        self.player = Player("Anthony",(945,650))
        self.sprites.add(self.player)
        
        
        self.ghostman_a = Ghostman("Melchoir",(75,650))
        self.sprites.add(self.ghostman_a)
        self.ghost_group.add(self.ghostman_a)
        
        self.ghostman_b = Ghostman("Casper",(250,305))
        self.sprites.add(self.ghostman_b)
        self.ghost_group.add(self.ghostman_b)
        
        
        self.mouse1 = Mouse("Mickey", (815,305))
        self.sprites.add(self.mouse1)
        self.mice_group.add(self.mouse1)
        self.mouse2 = Mouse("Mike", (400,305))
        self.sprites.add(self.mouse2)
        self.mice_group.add(self.mouse2)
        
        self.mice_array = [self.mouse1,self.mouse2]
        
        
        self.micea_dead = False
        self.miceb_dead = False
        
        
        self.score_board = Scoreboard((600,120))
        self.sprites.add(self.score_board)
        
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
            
            # player to chair
            ptoc = pygame.sprite.spritecollide(self.player, self.chair_list, False, pygame.sprite.collide_mask)
            if len(ptoc): # player collided with chair
                for chair in ptoc:
                    self.mtv_collision_reaction(self.player,chair)
            
            # mouse to chair
            for mouse in self.mice_group:
                mtoc = pygame.sprite.spritecollide(mouse, self.chair_list, False, pygame.sprite.collide_mask)
                if len(mtoc):
                    for chair in mtoc:
                        self.mouse_chair_collision(mouse,chair)
        
            # player to mouse
            ptom = pygame.sprite.spritecollide(self.player, self.mice_group, False, pygame.sprite.collide_mask)
            
            if self.player.attacking:
                for mouse in ptom:
                    mouse.kill()
            
            #ghosts eating mice
            if self.mice_array[0].dead:
                distance = sqrt(pow((self.mice_array[0].position[0] - self.ghostman_a.position[0]),2) + pow((self.mice_array[0].position[1] - self.ghostman_a.position[1]),2))
                if distance > 2 :
                    self.ghostman_a.not_eating = False
                    self.ghostman_a.eat_mouse(self.mice_array[0], .0167)
                else:
                    self.ghostman_a.eating_timer += 1
                    if self.ghostman_a.eating_timer > self.eating_time:
                        self.mice_array[0].dead = False
                        self.score_board.mouse_dead_counter += 1
                        self.ghostman_a.maxvelocity += 12
                        self.ghostman_a.not_eating = True
                        self.ghostman_a.eating_timer = 0
                        self.mice_array[0].rect.center = (815,305)
                    
            if self.mice_array[1].dead:
                distance = sqrt(pow((self.mice_array[1].position[0] - self.ghostman_b.position[0]),2) + pow((self.mice_array[1].position[1] - self.ghostman_b.position[1]),2))
                if distance > 2:
                    self.ghostman_b.not_eating = False
                    self.ghostman_b.eat_mouse(self.mice_array[1], .0167)
                else:
                    self.ghostman_b.eating_timer += 1
                    if self.ghostman_b.eating_timer > self.eating_time:
                        self.mice_array[1].dead = False
                        self.score_board.mouse_dead_counter += 1
                        self.ghostman_b.maxvelocity += 12
                        self.ghostman_b.eating_timer = 0
                        self.ghostman_b.not_eating = True
                        self.mice_array[1].rect.center = (245,305)
                
           
            for sprite in self.sprites:
                sprite.update(.0167,self.time_passed, self.player)  # 0.0166666 1/60
                
            #ghost to chair
            for ghost in self.ghost_group:
                gtoc = pygame.sprite.spritecollide(ghost, self.chair_list, False, pygame.sprite.collide_mask)
                if len(gtoc):
                    for chair in gtoc:
                        self.ghost_collision_reaction(ghost,chair)
                        ghost.collide = True    
            
            # player to ghost
            gtop = pygame.sprite.spritecollide(self.player, self.ghost_group, False, pygame.sprite.collide_mask)
            if len(gtop):
                running = False 
                
                
            if self.time_passed > 167:
                self.time_passed = 0

            # clear window
            self.sprites.clear(self.window, self.background) 
            # Calculates sprites that need to be redrawn
            redraw = self.sprites.draw(self.window)
            # blit areas of screen that need to be redrawn
            pygame.display.update(redraw)
        
        self.game_over()    
    
    
    def game_over(self):        
        
        self.window.blit(self.background, (0,0))
        
    
        self.message1 = pygame.font.SysFont("FreeMono", 56)
        self.message3 = pygame.font.SysFont("FreeMono", 24)
        self.message2 = pygame.font.SysFont("FreeMono", 24)
        
        
        surface1 = self.message1.render("Game Over", True, (0,0,0))
        surface3 = self.message3.render("Your Score: You survived for %d minutes, %d seconds with %d points"%(self.score_board.minutes,self.score_board.seconds,self.score_board.mouse_dead_counter), True,(0,0,0))
        surface2 = self.message2.render("Press 'E' to play again, or escape to quit", True, (0,0,0))
        
        self.window.blit(surface1,(445,50))
        self.window.blit(surface3,(150,120))
        self.window.blit(surface2,(310,150))
        
        pygame.display.flip()
        
        waiting = True
        
        while waiting:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_e:
                        self.__init__()
                        self.run()
                    if event.key == K_ESCAPE:
                        pygame.quit()
            

            
    def player_chair_collision(self,chair):
        pass
        '''
        if self.player_key_list[K_w] is 1 :
            self.player.rect.top += 2
        if self.player_key_list[K_s] is 1:
            self.player.rect.top -= 2
        if self.player_key_list[K_a] is 1: 
            self.player.rect.left += 2
        if self.player_key_list[K_d] is 1:
            self.player.rect.left -= 2
        '''
        
    def mtv_collision_reaction(self,moving_object, stationary_object):
        """Resolve the collision."""
        
        delta_x_left = stationary_object.rect.left - moving_object.rect.right # The minimum distance necessary to put the Unit flush with the left side of the Platform
        delta_x_right = stationary_object.rect.right - moving_object.rect.left # The minimum distance necessary to put the Unit flush with the right side of the Platform
        delta_y_up = stationary_object.rect.top - moving_object.rect.bottom # The minimum distance necessary to put the Unit flush with the top of the Platform
        delta_y_down = stationary_object.rect.bottom - moving_object.rect.top # The minimum distance necessary to put the Unit flush with the bottom of the Platform
        smallest_delta = sorted([math.fabs(delta_x_left), math.fabs(delta_x_right), math.fabs(delta_y_up), math.fabs(delta_y_down)])[0] #Obtain the vector with the smallest magnitude.
        
        if (math.fabs(delta_x_left) == smallest_delta):
            moving_object.rect = moving_object.rect.move(delta_x_left, 0)
            return True
        elif (math.fabs(delta_x_right) == smallest_delta):
            moving_object.rect = moving_object.rect.move(delta_x_right, 0)
            return True
        elif (math.fabs(delta_y_up) == smallest_delta):
            moving_object.rect = moving_object.rect.move(0, delta_y_up)
            return True
        elif (math.fabs(delta_y_down) == smallest_delta):
            moving_object.rect = moving_object.rect.move(0, delta_y_down)
            return True
        return False
    def ghost_collision_reaction(self,moving_object, stationary_object):
        """Resolve the collision."""
        
        delta_x_left = stationary_object.rect.left - moving_object.rect.right # The minimum distance necessary to put the Unit flush with the left side of the Platform
        delta_x_right = stationary_object.rect.right - moving_object.rect.left # The minimum distance necessary to put the Unit flush with the right side of the Platform
        delta_y_up = stationary_object.rect.top - moving_object.rect.bottom # The minimum distance necessary to put the Unit flush with the top of the Platform
        delta_y_down = stationary_object.rect.bottom - moving_object.rect.top # The minimum distance necessary to put the Unit flush with the bottom of the Platform
        smallest_delta = sorted([math.fabs(delta_x_left), math.fabs(delta_x_right), math.fabs(delta_y_up), math.fabs(delta_y_down)])[0] #Obtain the vector with the smallest magnitude.
        
        #moving_object.maxvelocity =  -1 * moving_object.maxvelocity
        if (math.fabs(delta_x_left) == smallest_delta):
            moving_object.rect = moving_object.rect.move(delta_x_left , 0)
        elif (math.fabs(delta_x_right) == smallest_delta):
            moving_object.rect = moving_object.rect.move(delta_x_right , 0)
        elif (math.fabs(delta_y_up) == smallest_delta):
            moving_object.rect = moving_object.rect.move(0, delta_y_up)
        elif (math.fabs(delta_y_down) == smallest_delta):
            moving_object.rect = moving_object.rect.move(0, delta_y_down)
            
     
    def mouse_chair_collision(self,mouse, chair):
        
        # get direction to chair
        direction = chair.position - mouse.position
        
        #normalize direction
        direction = array([(direction[0] / sqrt(vdot(direction, direction))), direction[1] / sqrt(vdot(direction, direction))])
        
        # move opposite direction to chair
        direction *= (mouse.maxvelocity * -1)
        
        mouse.velocity = direction 
        
        #mouse.position += (mouse.velocity * .0167)
        #mouse.rect.topleft = (round(mouse.position[0]), round(mouse.position[1]))
    
    
    
    def handleEvents(self):
        # poll pygame for events,     return false to game loop to end game
        
        
        for event in pygame.event.get():
                self.player_key_list = pygame.key.get_pressed()
                dx = 0
                dy = 0
                
                self.player.moving = False
                if event.type == QUIT:
                    return False
                
                if event.type == KEYDOWN:
                    self.player.detect_court_collisions()
                    if event.key == K_RCTRL:
                        self.player.attacking = True
                    if event.key == K_w and not self.player.hit_top_bound:
                        dy = -2
                        self.player.move_up = True
                        self.player.move_down = False
                        self.player.move_left = False
                        self.player.move_right = False
                    if event.key == K_s and not self.player.hit_bottom_bound:
                        dy  = 2
                        self.player.move_down = True
                        self.player.move_top = False
                        self.player.move_left = False
                        self.player.move_right = False
                    if event.key == K_a and not self.player.hit_left_bound: 
                        dx  = -2
                        self.player.move_left = True
                        self.player.move_down = False
                        self.player.move_up = False
                        self.player.move_right = False
                    if event.key == K_d and not self.player.hit_right_bound:
                        dx = 2
                        self.player.move_right = True
                        self.player.move_down = False
                        self.player.move_left = False
                        self.player.move_up = False
                    if event.key == K_g:
                        print self.player.position
                        print self.player.bounding_x_right
                    self.player.moving = True
                
                elif event.type == pygame.KEYUP:
                    if event.key == K_RCTRL:
                        self.player.attacking = False
                    if event.key == K_w and dy == -2:
                        dy=0
                    if event.key == K_s and dy == 2:
                        dy=0
                    if event.key == K_a and dx == -2: 
                        dx=0
                    if event.key == K_d and dx == 2:
                        dx=0
                
                self.player.rect.left += dx
                self.player.rect.top += dy
                self.player.position = array([self.player.rect.left, self.player.rect.top])

        return True




if __name__ == "__main__":
    game = Game()
    game.run()
