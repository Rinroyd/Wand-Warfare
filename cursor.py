import pygame
from game_object import GameObject

CURSOR_SPEED = 5   
# کلاس نشانگر بازیکن که با آن حرکت می‌کند و شلیک انجام می‌شود
class Cursor(GameObject):
    
    def __init__(self, location, size, color, image_path):
        super().__init__(location, size)
        self.color = color
        self.speed = CURSOR_SPEED   
        self.visible = False  # نشانگر معمولا مخفی است و فقط لحظه‌ی شلیک نمایش داده می‌شود
        self.freeze_timer = 0  # شمارنده‌ی باقی‌مانده از اثر فریز (کند شدن سرعت)
        self.visible_timer = 0  # شمارنده‌ی مدت زمانی که نشانگر باید نمایش داده شود
        self.normal_speed = CURSOR_SPEED  # سرعت عادی برای بازگشت بعد از پایان فریز
        
        # بارگذاری تصویر نشانگر و شفاف کردن پس‌زمینه‌ی مشکی آن
        self.image = pygame.image.load(image_path).convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, size)

    def move(self, dx, dy, screen_width, screen_height):
        # جابه‌جایی افقی نشانگر با محدود کردن آن به مرزهای صفحه
        self.rect.x += dx
        if self.rect.right >= screen_width:
            self.rect.right = screen_width
        elif self.rect.left <= 0:
            self.rect.left = 0
        
        # جابه‌جایی عمودی نشانگر با محدود کردن آن به مرزهای صفحه
        self.rect.y += dy
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
        

    def draw(self, surface):
        # اگر نشانگر در حالت نامرئی باشد، چیزی رسم نمی‌شود
        if self.visible == False:
            return 
        
        surface.blit(self.image, self.rect)

        
    def update(self):
        # کاهش تدریجی تایمر فریز؛ وقتی به صفر برسد سرعت به حالت عادی برمی‌گردد
        if self.freeze_timer > 0:
            self.freeze_timer -= 1
            if self.freeze_timer == 0:
                self.speed = self.normal_speed
        
        # کاهش تدریجی تایمر نمایش؛ وقتی به صفر برسد نشانگر دوباره مخفی می‌شود
        if self.visible_timer > 0:
            self.visible_timer -= 1
            if self.visible_timer == 0:
                self.visible = False