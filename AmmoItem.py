import pygame
from target import Target


# آیتم مهمات: وقتی بازیکن این هدف رو بزنه، تعدادی گلوله بهش اضافه می‌شه
class AmmoItem(Target):
    def __init__(self, location, size, color):
        super().__init__(location, size, color)

        # بارگذاری تصویر آیتم مهمات
        self.image = pygame.image.load("graphics/Ammo.jpg").convert()
        
        # تنظیم رنگ مشکی به عنوان رنگ شفاف تصویر
        self.image.set_colorkey((0, 0, 0))
        
        # تغییر اندازه‌ی تصویر متناسب با سایز هدف
        self.image = pygame.transform.scale(self.image, size)

        # بارگذاری صدای مخصوص برداشتن آیتم مهمات
        pygame.mixer.init()
        self.ammo_sound = pygame.mixer.Sound("sfx/Ammoglass.mp3")

    def draw(self, surface):
        # رسم تصویر آیتم روی صفحه
        surface.blit(self.image, self.rect)
    
    def update(self):
        pass

    def apply_effect(self, player, other=None):
        # پخش صدای آیتم گلوله و افزایش تعداد گلوله‌های بازیکن
        self.ammo_sound.play()
        player.bullets_left += 3