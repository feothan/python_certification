import pygame
import json
import sys
import time

# Load JSON
with open('bookmarks.json', 'r') as f:
    story = json.load(f)

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Adventure 1")
clock = pygame.time.Clock()

# Fonts
big_font = pygame.font.SysFont("georgia", 48)
med_font = pygame.font.SysFont("georgia", 32)
small_font = pygame.font.SysFont("georgia", 20)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
DARK_BLUE = (60, 100, 140)
GRAY = (230, 230, 230)

# Data root
root_title = next(iter(story))
current_node = story[root_title]

def draw_text_centered(text, y, font, color=BLACK):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(WIDTH // 2, y))
    screen.blit(rendered, rect)

def wait_for_click():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
        clock.tick(30)

def show_title_screen():
    screen.fill(WHITE)
    draw_text_centered("Welcome to", HEIGHT // 2 - 100, med_font)
    draw_text_centered(root_title, HEIGHT // 2 - 40, big_font)
    pygame.display.flip()
    time.sleep(1.25)  # Half-second pause before showing the Zelia line

    # Now draw the Zelia line and re-flip
    draw_text_centered("Zelia's extracted shortcut data successfully loaded!", HEIGHT // 2 + 40, small_font)
    pygame.display.flip()
    time.sleep(0.7)  # Slight dramatic delay before interaction
    wait_for_click()

def show_end_screen(text):
    screen.fill(WHITE)
    draw_text_centered(text, HEIGHT//2 - 40, med_font)
    draw_text_centered("The End", HEIGHT//2 + 30, med_font)
    pygame.display.flip()
    wait_for_click()

def show_choices(choices):
    screen.fill(WHITE)
    button_rects = []
    spacing = 80
    start_y = HEIGHT // 2 - (spacing * len(choices)) // 2

    for i, choice in enumerate(choices):
        rect = pygame.Rect(WIDTH // 2 - 250, start_y + i * spacing, 500, 50)
        pygame.draw.rect(screen, BLUE, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        text = med_font.render(choice, True, WHITE)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
        button_rects.append((rect, choice))

    pygame.display.flip()
    return button_rects

def get_clicked_choice(button_rects):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, choice in button_rects:
                    if rect.collidepoint(event.pos):
                        return choice
        clock.tick(30)

# --- RUN GAME ---
show_title_screen()

while True:
    # Special ending case: {"some message": {}}
    if isinstance(current_node, dict) and len(current_node) == 1:
        only_key = next(iter(current_node))
        if current_node[only_key] == {}:
            show_end_screen(only_key)
            break

    # Final string node
    if not isinstance(current_node, dict):
        show_end_screen(current_node)
        break

    choices = list(current_node)

    if len(choices) == 1:
        # Single option: just display and wait
        screen.fill(WHITE)
        draw_text_centered(choices[0], HEIGHT // 2, med_font)
        pygame.display.flip()
        wait_for_click()
        current_node = current_node[choices[0]]
    else:
        # Multiple choices
        buttons = show_choices(choices)
        selected = get_clicked_choice(buttons)
        current_node = current_node[selected]

pygame.quit()
