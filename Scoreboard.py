from time import time
import pygame

class Scoreboard(pygame.sprite.Sprite):
    
    def __init__(self,xy):
        
        # Initialize the pygame sprite part
        pygame.sprite.Sprite.__init__(self)
        
        self.mouse_dead_counter = 0
        self.xy = xy
        self.font= pygame.font.Font(None, 50)
        self.clock = pygame.time.Clock()
        self.elapsed = 0 
        
        self.minutes = 0
        self.seconds = 0
        
        self.render()
        
    def update(self,a,b,c):
        self.render()
        if self.seconds == 0:
            return False
            
    def render(self):
        self.elapsed += self.clock.tick()
        
        if self.elapsed >= 1000:
            self.seconds += 1
            if self.seconds >= 60:
                self.minutes += 1
                self.seconds = 0
            self.elapsed = 0
        
        if self.minutes < 1:
            self.image = self.font.render("Points: %d    Time Survived: %d seconds"%(self.mouse_dead_counter,self.seconds), True,(0,0,0))
        else:
            min = "minutes"
            if self.minutes == 1:
                min = "minute"     
            self.image = self.font.render("Points: %d    Time Survived: %d %s %d seconds"%(self.mouse_dead_counter,self.minutes,min,self.seconds), True,(0,0,0))
        
        self.rect = self.image.get_rect()
        self.rect.center = self.xy
