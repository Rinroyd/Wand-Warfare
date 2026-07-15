import pygame
from cursor import Cursor
import random
import math

# کلاس بازیکن که وضعیت کلی هر بازیکن (امتیاز، زمان، مهمات، نشانگر و ...) را نگه می‌دارد
class Player:
    def __init__(self, name, cursor_color, cursor_image_path):
        self.score = 0
        self.time_left = 25  # زمان اولیه‌ی هر بازیکن بر حسب ثانیه
        self.bullets_left = 15  # تعداد گلوله‌های اولیه
        self.applied_effects = []
        self.name = name
        self.last_shot_position = None
        self.combo = 0  # شمارنده‌ی زنجیره‌ی اصابت‌های پیاپی (کامبو) برای امتیاز اضافه
        # ساخت نشانگر بازیکن در یک موقعیت تصادفی روی صفحه
        self.cursor = Cursor((random.randint(0, 780), random.randint(0 ,580)), (40, 40), cursor_color, cursor_image_path)

    def move_cursor(self, dx, dy, screen_width, screen_height):
        # انتقال حرکت به نشانگر بازیکن
        self.cursor.move(dx, dy, screen_width, screen_height)

    def shoot(self):
        # اگر مهمات تمام شده باشد، شلیک انجام نمی‌شود
        if self.bullets_left == 0:
            return None
        
        if self.bullets_left > 0:
            self.bullets_left -= 1
            self.cursor.visible = True  # نمایش لحظه‌ای نشانگر هنگام شلیک
            self.cursor.visible_timer = 40  # مدت زمان نمایش نشانگر بعد از شلیک
        return self.cursor.rect.center  # موقعیت شلیک برای بررسی برخورد با اهداف
            
    def add_score(self, amount):
        # افزایش دستی امتیاز بازیکن
        self.score += amount
    
    def add_time(self, amount):
        # افزایش زمان باقی‌مانده‌ی بازیکن
        self.time_left += amount
    
    def add_bullets(self, amount):
        # افزایش تعداد مهمات بازیکن
        self.bullets_left += amount
    
    def draw(self, surface):
        # رسم نشانگر بازیکن روی صفحه
        self.cursor.draw(surface)
    
    def calculate_score(self, hit_pos, target_center):
        # محاسبه‌ی امتیاز بر اساس دقت شلیک (فاصله‌ی نقطه‌ی اصابت تا مرکز هدف)
        x_distance = hit_pos[0] - target_center[0]
        y_distance = hit_pos[1] - target_center[1]
        distance = math.sqrt(x_distance**2 + y_distance**2)
        
        # هرچه شلیک به مرکز هدف نزدیک‌تر باشد، امتیاز بیشتری تعلق می‌گیرد
        if distance > 30:     
            points = 1
        elif distance > 15:   
            points = 2
        else:              
            points = 3
            
        # پاداش کامبو: اگر این اصابت ادامه‌ی یک زنجیره‌ی موفق باشد، امتیاز اضافه تعلق می‌گیرد
        if self.combo >= 1:
            points += 2
            
        self.score += points
        self.combo += 1  # افزایش زنجیره‌ی کامبو بعد از هر اصابت موفق
        self.last_shot_position = hit_pos
        
        return points

    def miss(self):
        # با از دست دادن یک شلیک، زنجیره‌ی کامبو قطع می‌شود
        self.combo = 0