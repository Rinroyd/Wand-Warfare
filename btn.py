import pygame


class Btn:
    def __init__(self, text, action, location, size, text_color, back_color, for_color):
        self.action = action

        self.font = pygame.font.Font("fonts/VT323-Regular.ttf", 50)

        self._text = text
        self._location = location
        self._width, self._height = size
        self.text_color = (229, 182, 117)
        self.b_color = (15, 15, 20)
        self.f_color = (28, 48,89)
        self.hover_text_color = (190, 151, 223)
        self.hover_back_color = (15, 15, 20)
        self.hover_for_color = (73, 95, 142)

        self.text = self.font.render(self._text, True, self.text_color)

        self.rect1 = pygame.Rect(*location, *size)
        self.rect2 = pygame.Rect(location[0] + 4, location[1] + 4, size[0] - 8, size[1] - 8)

    def normal(self, surface):
        self.text = self.font.render(self._text, True, self.text_color)

        pygame.draw.rect(surface, self.b_color, self.rect1, border_radius=17)
        pygame.draw.rect(surface, self.f_color, self.rect2, border_radius=17)

        text_rect = self.text.get_rect(center=self.rect2.center)
        surface.blit(self.text, text_rect)

    def hover(self, surface):
        self.text = self.font.render(self._text, True, self.hover_text_color)

        pygame.draw.rect(surface, self.hover_back_color, self.rect1, border_radius=17)
        pygame.draw.rect(surface, self.hover_for_color, self.rect2, border_radius=17)

        text_rect = self.text.get_rect(center=self.rect2.center)
        surface.blit(self.text, text_rect)

    def draw(self, surface, mouse_pos):
        if self.rect1.collidepoint(mouse_pos):
            self.hover(surface)
        else:
            self.normal(surface)

    def is_clicked(self, mouse_pos, click):
        return click and self.rect1.collidepoint(mouse_pos)