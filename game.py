import pygame as pg
import numpy as np
import random
from enemies import Enemy

class Projectile:
    def __init__(self, player_pos, player_angle, speed=0.5, max_distance=20):
        player_angle = np.radians(player_angle) if player_angle > np.pi * 2 else player_angle

        direction_x = np.cos(player_angle - np.pi/2)
        direction_y = -np.sin(player_angle - np.pi/2)
        self.direction = np.array([direction_x, direction_y], dtype=np.float32)

        offset_distance = 2.0
        rotated_offset_x = offset_distance * direction_x
        rotated_offset_y = offset_distance * direction_y

        self.pos = np.array(player_pos, dtype=np.float32) + np.array([rotated_offset_x, rotated_offset_y])
        self.speed = speed
        self.max_distance = max_distance
        self.start_pos = np.array(self.pos, dtype=np.float32)
        self.active = True

    def update(self):
        self.pos += self.direction * self.speed
        if np.linalg.norm(self.pos - self.start_pos) > self.max_distance:
            self.active = False

    def draw(self, screen, mode7):
        screen_x, screen_y, scale = mode7.project(self.pos)
        if scale > 0:
            radius = max(2, scale // 15)
            pg.draw.circle(screen, (0, 0, 0), (int(screen_x), int(screen_y)), radius)

class Game:
    def __init__(self, mode7, player):
        self.mode7 = mode7
        self.player = player
        self.projectiles = []
        self.enemies = []
        self.wave = 1
        self.spawn_wave(self.wave)

    def spawn_wave(self, wave_num):
        self.enemies.clear()
        for _ in range(5 + wave_num * 2):
            x, y = random.uniform(-10, 10), random.uniform(-10, 10)
            self.enemies.append(Enemy((x, y)))

    def update(self, player_pos):
        for proj in self.projectiles:
            proj.update()

        for proj in self.projectiles:
            for enemy in self.enemies:
                if enemy.check_collision(proj):
                    proj.active = False

        self.projectiles = [p for p in self.projectiles if p.active]

        for enemy in self.enemies:
            enemy.update(player_pos)
            for bullet in enemy.bullets:
                if np.linalg.norm(np.array(player_pos) - bullet.pos) < 0.5:
                    self.player.take_damage(1)
                    bullet.active = False

        self.enemies = [e for e in self.enemies if e.alive]

        if len(self.enemies) == 0:
            self.wave += 1
            self.spawn_wave(self.wave)

    def draw(self, screen):
        for proj in self.projectiles:
            proj.draw(screen, self.mode7)
        for enemy in self.enemies:
            enemy.draw(screen, self.mode7)

    def shoot_revolver(self, pos, angle):
        self.projectiles.append(Projectile(pos, angle, speed=0.6))

    def shoot_shotgun(self, pos, angle):
        for spread in [-0.2, 0, 0.2]:
            self.projectiles.append(Projectile(pos, angle + spread, speed=0.5))

    def shoot_minigun(self, pos, angle):
        self.projectiles.append(Projectile(pos, angle, speed=0.8))