#!/usr/bin/env python3
"""
Purple Ball Game
A platformer game where you control a purple ball and navigate through obstacles.
"""

import pygame
import sys
import random
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.8
JUMP_STRENGTH = -15
MOVE_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Purple Ball Game')
clock = pygame.time.Clock()

# Font setup
font = pygame.font.Font(None, 36)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.color = PURPLE
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.is_invisible = False
        self.invisible_duration = 0
        self.max_invisible_duration = 3 * FPS  # 3 seconds
        self.move_step = 20  # Distance to move in one step
    
    def update(self):
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Check boundaries
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vel_x = 0
        elif self.x + self.radius > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.radius
            self.vel_x = 0
        
        # Update invisibility
        if self.is_invisible:
            self.invisible_duration += 1
            if self.invisible_duration >= self.max_invisible_duration:
                self.is_invisible = False
                self.invisible_duration = 0
    
    def draw(self):
        if self.is_invisible:
            # Draw with transparency when invisible
            s = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (PURPLE[0], PURPLE[1], PURPLE[2], 100), (self.radius, self.radius), self.radius)
            screen.blit(s, (self.x - self.radius, self.y - self.radius))
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
    
    def toggle_invisibility(self):
        if not self.is_invisible:
            self.is_invisible = True
            self.invisible_duration = 0

class Platform:
    def __init__(self, x, y, width, height, color=GREEN):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

class Obstacle:
    def __init__(self, x, y, width, height, speed=2, direction=1):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = RED
        self.speed = speed
        self.direction = direction  # 1 for right, -1 for left
        self.initial_x = x
        self.move_range = 100  # How far it moves from initial position
    
    def update(self):
        self.rect.x += self.speed * self.direction
        
        # Change direction if moved too far
        if self.rect.x > self.initial_x + self.move_range:
            self.direction = -1
        elif self.rect.x < self.initial_x - self.move_range:
            self.direction = 1
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

class Goal:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = YELLOW
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.platforms = []
        self.obstacles = []
        self.goal = None
        self.player_start = (100, 300)
        self.generate_level()
    
    def generate_level(self):
        # Clear existing objects
        self.platforms = []
        self.obstacles = []
        
        # Add ground
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        
        if self.level_number == 1:
            # Level 1: Simple platforms and few obstacles
            self.platforms.append(Platform(200, 450, 100, 20))
            self.platforms.append(Platform(350, 350, 100, 20))
            self.platforms.append(Platform(500, 250, 100, 20))
            
            self.obstacles.append(Obstacle(300, 430, 30, 20, 2))
            
            self.goal = Goal(650, 210)
            
        elif self.level_number == 2:
            # Level 2: More complex platforms and obstacles
            self.platforms.append(Platform(150, 500, 100, 20))
            self.platforms.append(Platform(300, 400, 100, 20))
            self.platforms.append(Platform(450, 300, 100, 20))
            self.platforms.append(Platform(600, 200, 100, 20))
            
            self.obstacles.append(Obstacle(250, 480, 30, 20, 3))
            self.obstacles.append(Obstacle(400, 380, 30, 20, 3))
            self.obstacles.append(Obstacle(550, 280, 30, 20, 3))
            
            self.goal = Goal(650, 160)
            
        elif self.level_number == 3:
            # Level 3: Even more complex
            self.platforms.append(Platform(100, 500, 100, 20))
            self.platforms.append(Platform(250, 450, 100, 20))
            self.platforms.append(Platform(400, 400, 100, 20))
            self.platforms.append(Platform(550, 350, 100, 20))
            self.platforms.append(Platform(400, 250, 100, 20))
            self.platforms.append(Platform(250, 150, 100, 20))
            
            self.obstacles.append(Obstacle(150, 480, 30, 20, 4))
            self.obstacles.append(Obstacle(300, 430, 30, 20, 4))
            self.obstacles.append(Obstacle(450, 380, 30, 20, 4))
            self.obstacles.append(Obstacle(450, 230, 30, 20, 4))
            self.obstacles.append(Obstacle(300, 130, 30, 20, 4))
            
            self.goal = Goal(300, 110)
        
        else:
            # Generate random levels for higher levels
            num_platforms = 5 + self.level_number
            for i in range(num_platforms):
                x = random.randint(100, SCREEN_WIDTH - 200)
                y = random.randint(150, SCREEN_HEIGHT - 100)
                width = random.randint(80, 150)
                height = 20
                self.platforms.append(Platform(x, y, width, height))
            
            num_obstacles = 3 + self.level_number // 2
            for i in range(num_obstacles):
                platform = random.choice(self.platforms)
                x = platform.rect.x + random.randint(10, platform.rect.width - 40)
                y = platform.rect.y - 20
                speed = random.randint(2, 4)
                self.obstacles.append(Obstacle(x, y, 30, 20, speed))
            
            # Place goal on a high platform
            highest_platform = min(self.platforms, key=lambda p: p.rect.y)
            self.goal = Goal(highest_platform.rect.x + highest_platform.rect.width // 2 - 20, 
                           highest_platform.rect.y - 40)

