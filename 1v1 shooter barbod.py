import pygame
import sys
from btn import Btn
import random
from player import Player
from NormalTarget import NormalTarget
from FreezeItem import FreezeItem
from TimeItem import TimeItem
from AmmoItem import AmmoItem
#a test for syncing!

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Game:
    def __init__(self):
        pygame.init()
        self.game_display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Wand Warfare")
        self.state = 1
        self.btns = self.main_menu()
        self.click = False
        self.targets = []
        self.clock = pygame.time.Clock()
        self.player1_name = ""
        self.player2_name = ""
        self.active_input = 1
        self.font = pygame.font.Font("fonts/VT323-Regular.ttf", 48)
        self.small_font = pygame.font.Font("fonts/VT323-Regular.ttf", 32)
        self.title_font = pygame.font.Font("fonts/VT323-Regular.ttf", 85)
        self.last_tick = 0
        self.menu_background = pygame.image.load("graphics/menu_bg.png").convert()
        self.menu_background = pygame.transform.scale(self.menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.game_background = pygame.image.load("graphics/game_bg.png").convert()
        self.game_background = pygame.transform.scale(self.game_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound("sfx/click.mp3")
        self.game_over_sound = pygame.mixer.Sound("sfx/Game_over.mp3")
        self.miss_sound = pygame.mixer.Sound("sfx/Missed_shot.mp3")
        self.empty_sound = pygame.mixer.Sound("sfx/No_ammo.mp3")
        self.countdown_sound = pygame.mixer.Sound("sfx/Timeout.mp3")
        self.countdown_channel = pygame.mixer.Channel(5)
        pygame.mixer.music.load("sfx/Main_theme.mp3")
        pygame.mixer.music.set_volume(0.8)
        self.click_sound.set_volume(1.0)
        pygame.mixer.music.play(-1)
        self.run()

    def main_menu(self):
        btns = [
            Btn("New Game", "new_game", (280, 220), (240, 60), (229, 182, 117), (15, 15, 20), (28, 48, 89)),
            Btn("Description", "description", (280, 320), (240, 60), (229, 182, 117), (15, 15, 20), (28, 48, 89)),
            Btn("Scoreboard", "scoreboard", (280, 420), (240, 60), (229, 182, 117), (15, 15, 20), (28, 48, 89)),
            Btn("Exit", "exit", (280, 520), (240, 60), (229, 182, 117), (15, 15, 20), (28, 48, 89))
        ]
        return btns
    def events_handler(self):
        self.click = False
        self.shoot1 = False
        self.shoot2 = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                self.click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.shoot1 = True
                if event.key == pygame.K_KP_ENTER:
                    self.shoot2 = True
                if event.key == pygame.K_r and self.state == 4:
                    self.restart_game()
                if event.key == pygame.K_ESCAPE and self.state == 4:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_ESCAPE and self.state == 5:
                    self.state = 1
                

                
    
    
    def name_input_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.active_input == 1:
                    if event.key == pygame.K_BACKSPACE:
                        self.player1_name = self.player1_name[:-1]
                    elif event.key == pygame.K_RETURN and self.player1_name.strip():
                        self.active_input = 2  
                    else:
                        self.player1_name += event.unicode

                elif self.active_input == 2:
                    if event.key == pygame.K_BACKSPACE:
                        self.player2_name = self.player2_name[:-1]
                    elif event.key == pygame.K_RETURN and self.player2_name.strip():
        
                        self.player1 = Player(self.player1_name, (190, 151, 223), "graphics/Purplecursor.jpg")
                        self.player2 = Player(self.player2_name, (229, 182, 117), "graphics/yellowcursor.jpg")
                        pygame.mixer.music.fadeout(500)
                        self.setup_game()
                        self.state = 3
                    else:
                        self.player2_name += event.unicode

    
        self.game_display.blit(self.menu_background, (0, 0))

        title_text = self.font.render("Enter Player Names", True, (190, 151, 223))
        title_border = self.font.render("Enter Player Names", True, (15, 15, 20))
        
        center_x = SCREEN_WIDTH // 2
        center_y = 80

        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                if dx != 0 or dy != 0:
                    b_rect = title_border.get_rect(center=(center_x + dx, center_y + dy))
                    self.game_display.blit(title_border, b_rect)

        title_rect = title_text.get_rect(center=(center_x, center_y))
        self.game_display.blit(title_text, title_rect)

 
        p1_box_border_color = (73, 95, 142) if self.active_input == 1 else (52, 52, 64)     
    
        p1_rect = pygame.Rect(80, 190, 640, 110)
        pygame.draw.rect(self.game_display, (15, 15, 20), p1_rect, border_radius=10)     
        pygame.draw.rect(self.game_display, p1_box_border_color, p1_rect, width=3, border_radius=10)     
        
        p1_label = self.small_font.render("Player 1 (WASD):", True, (190, 151, 223))     
        p1_text = self.font.render(self.player1_name + ("|" if self.active_input == 1 else ""), True, (255, 255, 255))     
        self.game_display.blit(p1_label, (100, 200))     
        self.game_display.blit(p1_text, (100, 240))


        p2_box_border_color = (229, 182, 117) if self.active_input == 2 else (52, 52, 64)     
        
        p2_rect = pygame.Rect(80, 330, 640, 110)
        pygame.draw.rect(self.game_display, (15, 15, 20), p2_rect, border_radius=10)     
        pygame.draw.rect(self.game_display, p2_box_border_color, p2_rect, width=3, border_radius=10)     
        
        p2_label = self.small_font.render("Player 2 (Arrow Keys):", True, (229, 182, 117))     
        p2_text = self.font.render(self.player2_name + ("|" if self.active_input == 2 else ""), True, (255, 255, 255))     
        self.game_display.blit(p2_label, (100, 340))
        self.game_display.blit(p2_text, (100, 380))

        hint_rect = pygame.Rect(160, 500, 480, 45)
        pygame.draw.rect(self.game_display, (20, 20, 25), hint_rect, border_radius=6)
        hint = self.small_font.render("Press ENTER to confirm each name", True, (200, 200, 200)) 
        hint_text_rect = hint.get_rect(center=hint_rect.center)
        self.game_display.blit(hint, hint_text_rect)

        
    def menu_loop(self, mouse_pos):
        for btn in self.btns:
                btn.draw(self.game_display, mouse_pos)

                if btn.is_clicked(mouse_pos, self.click):
                        self.click_sound.play()

                        if btn.action == "new_game":
                            self.state = 2

                        elif btn.action == "description":
                            self.state = 5

                        elif btn.action == "exit":
                            pygame.quit()
                            sys.exit()

    
    
    def game_loop(self):
        self.game_display.blit(self.game_background, (0, 0))
        self.player1.draw(self.game_display)
        self.player2.draw(self.game_display)

        for target in self.targets:
            target.update()
            target.draw(self.game_display)
            
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy -= self.player1.cursor.speed
        if keys[pygame.K_a]:
            dx -= self.player1.cursor.speed
        if keys[pygame.K_s]:
            dy += self.player1.cursor.speed
        if keys[pygame.K_d]:
            dx += self.player1.cursor.speed
        self.player1.move_cursor(dx, dy, SCREEN_WIDTH, SCREEN_HEIGHT)


        dx_2 = 0
        dy_2 = 0
        if keys[pygame.K_UP]:
            dy_2 -= self.player2.cursor.speed
        if keys[pygame.K_LEFT]:
            dx_2 -= self.player2.cursor.speed
        if keys[pygame.K_DOWN]:
            dy_2 += self.player2.cursor.speed
        if keys[pygame.K_RIGHT]:
            dx_2 += self.player2.cursor.speed
        self.player2.move_cursor(dx_2, dy_2, SCREEN_WIDTH, SCREEN_HEIGHT)


        shot1 = None
        shot2 = None
        if self.shoot1:
            if self.player1.bullets_left > 0:
                shot1 = self.player1.shoot()
            else:
                self.empty_sound.play()

        if self.shoot2:
            if self.player2.bullets_left > 0:
                shot2 = self.player2.shoot()
            else:
                self.empty_sound.play()

        self.check_collision(self.player1, shot1)
        self.check_collision(self.player2, shot2)
        self.player1.cursor.update()
        self.player2.cursor.update()
        self.update_timers()
        self.draw_hud()
        
    def check_collision(self, player, shot):
        if shot is None:
            return

        hit_detected = False
        if player == self.player1:
            other = self.player2
        if player == self.player2:
            other = self.player1 
        
        for target in self.targets[:]:
            if target.rect.collidepoint(shot):
                target.apply_effect(player, other)
                self.targets.remove(target)
                self.spawn_item()
                hit_detected = True 
                break 

        if not hit_detected:
            self.miss_sound.play()
            player.miss()

    def spawn_item(self):
        target_width, target_height = 80, 80
        
        while True:
            x_target = random.randint(130, 750)
            y_target = random.randint(125, 550)
            
            temp_rect = pygame.Rect(x_target, y_target, target_width, target_height)
            
            overlap = False
            for existing_target in self.targets:
                if temp_rect.colliderect(existing_target.rect):
                    overlap = True
                    break
            
            if not overlap:
                break

        chance = random.randint(1, 100)
        if chance <= 60:
            item = NormalTarget((x_target, y_target), (target_width, target_height), (220, 90, 48))
        elif chance <= 75:
            item = AmmoItem((x_target, y_target), (target_width, target_height), (90, 200, 90))
        elif chance <= 90:
            item = TimeItem((x_target, y_target), (target_width, target_height), (90, 170, 255))
        else:
            item = FreezeItem((x_target, y_target), (target_width, target_height), (200, 90, 255))
            
        self.targets.append(item)
    
    def setup_game(self):
        self.last_tick = pygame.time.get_ticks() ### ai check
        self.targets = []
        for _ in range(5):
            self.spawn_item()
    
    def update_timers(self):
        now = pygame.time.get_ticks()
        if now - self.last_tick >= 1000:  # checks if 1 second has passed or not
            self.last_tick = now
            if self.player1.time_left > 0:
                self.player1.time_left -= 1
            if self.player2.time_left > 0:
                self.player2.time_left -= 1

        p1_danger = 0 < self.player1.time_left <= 5
        p2_danger = 0 < self.player2.time_left <= 5

        if p1_danger or p2_danger:
            if not self.countdown_channel.get_busy():
                self.countdown_channel.play(self.countdown_sound, loops=-1)
        else:
            if self.countdown_channel.get_busy():
                self.countdown_channel.stop()
        time_out = self.player1.time_left <= 0 and self.player2.time_left <= 0
        ammo_out = self.player1.bullets_left <= 0 and self.player2.bullets_left <= 0

        if time_out or ammo_out:
            self.countdown_channel.stop()
            self.game_over_sound.play()
            self.state = 4  
            self.show_results()
    

    def show_results(self):
        # ۱. رسم پس‌زمینه منو
        self.game_display.blit(self.menu_background, (0, 0))
        
        center_x = SCREEN_WIDTH // 2
        bg_color = (15, 15, 20)  
        border_color = (52, 52, 64)  
        padding = 15  

    
        title_text = self.title_font.render("Game Over", True, (190, 151, 223))
        title_rect = title_text.get_rect(center=(center_x, 80))
       
        title_bg_rect = title_rect.inflate(padding * 2, padding)
        pygame.draw.rect(self.game_display, bg_color, title_bg_rect, border_radius=8)
        pygame.draw.rect(self.game_display, border_color, title_bg_rect, width=2, border_radius=8)
        self.game_display.blit(title_text, title_rect)

        if self.player1.score > self.player2.score:
            winner_text = f"{self.player1.name} WINS"  
            winner_color = (229, 182, 117)  
        elif self.player2.score > self.player1.score: 
            winner_text = f"{self.player2.name} WINS"  
            winner_color = (190, 151, 223)  
        else:
            winner_text = "DRAW!"  
            winner_color = (54, 230, 111)
        
        winner = self.font.render(winner_text, True, winner_color)  
        winner_rect = winner.get_rect(center=(center_x, 185))
        winner_bg_rect = winner_rect.inflate(padding * 2, padding)
        pygame.draw.rect(self.game_display, bg_color, winner_bg_rect, border_radius=8)
        pygame.draw.rect(self.game_display, border_color, winner_bg_rect, width=2, border_radius=8)
        self.game_display.blit(winner, winner_rect)  

        p1_string = f"{self.player1.name} : {self.player1.score}pts | bullets : {self.player1.bullets_left} | time : {self.player1.time_left}"
        p1_score = self.small_font.render(p1_string, True, (54, 230, 111))
        p1_rect = p1_score.get_rect(center=(center_x, 290))

        p1_bg_rect = p1_rect.inflate(padding * 2, padding)
        pygame.draw.rect(self.game_display, bg_color, p1_bg_rect, border_radius=8)
        pygame.draw.rect(self.game_display, border_color, p1_bg_rect, width=2, border_radius=8)
        self.game_display.blit(p1_score, p1_rect)  
        
     
        p2_string = f"{self.player2.name} : {self.player2.score}pts | bullets : {self.player2.bullets_left} | time : {self.player2.time_left}"
        p2_score = self.small_font.render(p2_string, True, (190, 151, 223))
        p2_rect = p2_score.get_rect(center=(center_x, 360))
        
        p2_bg_rect = p2_rect.inflate(padding * 2, padding)
        pygame.draw.rect(self.game_display, bg_color, p2_bg_rect, border_radius=8)
        pygame.draw.rect(self.game_display, border_color, p2_bg_rect, width=2, border_radius=8)
        self.game_display.blit(p2_score, p2_rect)  
        
        play_again = self.small_font.render("Press R to Play Again  |  Press ESC to Exit", True, (255, 255, 255))  
        play_again_rect = play_again.get_rect(center=(center_x, 510))
        hint_bg_rect = play_again_rect.inflate(padding * 2, padding)
        pygame.draw.rect(self.game_display, bg_color, hint_bg_rect, border_radius=8)
        pygame.draw.rect(self.game_display, border_color, hint_bg_rect, width=2, border_radius=8)
        self.game_display.blit(play_again, play_again_rect)
    
    def restart_game(self):
        self.countdown_channel.stop()
        self.player1_name = "" 
        self.player2_name = ""
        self.active_input = 1 
        self.targets = []
        pygame.mixer.music.play(-1)
        self.state = 2 
    
    def draw_hud(self):
        p1_name = self.small_font.render(self.player1.name, True, (223, 151, 190))
        p1_bullets = self.small_font.render(f"Bullets: {self.player1.bullets_left}", True, (229, 182, 117))
        p1_time = self.small_font.render(f"Time: {self.player1.time_left}s", True, (229, 182, 117))
        p1_score = self.small_font.render(f"Score: {self.player1.score}", True, (229, 182, 117))

        self.game_display.blit(p1_name, (10,10))   
        self.game_display.blit(p1_bullets, (10,40))
        self.game_display.blit(p1_time, (10,65))
        self.game_display.blit(p1_score, (10,90))


        p2_name = self.small_font.render(self.player2.name, True, (117, 182, 229))
        p2_bullets = self.small_font.render(f"Bullets: {self.player2.bullets_left}", True, (229, 182, 117))
        p2_time = self.small_font.render(f"Time: {self.player2.time_left}s", True, (229, 182, 117))
        p2_score = self.small_font.render(f"Score: {self.player2.score}", True, (229, 182, 117))

        self.game_display.blit(p2_name, (650,10))   
        self.game_display.blit(p2_bullets, (650,40))
        self.game_display.blit(p2_time, (650,65))
        self.game_display.blit(p2_score, (650,90))
    
    def description_loop(self):
        self.game_display.blit(self.menu_background, (0, 0))
    
        center_x = SCREEN_WIDTH // 2
        bg_color = (15, 15, 20)
        border_color = (52, 52, 64)
        padding = 15

        # عنوان
        title = self.font.render("How To Play", True, (54, 230, 111))
        title_rect = title.get_rect(center=(center_x, 60))
        title_bg = title_rect.inflate(padding * 2, padding)
        pygame.draw.rect(self.game_display, bg_color, title_bg, border_radius=8)
        pygame.draw.rect(self.game_display, border_color, title_bg, width=2, border_radius=8)
        self.game_display.blit(title, title_rect)

        lines = [
            ("Welcome to Wand Warfare, Wizard!", (54, 230, 111)),
            ("Hunt down ghosts, score points", (255, 255, 255)),
            ("prove who the ultimate mage is!", (255, 255, 255)),
            ("Player 1(Purple Sorcerer): WASD to move|  SPACE to cast", (190, 151, 223)),
            ("Player 2(Golden Mage): Arrow Keys to move|  KP Enter to cast", (229, 182, 117)),
            ("Ghosts: Main targets  >>  +3 Points", (255, 255, 255)),
            ("Freeze Orb: Slows your rival for 3 seconds", (200, 90, 255)),
            ("Hourglass: +6 Seconds to your time", (90, 170, 255)),
            ("Mana Potion: +3 Spells (Bullets)", (90, 200, 90)),
            ("Duel ends when time or spells run out. Highest score wins!", (200, 200, 200)),
        ]
        

        y = 120 
        for text, color in lines:
            surface = self.small_font.render(text, True, color)
            rect = surface.get_rect(center=(center_x, y))
            bg = rect.inflate(padding * 2, padding)
            pygame.draw.rect(self.game_display, bg_color, bg, border_radius=8)
            pygame.draw.rect(self.game_display, border_color, bg, width=2, border_radius=8)
            self.game_display.blit(surface, rect)
            y += 50


        back = self.small_font.render("Press ESC to go back", True, (150, 150, 150))
        back_rect = back.get_rect(center=(60, 30))
        self.game_display.blit(back, back_rect)
    
    
    
    
    
    def run(self):
        running = True

        while running:
                
            if self.state == 1:# be in the main menu
                    self.events_handler()
                    mouse_pos = pygame.mouse.get_pos()
                    self.game_display.blit(self.menu_background, (0, 0))
                    title_text = self.title_font.render("Wand Warfare", True, (54, 230, 111))
                    border_text = self.title_font.render("Wand Warfare", True, (15, 15, 20))
                    
                    center_x = SCREEN_WIDTH // 2
                    center_y = 120
                    
                    for dx in [-2, 0, 2]:
                        for dy in [-2, 0, 2]:
                            if dx != 0 or dy != 0:
                                b_rect = border_text.get_rect(center=(center_x + dx, center_y + dy))
                                self.game_display.blit(border_text, b_rect)
                    
                    title_rect = title_text.get_rect(center=(center_x, center_y))
                    self.game_display.blit(title_text, title_rect)
                    
                    self.menu_loop(mouse_pos)
            elif self.state == 2:#get the player names
                    self.name_input_loop()
                
            elif self.state == 3: # play the game
                    self.events_handler()
                    self.game_loop()
            elif self.state == 4:   # showing results
                self.events_handler()
                self.show_results()
            elif self.state == 5: #description
                self.events_handler()
                self.description_loop()
        


            

                

            pygame.display.update()
            self.clock.tick(60)

Game()