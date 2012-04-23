import pygame
from pygame.locals import *

class TitleScreen():
    
    def __init__(self,screen):
        pygame.font.init()
        
        # Screen we're drawing to
        self.screen = screen
        
        # Font objects for title
        self.title_name = pygame.font.SysFont("FreeMono",64)
        self.player_request = pygame.font.SysFont("FreeMono",24)
        
    def display_title(self):
        
        
        title_text = self.title_name.render("Ghosts In A Gymnasium",True,(0,0,0))
        self.screen.blit(title_text,(195,380))
        
        request_text = self.player_request.render("Press S to Start!",True,(0,0,0))
        self.screen.blit(request_text,(485,500))
        
        pygame.display.flip()
        
        t = self.handle_events()
        return t

    def handle_events(self):
        keylist = pygame.key.get_pressed()
        for event in pygame.event.get():
            if keylist[K_s] is 1:
                return False
        
        return True
