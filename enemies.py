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


class Projectile:
    def __init__(self, player_pos, player_angle, speed=0.5, max_distance=20):
        # Convert angle to radians if necessary
        player_angle = np.radians(player_angle) if player_angle > np.pi * 2 else player_angle
        
        # Compute direction relative to player rotation (correcting for 90-degree offset)
        direction_x = np.cos(player_angle - np.pi/2)
        direction_y = -np.sin(player_angle - np.pi/2)
        self.direction = np.array([direction_x, direction_y], dtype=np.float32)
        
        # Offset projectile position relative to player orientation
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
        
        # Calculate projectile size based on distance traveled (larger at spawn, smaller as it moves)
        distance_traveled = np.linalg.norm(self.pos - self.start_pos)
        initial_size = 9  # Size at spawn
        min_size = 1  # Smallest size when far away
        size = max(min_size, initial_size - int(distance_traveled / self.max_distance * initial_size))
        
        pg.draw.circle(screen, (0, 0, 0), (int(screen_x), int(screen_y)), size)  # Blue projectile for better visibility


class Game:
    def __init__(self, mode7):
        self.mode7 = mode7
        self.enemies = [Enemy((5, 5)), Enemy((-5, 2)), Enemy((5, -5)), Enemy((-5, -2))]  # Example enemies
        self.projectiles = []
    
    def update(self, player_pos):
        for enemy in self.enemies:
            enemy.update(player_pos)
        for projectile in self.projectiles:
            projectile.update()
        
        # Check collisions and remove hit enemies
        for projectile in self.projectiles:
            for enemy in self.enemies:
                if enemy.check_collision(projectile):
                    self.enemies.remove(enemy)
                    projectile.active = False
                    break
        
        self.projectiles = [p for p in self.projectiles if p.active]  # Remove inactive projectiles
    
    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen, self.mode7)
        for projectile in self.projectiles:
            projectile.draw(screen, self.mode7)
    
    def shoot(self, player_pos, player_angle):
        self.projectiles.append(Projectile(player_pos, player_angle))

