import pygame as pg
import sys
from settings import WIN_RES
from mode7 import *
from enemies import Game  # Import the new Game class

class App:
    def __init__(self):
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.mode7 = Mode7(self)
        self.game = Game(self.mode7)  # Initialize the game logic

    def update(self):
        player_pos = self.mode7.pos  # Get player position from Mode7
        self.mode7.update()
        self.game.update(player_pos)  # Update enemies and projectiles
        self.clock.tick()
        pg.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw(self):
        self.mode7.draw()
        self.game.draw(self.screen)  # Draw enemies and projectiles
        pg.display.flip()

    def check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                # Shoot projectile in player's current direction
                direction = np.array([np.cos(self.mode7.angle), np.sin(self.mode7.angle)])
                self.game.shoot(self.mode7.pos, self.mode7.angle)

    def run(self):
        while True:
            self.check_event()
            self.update()
            self.draw()

if __name__ == '__main__':
    app = App()
    app.run()
