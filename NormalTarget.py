import pygame
from target import Target

class NormalTarget(Target):
    def __init__(self, location, size, color):
        super().__init__(location, size, color)

        self.frames = []
        for path in ["graphics/Fly1.jpg", "graphics/Fly2.jpg", "graphics/Fly3.jpg"]:
            img = pygame.image.load(path).convert()
            img.set_colorkey((0, 0, 0))  
            img = pygame.transform.scale(img, size)
            self.frames.append(img)
            
        self.current_frame = 0.0
        self.animation_speed = 0.15
        self.image = self.frames[0]

        pygame.mixer.init()
        self.ghost_sound = pygame.mixer.Sound("sfx/Ghost.mp3")

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0.0
        self.image = self.frames[int(self.current_frame)]

    def apply_effect(self, player, other=None):
        self.ghost_sound.play()
        player.calculate_score(player.cursor.rect.center, self.rect.center)
        