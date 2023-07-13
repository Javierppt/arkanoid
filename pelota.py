import pygame
import math

FUERZA_POWERUP = 30
SPEED = 7

class Pelota(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("resources/pelota.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.verticalSpeed = -SPEED
        self.horizontalSpeed = SPEED
        self.strenght = 1
        self.bounce = pygame.mixer.Sound("resources/rebotePelota.mp3")

    def getDefaultSpeed():
        return SPEED

    def getSpeed(self):
        return self.horizontalSpeed,self.verticalSpeed
    
    def setSpeed(self,Hspeed,vSpeed):
        self.verticalSpeed = Hspeed
        self.horizontalSpeed = vSpeed

    def setAngle(self, angle):
        self.angle = angle

    def invertVSpeed(self):
        self.verticalSpeed*= -1
        
    def invertHSpeed(self):
        self.horizontalSpeed*= -1

    def move(self):
        self.rect.x += self.horizontalSpeed 
        self.rect.y += self.verticalSpeed

    def strengthUp(self):
        self.strenght = FUERZA_POWERUP 

    def serve(self, angle):
        self.horizontalSpeed = math.sin(math.radians(angle)) * SPEED
        self.verticalSpeed = -math.cos(math.radians(angle)) * SPEED
