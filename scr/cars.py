import pygame
from pygame.locals import *
from pygame import Vector2
from os.path import join

class Car_1(pygame.sprite.Sprite):
    def __init__(self, width, height, img, pos, vel, ang) -> None:
        super().__init__()
        self.pos = pos
        self.vel = vel
        self.ang = ang
        self.front = Vector2(0,-1)
        self.size = (width, height)
        path = join('img', f'{img}.png')
        image = pygame.image.load(path).convert_alpha()
        self.org_image = pygame.transform.scale(image, self.size)
        self.image = self.org_image.copy()
        self.rect = self.image.get_rect(center=self.pos)
    
    def key_input(self):
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            self.pos += self.vel*self.front
        if keys[K_s]:
            self.pos -= self.vel*self.front
        if keys[K_a]:
            self.front.rotate_ip(-self.ang)
        if keys[K_d]:
            self.front.rotate_ip(self.ang)

    def update(self):
        self.key_input()
        ang = self.front.angle_to(Vector2(0,-1))
        self.image = pygame.transform.rotate(self.org_image, ang)
        self.rect = self.image.get_rect(center=self.pos)


class Car_2(Car_1):
    def __init__(self, width, height, img, pos, vel, ang, acc) -> None:
        super().__init__(width, height, img, pos, vel, ang)
        self.speed = 0
        self.turn = 0
        self.max_acc = acc
        self.max_vel = vel
        self.acc = 0

        self.friction = -0.01
        self.drag = -0.015
    
    def key_input(self):
        keys = pygame.key.get_pressed()
        #self.speed = 0
        self.acc = 0
        self.turn = 0
        if keys[K_w]:
            self.acc = self.max_acc
        if keys[K_s]:
            self.acc = -self.max_acc
        if keys[K_a]:
            self.turn = -self.ang
        if keys[K_d]:
            self.turn = self.ang

    def update(self):
        dt = 1
        self.key_input()

        if self.speed < 0.1:
            self.speed = 0
        
        friction = self.speed*self.friction
        drag = self.speed**2*self.drag
        
        self.acc += friction + drag

        front_wheel = self.pos + self.front*self.size[1]/4
        back_wheel = self.pos - self.front*self.size[1]/4
        self.speed += self.acc*dt
        if self.speed > self.max_vel:
            self.speed = self.max_vel

        back_wheel += self.speed*self.front*dt
        direct = self.front.rotate(self.turn)
        front_wheel += self.speed*direct*dt

        new_front = front_wheel - back_wheel
        new_front.normalize_ip()
        self.front = new_front
        self.pos = back_wheel + self.front*self.size[1]/4



        ang = self.front.angle_to(Vector2(0,-1))
        self.image = pygame.transform.rotate(self.org_image, ang)
        self.rect = self.image.get_rect(center=self.pos)
