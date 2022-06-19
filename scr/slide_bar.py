from dataclasses import dataclass
import pygame
from pygame.locals import *

@dataclass
class Slide:
    pos : tuple[int, int]
    min_value : float
    max_value : float
    round_value : float
    init_value : float = None
    size : tuple[int, int] = (500, 10)
    diameter : int = 30
    bar_color : tuple[int, int, int] = (0,100,100)
    ball_color : tuple[int, int, int] = (0,200,200)
    text_color : tuple[int, int, int] = (0,200,200)
    font_size : int = 40
    font_type : str = 'consolas'

    def __post_init__(self) -> None:
        if self.init_value == None:
            self.init_value = self.min_value
        else:
            self.init_value = max( min( self.init_value, self.max_value ), self.min_value )
        self.make_slide()
        self.press = False
        self.dt_press = 0
    
    def get_initial_pos(self) -> tuple[int, int]:
        dx = self.max_value - self.min_value
        cx = self.init_value - (self.min_value + dx/2)
        cxp = cx*self.size[0]/dx

        new_x = int(self.pos[0] + cxp)
        return new_x, self.pos[1]

    def make_slide(self) -> None:
        self.image = pygame.Surface( self.size )
        self.image.fill( self.bar_color )
        self.rect = self.image.get_rect(center=self.pos)

        self.ball = pygame.Surface( (self.diameter, self.diameter) ).convert_alpha()
        self.ball.set_colorkey((0,0,0))
        center = self.diameter//2, self.diameter//2
        pygame.draw.circle(self.ball, self.ball_color, center, self.diameter//2)
        self.rect_ball = self.ball.get_rect(center=self.get_initial_pos())

        font_type = pygame.font.match_font(self.font_type)
        self.font = pygame.font.Font(font_type, self.font_size)

    @property
    def percent(self) -> None:
        return ( self.rect_ball.centerx - self.rect.left )/self.size[0]*100
    
    @property
    def value(self) -> None:
        m = (self.max_value - self.min_value)/100
        y = self.percent*m + self.min_value
        return round(y, self.round_value)

    def draw_text(self, surface:pygame.Surface) -> None:
        #surf = self.font.render(f'{self.percent} %', True, (255,255,255))
        surf = self.font.render(f'{self.value}', True, self.text_color)
        rect = surf.get_rect(midleft=(self.pos[0] + self.size[0]//2 + 50, self.pos[1]))
        surface.blit(surf, rect)

    def draw(self, surface:pygame.Surface) -> None:
        surface.blit(self.image, self.rect)
        surface.blit(self.ball, self.rect_ball)
        self.draw_text(surface)
    
    def move_slide(self, posx:int) -> None:
        if posx > self.pos[0] + self.size[0]//2:
            x = self.pos[0] + self.size[0]//2
        elif posx < self.pos[0] - self.size[0]//2:
            x = self.pos[0] - self.size[0]//2
        else:
            x = posx
        self.rect_ball.centerx = x

    def mouse_event(self) -> None:
        press = pygame.mouse.get_pressed()[0]
        if press:
            pos = pygame.mouse.get_pos()
            collide = self.rect_ball.collidepoint(pos) or self.rect.collidepoint(pos)
            if self.dt_press == 0 and collide:
                self.press = True
            if self.press:
                self.move_slide(pos[0])
            self.dt_press += 1
        else:
            self.press = False
            self.dt_press = 0

    def update(self) -> None:
        self.mouse_event()


def test():
    size = (1000,800)
    fps = 60
    run = True
    font_size = 40

    pygame.init()
    
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    font_type = pygame.font.match_font('consolas')
    font = pygame.font.Font(font_type, font_size)

    slides = [
        Slide(pos=(300,300), min_value=0, max_value=0.1, round_value=4, init_value=75),
        Slide(pos=(300,400), min_value=50, max_value=100, round_value=2, init_value=100.5),
        Slide(pos=(300,500), min_value=0, max_value=100, round_value=0, init_value=10, size=(600,20), diameter=40, font_size=30)
        ]

    while run:
        if pygame.event.get(QUIT):
            run = False
        
        screen.fill( (10,10,10) )
        #screen.fill( (255,255,255) )
        font_surf = font.render(f'fps : {round(clock.get_fps(), 1)}', True, (255,255,255), (0,0,0))
        font_rect = font_surf.get_rect(topleft=(0,0))
        screen.blit(font_surf, font_rect)

        #print(slides[0].value)

        for slide in slides:
            slide.update()
            slide.draw(screen)

        pygame.display.flip()
        clock.tick(fps)
    
    pygame.quit()


if __name__ == '__main__':
    test()