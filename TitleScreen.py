import pygame
from pygame.locals import *

class TitleScreen:
    
    def __init__(self, window):
    
        self.window = window
    
        self.message1 = pygame.font.SysFont("FreeMono", 56)
        self.message2 = pygame.font.SysFont("FreeMono", 24)
        self.message3 = pygame.font.SysFont("FreeMono", 24)
    
    def display_title(self):
        
        running = True
        
        while running:
            
            running = self.event_handle()
        
            surface1 = self.message1.render("Ghosts In A Gymnasium", True, (0,0,0))
            surface2 = self.message2.render("Press 'S' to Start!", True, (0,0,0))
            surface3 = self.message3.render("Controls: Movement - WASD, Attack - Right CTRL ",True,(0,0,0)) 
            
            self.window.blit(surface1,(245,400))
            self.window.blit(surface2,(465,460))
            self.window.blit(surface3, (275,500))
            
            pygame.display.flip()
            
        return False
    
    
    
    
    def event_handle(self):
        for event in pygame.event.get():
            player_key_list = pygame.key.get_pressed()
            
            if player_key_list[K_s] is 1:
                    return False
        return True
        
    
    
    
    
