from time import time
import pygame

class Scoreboard(pygame.sprite.Sprite):
    
    def __init__(self,xy):
        
        # Initialize the pygame sprite part
        pygame.sprite.Sprite.__init__(self)
        
        self.mouse_dead_counter = 0
        self.xy = xy
        self.font= pygame.font.Font(None, 50)
        
        self.start = time()
        self.minutes = 0
    
        
        self.render()
        
    def update(self,a,b,c):
        self.render()
        
    def render(self):
        
        elapsed = time() - self.start
        if elapsed > 60:
            self.minutes += 1
            self.seconds = 0
        self.seconds = elapsed
        
        self.image = self.font.render("Points: %d    Time Survived: %d minutes %d seconds"%(self.mouse_dead_counter,self.minutes,self.seconds), True,(0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = self.xy
