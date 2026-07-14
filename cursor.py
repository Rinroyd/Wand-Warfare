import pygame
from game_object import GameObject

CURSOR_SPEED = 5   
class Cursor(GameObject):
    
    def __init__(self, location, size, color, image_path):
        super().__init__(location, size)
        self.color = color
        self.speed = CURSOR_SPEED   
        self.visible = False
        self.freeze_timer = 0
        self.visible_timer = 0
        self.normal_speed = CURSOR_SPEED
        
        self.image = pygame.image.load(image_path).convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, size)

    def move(self, dx, dy, screen_width, screen_height):
        self.rect.x += dx
        if self.rect.right >= screen_width:
            self.rect.right = screen_width
        elif self.rect.left <= 0:
            self.rect.left = 0
        
        self.rect.y += dy
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
        

    def draw(self, surface):
        if self.visible == False:
            return 
        
        surface.blit(self.image, self.rect)

        
    def update(self):
        if self.freeze_timer > 0:
            self.freeze_timer -= 1
            if self.freeze_timer == 0:
                self.speed = self.normal_speed
        
        if self.visible_timer > 0:
            self.visible_timer -= 1
            if self.visible_timer == 0:
                self.visible = False