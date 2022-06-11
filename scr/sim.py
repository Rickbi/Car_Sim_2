import pygame
from pygame.locals import *
from cars import *

class Sim:
    def __init__(self, width, height, fps, font_size, car_type) -> None:
        self.fps = fps
        self.window_size = (width, height)

        pygame.init()

        self.screen = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()
        font = pygame.font.match_font('consolas')
        self.font = pygame.font.Font(font, font_size)

        self.init_Car(car_type)
    
    def init_Car(self, car_type):
        if car_type == 1:
            car = Car_1(width=50, height=100, img='car_1', pos=(100,100), vel = 5, ang = 3)
        else:
            car = Car_2(width=50, height=100, img='car_2', pos=(100,400), vel = 5, ang = 15, acc=0.1)
        
        self.car = pygame.sprite.GroupSingle(car)

    def show_fps(self, topleft):
        fps = round( self.clock.get_fps() )
        text_surf = self.font.render(f'fps: {fps}', True, (255,255,255), (0,0,0))
        text_rect = text_surf.get_rect(topleft=topleft)
        self.screen.blit(text_surf, text_rect)
    
    def run(self):
        run = True
        while run:
            if pygame.event.get(QUIT):
                run = False
            
            self.screen.fill( (50,50,50) )
            self.show_fps( (10,10) )
            self.car.draw(self.screen)
            self.car.update()

            self.clock.tick(self.fps)
            pygame.display.flip()
        
        pygame.quit()

def main():
    sim = Sim(width=900, height=500, fps=60, font_size=30, car_type=2)
    sim.run()

if __name__ == '__main__':
    main()
