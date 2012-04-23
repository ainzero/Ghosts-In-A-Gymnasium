from Chair import *
import pygame
from pygame.locals import *
from numpy import *
from PixelPerfect import *

class Sandbox():
    
    def __init__(self,screen,clock):

        
        #set screen to blit on, and draw it
        self.window = screen
        self.background = pygame.image.load("data/sprites/background/bbcourtsandbox.png").convert_alpha()
        self.window.blit(self.background, (0,0))
        pygame.display.flip()
        
        
        # set bookkeeping groups
        self.player_key_list = []
        self.chair_sprites = pygame.sprite.RenderUpdates() # Group just chair sprites
        
        # create landing zones for player and ghosts
        self.player_zone = Rect(941,647,180,110)
        self.ghosta_zone = Rect(68,647,180,110)
        self.ghostb_zone = Rect(236,308,180,110)
        self.mice_zone   = Rect(814,308,180,110)
    
        # set message to player
        player_request = pygame.font.SysFont("FreeMono",36)
        player_request.set_bold(True)
        mouse_request = pygame.font.SysFont("FreeMono",26)
        
        request_text = player_request.render("Hey Bro,Could you set up chairs for graduation?",True,(0,0,0)) 
        mouse_text = mouse_request.render("Use your janitor's mouse click,then press V when done!",True,(0,0,0))
        self.window.blit(request_text,(25,200))
        self.window.blit(mouse_text,(185,240))
        
        # set clock
        self.clock = clock
        self.time_passed = 0 # keeps track of passing time for all
        
        # show screen
        pygame.display.flip()
    
    def play(self):
        
        running = True
        
        while running:
        
            # tick game clock, pass int to limit the fps
            self.time_passed += self.clock.tick(60)

            # handles events (in this case if user closes game, stop running)
            running = self.exit_sandbox_stage()

            if len(self.chair_sprites):        
                # clear window
                self.chair_sprites.clear(self.window, self.background) 
                # Calculates sprites that need to be redrawn
                redraw = self.chair_sprites.draw(self.window)
                # blit areas of screen that need to be redrawn
                pygame.display.update(redraw)
            
        
        return False
        

    
    def exit_sandbox_stage(self):
        
        for event in pygame.event.get():
           
            if event.type == QUIT:
                return False
            if event.type == KEYDOWN:
                self.player_key_list = pygame.key.get_pressed()
                if self.player_key_list[K_v] is 1:
                    return False
            if event.type == MOUSEBUTTONDOWN:
                
                chair = Chair(event.pos)
                
                chi = ((chair.rect.top - 251) / 421.0)
                bounding_x_left = (chi * -205.0) + 223.0
                bounding_x_right = (chi * 213.0) + 899.0
                
                print event.pos
                
                if self.player_zone.collidepoint(event.pos) or self.ghosta_zone.collidepoint(event.pos) or self.ghostb_zone.collidepoint(event.pos) or self.mice_zone.collidepoint(event.pos):
                    continue
                
                if chair.rect.top <= 672 and chair.rect.top >= 251 and chair.rect.left <= bounding_x_right and chair.rect.left >= bounding_x_left:
                        self.chair_sprites.add(chair)

    
        return True


                
