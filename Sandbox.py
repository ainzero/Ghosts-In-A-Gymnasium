import pygame
from pygame.locals import *
from Chair import Chair


class Sandbox():
    
    def __init__(self,window,clock):
        
        self.window = window
        
        self.background = pygame.image.load("data/sprites/background/bbcourtsandbox.png").convert_alpha()
        self.window.blit(self.background, (0,0))
        
        self.clock = clock
 
        self.message1 = pygame.font.SysFont("FreeMono", 28)
        self.message1.set_bold(True)
        self.message2 = pygame.font.SysFont("FreeMono", 24)
        
        surface1 = self.message1.render("Hey Janitor, Could you set up some chairs before graduation?", True, (0,0,0))
        surface2 = self.message2.render("Use your janitor's mouse to click locations, press 'V' when done!", True, (0,0,0))
            
        self.window.blit(surface1,(30,200))
        self.window.blit(surface2,(135,250))
        
        pygame.display.flip()
        
        self.chair_sprites = pygame.sprite.RenderUpdates()
        
        
        self.player_zone = Rect(941,647,180,130)
        self.ghosta_zone = Rect(90,647,180,130)
        self.ghostb_zone = Rect(220,305,180,130)
        self.mice_zone = Rect(802,305,180,130)
    
    
    def play(self):
        
        running = True
        
        while running:
            
            running = self.event_handle()
            
            # clear window
            self.chair_sprites.clear(self.window, self.background) 
            # Calculates sprites that need to be redrawn
            redraw = self.chair_sprites.draw(self.window)
            # blit areas of screen that need to be redrawn
            pygame.display.update(redraw)
            
            
            
    
    
    def event_handle(self):
        player_key_list = pygame.key.get_pressed()
        for event in pygame.event.get():
            

                if event.type == MOUSEBUTTONDOWN:
                    chair = Chair(event.pos)
                    print event.pos
                    chi = ((chair.rect.top - 211) / 461.0)
                    bounding_x_left = (chi * -223.0) + 293.0  #233
                    bounding_x_right = (chi * 221) + 907 
                    
                    if (event.pos[1] <= 715 and event.pos[1] >= 300) and event.pos[0] >= bounding_x_left and event.pos[0] <= bounding_x_right:
                        
                        if not self.player_zone.collidepoint(event.pos) and not self.ghosta_zone.collidepoint(event.pos) and not self.ghostb_zone.collidepoint(event.pos) and not self.mice_zone.collidepoint(event.pos) :
                            chair.rect.center = event.pos
                            self.chair_sprites.add(chair)
                
                if event.type == KEYDOWN:
                    player_key_list = pygame.key.get_pressed()
                    if player_key_list[K_v] is 1:
                        return False
        return True
        
        
        
