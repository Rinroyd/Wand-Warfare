import pygame
from target import Target



class AmmoItem(Target):
    def __init__(self, location, size, color):
        super().__init__(location, size, color)

        self.image = pygame.image.load("graphics/Ammo.jpg").convert()
        
        self.image.set_colorkey((0, 0, 0))
        
        self.image = pygame.transform.scale(self.image, size)

        pygame.mixer.init()
        self.ammo_sound = pygame.mixer.Sound("sfx/Ammoglass.mp3")

    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def update(self):
        pass

    def apply_effect(self, player, other=None):
        self.ammo_sound.play()
        player.bullets_left += 3