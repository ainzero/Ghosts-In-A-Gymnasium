import pygame
from pygame.locals import *
from Chair import Chair
from Graph import Graph
from PixelPerfect import *
import math

class Sandbox():
    
    def __init__(self,window,clock):
        
        self.window = window
        
        self.background = pygame.image.load("data/sprites/background/bbcourt.png").convert_alpha()
        self.window.blit(self.background, (0,0))
        
        self.clock = clock
 
        self.message1 = pygame.font.SysFont("FreeMono", 28)
        self.message1.set_bold(True)
        self.message2 = pygame.font.SysFont("FreeMono", 24)
        
        surface1 = self.message1.render("Hey, Could you set up six sets of chairs before graduation?", True, (0,0,0))
        surface2 = self.message2.render("Use your mouse to click locations for chairs", True, (0,0,0))
            
        self.window.blit(surface1,(30,125))
        self.window.blit(surface2,(325,200))
        
        
        pygame.display.flip()
        
        self.chair_sprites = pygame.sprite.RenderUpdates()
        
        self.chair_counter = 0
        
        self.chair_zone = Rect(247,309,680,372) # can fit ten chairs by 4 chairs
        
    
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
            
        
       #self.chair_graph = self.create_graph()
            
        
    def event_handle(self):
        player_key_list = pygame.key.get_pressed()
        for event in pygame.event.get():
            

                if event.type == MOUSEBUTTONDOWN:
                    
                    chair = Chair(event.pos)
                    
                    chi = ((chair.rect.top - 211) / 461.0)
                    bounding_x_left = (chi * -223.0) + 293.0  #233
                    bounding_x_right = (chi * 221) + 907 
                    
                    # chairs are only allowed in a square
                    # chairs are not allowed to overlap
                    
                    if self.chair_zone.collidepoint(event.pos):
                        chair.rect.center = event.pos
                        self.chair_sprites.add(chair)
                        self.chair_counter += 1
                    if self.chair_counter == 6:
                        self.graph = Graph(self.chair_sprites)
                        return False
        return True
    
