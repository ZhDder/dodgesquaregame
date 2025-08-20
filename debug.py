from collections import deque

TEXT_COLOR = (255, 255, 255)
LINE_HEIGHT = 30
MAX_LINES = 15
MARGIN_LEFT = 1100
MARGIN_TOP = 20


class ScrollingText:
    def __init__(self, font, screen):
        self.screen = screen
        self.font = font
        self.max_lines = MAX_LINES
        self.text_lines = deque(maxlen=MAX_LINES)
        self.line_height = LINE_HEIGHT
        self.margin_left = MARGIN_LEFT
        self.margin_top = MARGIN_TOP

    def add_text(self, text):
        self.text_lines.append(text)

    def render(self):
        for i, text in enumerate(self.text_lines):
            y_position = self.margin_top + (i * self.line_height)
            text_surface = self.font.render(text, True, TEXT_COLOR)
            self.screen.blit(text_surface, (self.margin_left, y_position))