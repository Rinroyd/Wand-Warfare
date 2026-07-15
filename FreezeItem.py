import pygame
from target import Target


# آیتم فریز: وقتی بازیکن این هدف رو بزنه، سرعت حرکت نشانگر حریف کند می‌شود
class FreezeItem(Target):
    def __init__(self, location, size, color):
        super().__init__(location, size, color)
    
        # بارگذاری تصویر آیتم فریز
        self.image = pygame.image.load("graphics/freeze_item.jpg").convert()
        
        # تنظیم کردن رنگ مشکی به عنوان رنگ شفاف تصویر
        self.image.set_colorkey((0, 0, 0))
        
        # تغییر اندازه‌ی تصویر متناسب با سایز هدف
        self.image = pygame.transform.scale(self.image, size)
        
        # بارگذاری صدای مخصوص برداشتن آیتم فریز
        pygame.mixer.init()
        self.freeze_sound = pygame.mixer.Sound("sfx/Timefreeze.mp3")
    
    def draw(self, surface):
        # رسم تصویر آیتم روی صفحه
        surface.blit(self.image, self.rect)
    
    def update(self):
        pass

    def apply_effect(self, player, other=None):
        # پخش صدای فریز و اعمال اثر کند شدن روی نشانگر حریف، نه خود بازیکنی که هدف را زده
        self.freeze_sound.play()
        other.cursor.speed = 2  # کاهش سرعت نشانگر حریف
        other.cursor.freeze_timer = 180  # مدت زمان اثر فریز 