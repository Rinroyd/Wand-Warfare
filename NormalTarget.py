import pygame
from target import Target

# هدف اصلی بازی (شبح): با انیمیشن پرواز نمایش داده می‌شود و با زدنش امتیاز کسب می‌شود
class NormalTarget(Target):
    def __init__(self, location, size, color):
        super().__init__(location, size, color)

        # بارگذاری فریم‌های انیمیشن پرواز شبح از سه تصویر جداگانه
        self.frames = []
        for path in ["graphics/Fly1.jpg", "graphics/Fly2.jpg", "graphics/Fly3.jpg"]:
            img = pygame.image.load(path).convert()
            img.set_colorkey((0, 0, 0))  # شفاف کردن پس‌زمینه‌ی مشکی هر فریم
            img = pygame.transform.scale(img, size)
            self.frames.append(img)
            
        self.current_frame = 0.0  # اندیس فریم فعلی (اعشاری برای کنترل سرعت انیمیشن)
        self.animation_speed = 0.15  # سرعت پیشرفت انیمیشن در هر فریم بازی
        self.image = self.frames[0]  # تصویر شروع، اولین فریم

        # بارگذاری صدای برخورد به شبح
        pygame.mixer.init()
        self.ghost_sound = pygame.mixer.Sound("sfx/Ghost.mp3")

    def draw(self, surface):
        # رسم فریم فعلی انیمیشن روی صفحه
        surface.blit(self.image, self.rect)

    def update(self):
        # پیشروی انیمیشن؛ وقتی از آخرین فریم رد شد، دوباره از اول شروع می‌شود (حلقه)
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0.0
        self.image = self.frames[int(self.current_frame)]

    def apply_effect(self, player, other=None):
        # پخش صدای برخورد و محاسبه‌ی امتیاز بر اساس فاصله‌ی نقطه‌ی شلیک تا مرکز هدف
        self.ghost_sound.play()
        player.calculate_score(player.cursor.rect.center, self.rect.center)