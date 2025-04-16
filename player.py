import pygame as pg
import numpy as np

class Player:
    def __init__(self):
        self.health = 6
        self.max_health = 6

    def take_damage(self, amount):
        print(f"[DMG] Taking {amount} damage")
        self.health = max(0, self.health - amount)

    def is_dead(self):
        return self.health <= 0

    def draw_health(self, screen):
        bar_width = 150
        bar_height = 20
        x = screen.get_width() - bar_width - 10
        y = screen.get_height() - bar_height - 10

        bg_rect = pg.Rect(x, y, bar_width, bar_height)
        pg.draw.rect(screen, (50, 50, 50), bg_rect)

        health_ratio = self.health / self.max_health
        fg_rect = pg.Rect(x, y, int(bar_width * health_ratio), bar_height)
        pg.draw.rect(screen, (0, 255, 0), fg_rect)

        pg.draw.rect(screen, (255, 255, 255), bg_rect, 2)

        if self.is_dead():
            font = pg.font.SysFont("Arial", 48, bold=True)
            text_surface = font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(text_surface, (
                screen.get_width() // 2 - text_surface.get_width() // 2,
                screen.get_height() // 2 - text_surface.get_height() // 2))

    def update(self):
        pass