class Game:
    def __init__(self):
        self.level_number = 1
        self.level = Level(self.level_number)
        self.player = Player(*self.level.player_start)
        self.game_state = "playing"  # "playing", "level_complete", "game_over"
        self.message = ""
        self.message_timer = 0
        self.key_a_held = False
        self.key_d_held = False
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
                if self.game_state == "playing":
                    if event.key == K_SPACE or event.key == K_w:
                        self.player.jump()
                    if event.key == K_z:
                        self.player.toggle_invisibility()
                    if event.key == K_a:
                        if not self.key_a_held:
                            self.player.x -= self.player.move_step
                        self.key_a_held = True
                    if event.key == K_d:
                        if not self.key_d_held:
                            self.player.x += self.player.move_step
                        self.key_d_held = True
                    if event.key == K_s:
                        self.player.vel_x = 0
                
                elif self.game_state == "level_complete":
                    if event.key == K_RETURN:
                        self.level_number += 1
                        self.level = Level(self.level_number)
                        self.player = Player(*self.level.player_start)
                        self.game_state = "playing"
                
                elif self.game_state == "game_over":
                    if event.key == K_RETURN:
                        self.level = Level(self.level_number)
                        self.player = Player(*self.level.player_start)
                        self.game_state = "playing"
            
            elif event.type == KEYUP:
                if event.key == K_a:
                    self.key_a_held = False
                    if not pygame.key.get_pressed()[K_d]:
                        self.player.vel_x = 0
                elif event.key == K_d:
                    self.key_d_held = False
                    if not pygame.key.get_pressed()[K_a]:
                        self.player.vel_x = 0
    
    def update(self):
        if self.game_state != "playing":
            return
        
        # Handle continuous movement for held keys
        if self.key_a_held:
            self.player.vel_x = -MOVE_SPEED
        elif self.key_d_held:
            self.player.vel_x = MOVE_SPEED
        
        # Update player
        self.player.update()
        
        # Check collisions with platforms
        self.player.on_ground = False
        for platform in self.level.platforms:
            if (self.player.y + self.player.radius > platform.rect.top and
                self.player.y - self.player.radius < platform.rect.bottom and
                self.player.x + self.player.radius > platform.rect.left and
                self.player.x - self.player.radius < platform.rect.right):
                
                # Collision from above (landing)
                if self.player.vel_y > 0 and self.player.y + self.player.radius > platform.rect.top and self.player.y < platform.rect.top:
                    self.player.y = platform.rect.top - self.player.radius
                    self.player.vel_y = 0
                    self.player.on_ground = True
                
                # Collision from below (hitting head)
                elif self.player.vel_y < 0 and self.player.y - self.player.radius < platform.rect.bottom and self.player.y > platform.rect.bottom:
                    self.player.y = platform.rect.bottom + self.player.radius
                    self.player.vel_y = 0
                
                # Collision from left
                elif self.player.vel_x > 0 and self.player.x + self.player.radius > platform.rect.left and self.player.x < platform.rect.left:
                    self.player.x = platform.rect.left - self.player.radius
                    self.player.vel_x = 0
                
                # Collision from right
                elif self.player.vel_x < 0 and self.player.x - self.player.radius < platform.rect.right and self.player.x > platform.rect.right:
                    self.player.x = platform.rect.right + self.player.radius
                    self.player.vel_x = 0
        
        # Update obstacles
        for obstacle in self.level.obstacles:
            obstacle.update()
        
        # Check collisions with obstacles
        for obstacle in self.level.obstacles:
            if (not self.player.is_invisible and
                self.player.x + self.player.radius > obstacle.rect.left and
                self.player.x - self.player.radius < obstacle.rect.right and
                self.player.y + self.player.radius > obstacle.rect.top and
                self.player.y - self.player.radius < obstacle.rect.bottom):
                
                self.game_state = "game_over"
                self.message = "Game Over! Press Enter to retry"
                break
        
        # Check if player reached the goal
        if (self.level.goal and
            self.player.x + self.player.radius > self.level.goal.rect.left and
            self.player.x - self.player.radius < self.level.goal.rect.right and
            self.player.y + self.player.radius > self.level.goal.rect.top and
            self.player.y - self.player.radius < self.level.goal.rect.bottom):
            
            self.game_state = "level_complete"
            self.message = f"Level {self.level_number} Complete! Press Enter for next level"
        
        # Check if player fell off the screen
        if self.player.y - self.player.radius > SCREEN_HEIGHT:
            self.game_state = "game_over"
            self.message = "Game Over! Press Enter to retry"
    
    def draw(self):
        # Clear the screen
        screen.fill(BLACK)
        
        # Draw platforms
        for platform in self.level.platforms:
            platform.draw()
        
        # Draw obstacles
        for obstacle in self.level.obstacles:
            obstacle.draw()
        
        # Draw goal
        if self.level.goal:
            self.level.goal.draw()
        
        # Draw player
        self.player.draw()
        
        # Draw level number
        level_text = font.render(f"Level: {self.level_number}", True, WHITE)
        screen.blit(level_text, (20, 20))
        
        # Draw invisibility status
        if self.player.is_invisible:
            invis_text = font.render(f"Invisibility: {(self.player.max_invisible_duration - self.player.invisible_duration) // FPS}s", True, WHITE)
            screen.blit(invis_text, (20, 60))
        else:
            ready_text = font.render("Invisibility Ready (Z)", True, WHITE)
            screen.blit(ready_text, (20, 60))
        
        # Draw game state messages
        if self.game_state != "playing":
            message_surface = font.render(self.message, True, WHITE)
            message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(message_surface, message_rect)
        
        # Update the display
        pygame.display.flip()

def main():
    game = Game()
    
    # Main game loop
    while True:
        game.handle_events()
        game.update()
        game.draw()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
