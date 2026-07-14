import pygame
from cursor import Cursor
import random
import math

class Player:
    def __init__(self, name, cursor_color, cursor_image_path):
        self.score = 0
        self.time_left = 25
        self.bullets_left = 15
        self.applied_effects = []
        self.name = name
        self.last_shot_position = None
        self.combo = 0
        self.cursor = Cursor((random.randint(0, 780), random.randint(0 ,580)), (40, 40), cursor_color, cursor_image_path)

    def move_cursor(self, dx, dy, screen_width, screen_height):
        self.cursor.move(dx, dy, screen_width, screen_height)

    def shoot(self):
        if self.bullets_left == 0:
            return None
        
        if self.bullets_left > 0:
            self.bullets_left -= 1
            self.cursor.visible = True
            self.cursor.visible_timer = 40
        return self.cursor.rect.center
            
    def add_score(self, amount):
        self.score += amount
    
    def add_time(self, amount):
        self.time_left += amount
    
    def add_bullets(self, amount):
        self.bullets_left += amount
    
    def draw(self, surface):
        self.cursor.draw(surface)
    
    def calculate_score(self, hit_pos, target_center):
        x_distance = hit_pos[0] - target_center[0]
        y_distance = hit_pos[1] - target_center[1]
        distance = math.sqrt(x_distance**2 + y_distance**2)
        
        if distance > 30:     
            points = 1
        elif distance > 15:   
            points = 2
        else:              
            points = 3
            
        if self.combo >= 1:
            points += 2
            
        self.score += points
        self.combo += 1
        self.last_shot_position = hit_pos
        
        return points
    def miss(self):
        self.combo = 0

            