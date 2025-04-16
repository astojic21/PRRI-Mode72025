import pygame as pg
import sys
from settings import WIN_RES, MENU, GAME
from mode7 import *
from game import Game
from menu import Menu
from weapons import *
from player import Player

class App:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.mode7 = Mode7(self)
        self.player = Player()
        self.game = Game(self.mode7, self.player)
        self.menu = Menu(self)
        self.state = MENU
        self.weapon = REVOLVER
        self.shooting = False
        self.shotgun_sound = pg.mixer.Sound("music/shotgun sound effect.mp3")
        pg.mixer.music.load("music/Pixel Pulse.mp3")
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1, 0.0)
        print("Initialized in MENU state.")

    def update(self):
        if self.state == MENU:
            self.menu.update()
        elif self.state == GAME:
            if self.player.is_dead():
                return
            player_pos = self.mode7.pos
            self.mode7.update()
            self.game.update(player_pos)
            if self.weapon == MINIGUN and self.shooting:
                self.shotgun_sound.play()
                self.game.shoot_minigun(self.mode7.pos, self.mode7.angle)
            self.clock.tick()
            pg.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw_ui(self):
        font = pg.font.SysFont('Arial', 24)
        wave_text = font.render(f"Wave: {self.game.wave}", True, (255, 255, 255))
        self.screen.blit(wave_text, (10, 10))

        enemy_count = len(self.game.enemies)
        enemy_text = font.render(f"Enemies: {enemy_count}", True, (255, 255, 255))
        self.screen.blit(enemy_text, (10, 40))

        self.player.draw_health(self.screen)
        print("PLAYER HP =", self.player.health)

    def draw(self):
        if self.state == MENU:
            self.menu.draw()
        elif self.state == GAME:
            self.mode7.draw()
            self.game.draw(self.screen)
            self.draw_ui()
            pg.display.flip()

    def check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if self.state == MENU and event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                self.state = GAME
                self.switch_to_game()
                print("Starting GAME state.")
            elif self.state == GAME and self.player.is_dead() and event.type == pg.KEYDOWN and event.key == pg.K_r:
                self.__init__()  # restartaj sve
            elif event.type == pg.KEYDOWN and event.key == pg.K_j:
                self.weapon = REVOLVER
            elif event.type == pg.KEYDOWN and event.key == pg.K_k:
                self.weapon = SHOTGUN
            elif event.type == pg.KEYDOWN and event.key == pg.K_l:
                self.weapon = MINIGUN
            elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.shooting = True
                direction = np.array([np.cos(self.mode7.angle), np.sin(self.mode7.angle)])
                if self.weapon == REVOLVER:
                    self.shotgun_sound.play()
                    self.game.shoot_revolver(self.mode7.pos, self.mode7.angle)
                elif self.weapon == SHOTGUN:
                    self.shotgun_sound.play()
                    self.game.shoot_shotgun(self.mode7.pos, self.mode7.angle)
                elif self.weapon == MINIGUN:
                    self.shotgun_sound.play()
                    self.game.shoot_minigun(self.mode7.pos, self.mode7.angle)
            elif event.type == pg.KEYUP and event.key == pg.K_SPACE:
                self.shooting = False

    def switch_to_game(self):
        pg.mixer.music.stop()
        pg.mixer.music.load("music/Pixel Forge.mp3")
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1, 0.0)

    def run(self):
        while True:
            self.check_event()
            self.update()
            self.draw()
            pg.display.flip()

if __name__ == "__main__":
    app = App()
    app.run()