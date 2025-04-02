import pygame as pg
import numpy as np

class Enemy:
    def __init__(self, pos, speed=0.02):
        self.pos = np.array(pos, dtype=np.float32)  # Store position as [x, y]
        self.speed = speed
        self.alive = True
        self.texture = pg.image.load('textures/airship_1.png').convert_alpha()
    
    def update(self, player_pos):
        # Simple AI: Move toward the player
        direction = player_pos - self.pos
        distance = np.linalg.norm(direction)
        if distance > 0:
            self.pos += (direction / distance) * self.speed
    
    def draw(self, screen, mode7):
        # Convert 3D world pos to screen pos using mode7's projection logic
        screen_x, screen_y, scale = mode7.project(self.pos)
        
        if scale > 0:  # Ensure the enemy is within view
            scaled_texture = pg.transform.scale(self.texture, (scale, scale))
            screen.blit(scaled_texture, (int(screen_x) - scale//2, int(screen_y) - scale//2))
    
    def check_collision(self, projectile):
        return np.linalg.norm(self.pos - projectile.pos) < 0.6  # Simple distance-based collision
