import pygame
from pygame.locals import *

class DidNotFeed(pygame.sprite.Sprite):
    
    def __init__(self,xy,ga,gb):
        
        # Initialize the pygame sprite part
        pygame.sprite.Sprite.__init__(self)
        
        
        self.ga = ga
        self.gb = gb
        self.mouse_dead_counter = 0
        self.xy = xy
        self.font= pygame.font.Font(None,36)
        self.clock = pygame.time.Clock()
        self.elapsed = 0 
        
        self.minutes = 0
        self.seconds = 0
        
        self.mouse_dead_a = False
        self.mouse_dead_b = False
        
        self.image = self.font.render("", True,(0,0,0))
        self.rect = self.image.get_rect()
        self.xy= xy
        
        self.just_killed = False
        
    def update_mouse_status(self,mouseflaga,mouseflagb):
        self.mouse_dead_a = mouseflaga
        self.mouse_dead_b = mouseflagb
    
    
    def update(self,a,b,c):
        # reset clock if a mouse has died
        
        self.elapsed += self.clock.tick()
        

        if not self.mouse_dead_a and not self.mouse_dead_b:
            if self.elapsed >= 30000:
                self.render()
                self.just_killed = True
                self.elapsed = 0
                self.gb.maxvelocity += 48
                self.ga.maxvelocity += 48
        else:
            self.image = self.font.render("", True,(0,0,0))
            
        self.just_killed  = False
        
        return False
    
    def render(self):
        self.image = self.font.render("Looks like someone didn't feed the animals...", True,(0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = self.xy
   
    
  
  
