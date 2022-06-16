from sim import *

if __name__ == '__main__':
    sim = Sim(width=1000, height=900, fps=60, font_size=30, car_type=2)
    sim.run()