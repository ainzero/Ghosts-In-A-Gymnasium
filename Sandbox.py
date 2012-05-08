import pygame
from pygame.locals import *
from Chair import Chair
from PixelPerfect import *
import game

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
        
        surface1 = self.message1.render("Hey, Could you set up five sets of chairs before graduation?", True, (0,0,0))
        surface2 = self.message2.render("Use your mouse to click locations for chairs", True, (0,0,0))
            
        self.window.blit(surface1,(30,125))
        self.window.blit(surface2,(325,200))
        
        # Display board
        pygame.display.flip()
        
        self.chair_sprites = pygame.sprite.RenderUpdates()
        
        self.chair_counter = 0
        
        # Area where chairs can be placed
        self.chair_zone = Rect(247,309,630,400) 
    
    def play(self):
        
        running = True

        while running:
            
            # Will be false when 4 chairs is reached 
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

                    # chairs are only allowed in a square
                    # chairs are not allowed to overlap
                    
                    collide = False
                    
                    for d in self.chair_sprites:    
                        #collide = game.collision_check(d,chair)
                        collide = pygame.sprite.collide_circle(d,chair)
                    if not collide:
                        if self.chair_zone.contains(chair.rect):
                            chair.rect.center = event.pos
                            self.chair_sprites.add(chair)
                            self.chair_counter += 1
                        if self.chair_counter == 5:
                            return False
        return True
