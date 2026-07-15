import pygame
from btn import Btn
from db_manager import LeaderboardDB

# پالت رنگ‌های مورد استفاده در صفحه‌ی جدول امتیازات
BG_COLOR = (18, 18, 26)
PANEL_COLOR = (28, 28, 38)
PANEL_BORDER = (60, 150, 220)
HEADER_COLOR = (90, 170, 255)
TEXT_COLOR = (230, 230, 235)
MUTED_TEXT = (140, 140, 150)
ROW_ALT_COLOR = (24, 24, 34)
GOLD = (255, 215, 0)
SILVER = (200, 205, 215)
BRONZE = (205, 140, 80)
CURRENT_PLAYER_COLOR = (60, 95, 140)


# کلاس نمایش صفحه‌ی جدول امتیازات (Leaderboard) شامل جدول، جست‌وجو و دکمه‌های بازگشت/رفرش
class Leaderboard:

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.db = LeaderboardDB()  # اتصال به دیتابیس امتیازات

        # فونت‌های مورد استفاده در بخش‌های مختلف صفحه
        self.title_font = pygame.font.Font(None, 52)
        self.header_font = pygame.font.Font(None, 26)
        self.row_font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)

        # ساخت دکمه‌های بازگشت به منو و رفرش کردن لیست امتیازات
        btn_y = screen_height - 60
        self.back_btn = Btn("Back", "back", (20, btn_y), (120, 44),
                             (255, 255, 255), (40, 40, 40), (90, 170, 255))
        self.refresh_btn = Btn("Refresh", "refresh", (screen_width - 150, btn_y), (130, 44),
                                (255, 255, 255), (40, 40, 40), (90, 170, 255))

        # وضعیت باکس جست‌وجوی بازیکن
        self.search_active = False
        self.search_text = ""
        self.search_box_rect = pygame.Rect(screen_width - 260, 22, 240, 32)

        # تعریف ستون‌های جدول به همراه عرض نسبی هرکدام (به صورت درصدی از عرض کل جدول)
        self.columns = [
            ("#", 0.08),
            ("Username", 0.32),
            ("Score", 0.18),
            ("Level", 0.14),
            ("Date", 0.28),
        ]

        self.entries = []
        self.refresh()  # بارگذاری اولیه‌ی لیست امتیازات از دیتابیس

    def refresh(self):
        # اگر متن جست‌وجو خالی نباشد، نتایج بر اساس جست‌وجوی نام بازیکن گرفته می‌شود
        # در غیر این صورت، لیست کلی ۱۰ امتیاز برتر نمایش داده می‌شود
        if self.search_text.strip():
            self.entries = self.db.search_player(self.search_text.strip(), limit=10)
        else:
            self.entries = self.db.get_top_scores(10)

    def handle_event(self, event):
        # فعال/غیرفعال کردن باکس جست‌وجو بسته به اینکه کلیک داخل آن انجام شده یا نه
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.search_active = self.search_box_rect.collidepoint(event.pos)

        elif event.type == pygame.KEYDOWN and self.search_active:
            # مدیریت تایپ در باکس جست‌وجو
            if event.key == pygame.K_BACKSPACE:
                self.search_text = self.search_text[:-1]
                self.refresh()
            elif event.key == pygame.K_RETURN:
                self.refresh()
            elif event.key == pygame.K_ESCAPE:
                # پاک کردن جست‌وجو و خروج از حالت فعال با ESC
                self.search_text = ""
                self.search_active = False
                self.refresh()
            elif event.unicode and event.unicode.isprintable():
                self.search_text += event.unicode
                self.refresh()

    def handle_click(self, mouse_pos, clicked):
        # بررسی کلیک روی دکمه‌ی بازگشت؛ در صورت کلیک، رشته‌ی "back" برگردانده می‌شود تا Game آن را مدیریت کند
        if self.back_btn.is_clicked(mouse_pos, clicked):
            return "back"
        # بررسی کلیک روی دکمه‌ی رفرش؛ در صورت کلیک، لیست امتیازات دوباره از دیتابیس خوانده می‌شود
        if self.refresh_btn.is_clicked(mouse_pos, clicked):
            self.refresh()
        return None

    def _table_geometry(self):
        # محاسبه‌ی ابعاد و موقعیت جدول امتیازات بر اساس عرض صفحه‌نمایش
        table_width = int(self.screen_width * 0.86)
        table_x = (self.screen_width - table_width) // 2
        table_y = 116
        header_height = 38
        row_height = 32
        return table_x, table_y, table_width, header_height, row_height

    def _draw_glow_panel(self, surface, rect, color, radius=14, layers=4):
        # رسم یک پنل با افکت درخشش (glow) دور آن با چند لایه‌ی نیمه‌شفاف که به تدریج بزرگ‌تر می‌شوند
        pad = layers * 4
        glow_surf = pygame.Surface((rect.width + pad * 2, rect.height + pad * 2), pygame.SRCALPHA)
        for i in range(layers, 0, -1):
            alpha = int(14 * (layers - i + 1) / layers) + 4
            grown = pygame.Rect(pad - i * 3, pad - i * 3,
                                 rect.width + i * 6, rect.height + i * 6)
            pygame.draw.rect(glow_surf, (*color, alpha), grown, border_radius=radius + i)
        surface.blit(glow_surf, (rect.x - pad, rect.y - pad))
        # رسم خود پنل اصلی روی لایه‌ی گلو
        pygame.draw.rect(surface, PANEL_COLOR, rect, border_radius=radius)
        pygame.draw.rect(surface, color, rect, width=2, border_radius=radius)

    def _draw_rounded_shadow_rect(self, surface, rect, color, radius=8):
        # رسم یک مستطیل گردشده با یک سایه‌ی ملایم زیر آن (برای هایلایت کردن ردیف بازیکن فعلی)
        shadow_rect = rect.move(0, 2)
        shadow_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, (0, 0, 0, 60), shadow_surf.get_rect(), border_radius=radius)
        surface.blit(shadow_surf, shadow_rect.topleft)
        pygame.draw.rect(surface, color, rect, border_radius=radius)

    def draw(self, surface, mouse_pos, current_players=None):
        # رسم کامل صفحه‌ی جدول امتیازات: عنوان، جدول، هدر ستون‌ها، ردیف‌ها، باکس جست‌وجو و دکمه‌ها
        current_players = set(current_players or [])
        surface.fill(BG_COLOR)

        # عنوان بالای صفحه
        title = self.title_font.render("LEADERBOARD", True, HEADER_COLOR)
        surface.blit(title, title.get_rect(center=(self.screen_width // 2, 48)))

        # محاسبه‌ی هندسه‌ی جدول و رسم پنل اصلی آن با افکت گلو
        table_x, table_y, table_width, header_height, row_height = self._table_geometry()
        table_height = header_height + row_height * 10 + 12
        table_rect = pygame.Rect(table_x, table_y, table_width, table_height)
        self._draw_glow_panel(surface, table_rect, PANEL_BORDER)

        # محاسبه‌ی عرض واقعی هر ستون بر اساس نسبت تعریف‌شده
        col_widths = [int(table_width * ratio) for _, ratio in self.columns]

        # رسم عنوان ستون‌ها (هدر جدول)
        x = table_x
        for (label, _), w in zip(self.columns, col_widths):
            header_surf = self.header_font.render(label, True, HEADER_COLOR)
            surface.blit(header_surf, (x + 14, table_y + 9))
            x += w
        # خط جداکننده‌ی زیر هدر جدول
        pygame.draw.line(surface, PANEL_BORDER,
                          (table_x + 10, table_y + header_height),
                          (table_x + table_width - 10, table_y + header_height), 1)

        # رنگ و برچسب مخصوص سه رتبه‌ی برتر (طلا، نقره، برنز)
        rank_colors = {1: GOLD, 2: SILVER, 3: BRONZE}
        rank_labels = {1: "1st", 2: "2nd", 3: "3rd"}

        row_y = table_y + header_height + 6
        if not self.entries:
            # پیام مناسب زمانی که هیچ امتیازی هنوز ثبت نشده
            empty = self.row_font.render("No scores yet — go play a match!", True, MUTED_TEXT)
            surface.blit(empty, (table_x + 20, row_y + 10))
        else:
            # رسم تک‌تک ردیف‌های جدول امتیازات
            for idx, (username, score, level, date_achieved) in enumerate(self.entries):
                rank = idx + 1
                row_rect = pygame.Rect(table_x + 6, row_y, table_width - 12, row_height - 4)

                # اگر این ردیف مربوط به یکی از بازیکن‌های فعلی بازی باشد، با رنگ خاص هایلایت می‌شود
                if username in current_players:
                    self._draw_rounded_shadow_rect(surface, row_rect, CURRENT_PLAYER_COLOR, radius=8)
                elif idx % 2 == 1:
                    # ردیف‌های زوج با رنگ متفاوت (افکت خط‌خطی/striped) رسم می‌شوند
                    pygame.draw.rect(surface, ROW_ALT_COLOR, row_rect, border_radius=8)

                text_color = rank_colors.get(rank, TEXT_COLOR)
                rank_display = rank_labels.get(rank, str(rank))

                # رسم مقادیر هر ستون برای این ردیف (رتبه، نام، امتیاز، سطح، تاریخ)
                values = [rank_display, username, f"{score:,}", str(level), date_achieved]
                x = table_x
                for val, w in zip(values, col_widths):
                    val_surf = self.row_font.render(val, True, text_color)
                    surface.blit(val_surf, (x + 14, row_y + 4))
                    x += w

                row_y += row_height

        # رسم باکس جست‌وجو با تغییر رنگ حاشیه بسته به فعال بودن آن
        pygame.draw.rect(surface, PANEL_COLOR, self.search_box_rect, border_radius=8)
        border_col = HEADER_COLOR if self.search_active else (70, 70, 82)
        pygame.draw.rect(surface, border_col, self.search_box_rect, width=2, border_radius=8)
        # نمایش متن تایپ‌شده یا متن راهنمای پیش‌فرض ("Search player...") در صورت خالی بودن
        display_text = self.search_text if (self.search_text or self.search_active) else "Search player..."
        text_color = TEXT_COLOR if self.search_text else MUTED_TEXT
        search_surf = self.small_font.render(display_text, True, text_color)
        surface.blit(search_surf, (self.search_box_rect.x + 10, self.search_box_rect.y + 8))

        # راهنمای کوچک زیر باکس جست‌وجو
        hint = self.small_font.render("Click the box and type to search a player", True, MUTED_TEXT)
        surface.blit(hint, (self.search_box_rect.x - 20,
                             self.search_box_rect.y + self.search_box_rect.height + 6))

        # رسم دکمه‌های بازگشت و رفرش
        self.back_btn.draw(surface, mouse_pos)
        self.refresh_btn.draw(surface, mouse_pos)