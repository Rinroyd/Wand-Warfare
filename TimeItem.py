import pygame
from target import Target

# آیتم زمان (ساعت شنی): وقتی بازیکن این هدف رو بزنه، مقداری زمان بهش اضافه می‌شه
class TimeItem(Target):
    def __init__(self, location, size, color):
        super().__init__(location, size, color)

        #  بارگذاری فریم‌های این آیتم از سه تصویر جداگانه برای ایجاد انیمیشن
        self.frames = []
        for path in ["graphics/Time1.jpg", "graphics/Time2.jpg", "graphics/Time3.jpg"]:
            img = pygame.image.load(path).convert()
            img.set_colorkey((0, 0, 0))  # شفاف کردن پس‌زمینه‌ی مشکی هر فریم
            img = pygame.transform.scale(img, size) 
            self.frames.append(img)
            
        self.current_frame = 0.0  # اندیس فریم فعلی (اعشاری برای کنترل سرعت انیمیشن)
        self.animation_speed = 0.12  # سرعت پیشرفت انیمیشن در هر فریم بازی
        self.image = self.frames[0]  # تصویر شروع، اولین فریم
        
        # بارگذاری صدای مخصوص برداشتن آیتم زمان
        pygame.mixer.init()
        self.timer_sound = pygame.mixer.Sound("sfx/Timer.mp3")
    
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
        # پخش صدای برداشتن آیتم و افزایش زمان باقی‌مانده‌ی بازیکنی که آن را زده
        self.timer_sound.play()
        player.time_left += 6