import pygame
from pygame.locals import *
from pygame import Vector2
from os.path import join

class Car_1(pygame.sprite.Sprite):
    def __init__(self, width, height, img, pos, max_vel, turn_ang) -> None:
        super().__init__()
        self.pos : Vector2 = Vector2( pos )
        self.vel : Vector2 = Vector2(0, 0)
        self.direction : Vector2 = Vector2(0,-1)
        
        self.max_vel = max_vel
        self.turn_ang = turn_ang
        
        self.size = (width, height)
        path = join('img', f'{img}.png')
        image = pygame.image.load(path).convert_alpha()
        self.org_image = pygame.transform.scale(image, self.size)
        self.image = self.org_image.copy()
        self.rect = self.image.get_rect(center=self.pos)
    
    @property
    def speedometer(self):
        return self.vel.magnitude()

    def key_input(self):
        keys = pygame.key.get_pressed()
        self.vel = Vector2(0, 0)
        if keys[K_w]:
            self.vel = self.direction*self.max_vel
        if keys[K_s]:
            self.vel = -self.direction*self.max_vel
        if keys[K_a]:
            self.direction.rotate_ip(-self.turn_ang)
        if keys[K_d]:
            self.direction.rotate_ip(self.turn_ang)

    def update_img(self):
        ang = self.direction.angle_to(Vector2(0,-1))
        self.image = pygame.transform.rotate(self.org_image, ang)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt):
        self.key_input()
        self.pos += self.vel*dt

        self.update_img()


class Car_2(Car_1):
    def __init__(self, width, height, img, pos, max_vel, turn_ang, acc) -> None:
        super().__init__(width, height, img, pos, max_vel, turn_ang)
        
        self.acc : Vector2 = Vector2(0, 0)
        self.turn : int = 0

        self.engine = acc
        self.max_rev_vel = max_vel/2

        self.friction = -0.01
        self.drag = -0.01

        self.brake = -acc*0.8

        self.drift_speed = 4
        self.traction_slow = 0.9
        self.traction_fast = 0.0001
    
    def key_input(self):
        keys = pygame.key.get_pressed()
        self.acc = Vector2(0, 0)
        self.turn = 0
        if keys[K_w] or keys[K_UP]:
            self.acc = self.engine*self.direction
        if keys[K_s] or keys[K_DOWN]:
            self.acc = -self.engine*self.direction
        if keys[K_a] or keys[K_LEFT]:
            self.turn = -self.turn_ang
        if keys[K_d] or keys[K_RIGHT]:
            self.turn = self.turn_ang
        if keys[K_SPACE]:
            self.acc = self.vel*self.brake

    def apply_forces(self):
        friction = self.vel*self.friction
        drag = self.vel.magnitude()*self.vel*self.drag
        self.acc += friction + drag

    def move_1(self, dt):
        self.key_input()

        # Set the positions of the wheels.
        front_wheel = self.pos + self.direction*self.size[1]/4
        back_wheel = self.pos - self.direction*self.size[1]/4

        #Apply friction and drag.
        self.apply_forces()

        # Apply speed limits.
        self.vel += self.acc*dt
        speed = self.vel.magnitude()
        d = self.vel.dot(self.direction)

        if speed < 0.1:
            self.vel = Vector2(0, 0)
        elif d > 0:
            if speed > self.max_vel:
                self.vel = self.max_vel*self.vel.normalize()
        elif d < 0:
            if speed > self.max_rev_vel:
                self.vel = self.max_rev_vel*self.vel.normalize()

        # Move the positions of the wheels.
        back_wheel += self.vel*dt
        front_wheel += self.vel.rotate(self.turn)*dt

        # Find the new direction of the car.
        new_direction = front_wheel - back_wheel
        self.direction = new_direction.normalize()
        if d > 0:
            self.vel = self.vel.magnitude()*self.direction
        else:
            self.vel = -self.vel.magnitude()*self.direction

        # Move the position of the car.
        self.pos = back_wheel + self.direction*self.size[1]/4

    def move_2(self, dt):
        self.key_input()

        # Set the positions of the wheels.
        front_wheel = self.pos + self.direction*self.size[1]/4
        back_wheel = self.pos - self.direction*self.size[1]/4

        #Apply friction and drag.
        self.apply_forces()

        # Apply speed limits.
        self.vel += self.acc*dt
        speed = self.vel.magnitude()
        d = self.vel.dot(self.direction)

        if speed < 0.1:
            self.vel = Vector2(0, 0)
        elif d > 0:
            if speed > self.max_vel:
                self.vel = self.max_vel*self.vel.normalize()
        elif d < 0:
            if speed > self.max_rev_vel:
                self.vel = self.max_rev_vel*self.vel.normalize()

        # Move the positions of the wheels.
        back_wheel += self.vel*dt
        front_wheel += self.vel.rotate(self.turn)*dt

        # Find the new direction of the car.
        new_direction = front_wheel - back_wheel
        self.direction = new_direction.normalize()
        traction = self.traction_slow
        if speed >= self.drift_speed:
            traction = self.traction_fast
        if d > 0:
            self.vel = self.vel.lerp(self.vel.magnitude()*self.direction, traction)
        else:
            self.vel = self.vel.lerp(-self.vel.magnitude()*self.direction, traction)

        # Move the position of the car.
        self.pos = (back_wheel + front_wheel)/2#back_wheel + self.direction*self.size[1]/4


    def update(self, dt):
        self.move_2(dt)
        self.update_img()
