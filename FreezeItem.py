import pygame
from target import Target



class FreezeItem(Target):
    def __init__(self, location, size, color):
        super().__init__(location, size, color)
    
        self.image = pygame.image.load("graphics/freeze_item.jpg").convert()
        
        self.image.set_colorkey((0, 0, 0))
        
        self.image = pygame.transform.scale(self.image, size)
        
        pygame.mixer.init()
        self.freeze_sound = pygame.mixer.Sound("sfx/Timefreeze.mp3")
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def update(self):
        pass

    def apply_effect(self, player, other=None):
        self.freeze_sound.play()
        other.cursor.speed = 2
        other.cursor.freeze_timer = 180
        