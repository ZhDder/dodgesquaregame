from collections import deque
import pygame

'''
Update 8/10/2025
- Included a new function which shows some debugging stats on screen while training.
'''

TEXT_COLOR = (255, 255, 255)
LINE_HEIGHT = 30
MAX_LINES = 15
MARGIN_LEFT = 1100
MARGIN_TOP = 20


class ScrollingText:
    '''
    Scrolling text class for debug purposes.
    '''
    def __init__(self, font, screen):
        self.screen = screen
        self.font = font
        self.max_lines = MAX_LINES
        self.text_lines = deque(maxlen=MAX_LINES)
        self.line_height = LINE_HEIGHT
        self.margin_left = MARGIN_LEFT
        self.margin_top = MARGIN_TOP

    def add_text(self, text):
        '''
        Add text to be shown on the scrolling text section.
        '''
        self.text_lines.append(text)

    def render(self):
        '''
        Render and show.
        '''
        for i, text in enumerate(self.text_lines):
            y_position = self.margin_top + (i * self.line_height)
            text_surface = self.font.render(text, True, TEXT_COLOR)
            self.screen.blit(text_surface, (self.margin_left, y_position))

def draw_debug_stats(screen, font, stats, screen_width, screen_height):
    '''
    Shows some stats about the training loop on the right side of the screen.
    '''
    start_y = screen_height - 120  # Starting y-position for the text
    for i, (key, value) in enumerate(stats.items()):
        text = f"{key}: {value}"
        text_surface = font.render(text, True, (255, 255, 255))
        
        # Position text at the bottom right
        text_rect = text_surface.get_rect(bottomright=(screen_width - 20, start_y + i * 25))

        screen.blit(text_surface, text_rect)