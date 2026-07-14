import pygame
from target import Target

class TimeItem(Target):
    def __init__(self, location, size, color):
        super().__init__(location, size, color)

        self.frames = []
        for path in ["graphics/Time1.jpg", "graphics/Time2.jpg", "graphics/Time3.jpg"]:
            img = pygame.image.load(path).convert()
            img.set_colorkey((0, 0, 0))  
            img = pygame.transform.scale(img, size) 
            self.frames.append(img)
            
        self.current_frame = 0.0
        self.animation_speed = 0.12
        self.image = self.frames[0]
        
        pygame.mixer.init()
        self.timer_sound = pygame.mixer.Sound("sfx/Timer.mp3")
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def update(self):
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0.0
        self.image = self.frames[int(self.current_frame)]

    def apply_effect(self, player, other=None):
        self.timer_sound.play()
        player.time_left += 6