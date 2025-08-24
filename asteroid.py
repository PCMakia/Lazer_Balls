from circleshape import CircleShape
from constants import *
import pygame, random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x,y,radius)
    
    def draw(self, screen):
        pygame.draw.circle(screen,"white", self.position, self.radius, 2)
    
    def update(self, dt):
        self.position += (self.velocity * dt)

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        # spawn smaller two
        angle = random.uniform(20,50)
        vect_1 = self.velocity.rotate(angle)
        vect_2 = self.velocity.rotate(-angle)
        new_rad = self.radius - ASTEROID_MIN_RADIUS
        x, y = self.position
        smol_1 = Asteroid(x,y,new_rad)
        smol_2 = Asteroid(x,y,new_rad)
        smol_1.velocity = vect_1
        smol_2.velocity = vect_2