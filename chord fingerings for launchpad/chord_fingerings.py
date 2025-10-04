import pygame

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1300, 1000
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3x3 Pad Chord Layout - Paginated")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)   # root
RED = (200, 0, 0)     # extension
GRAY = (220, 220, 220)

FONT = pygame.font.SysFont(None, 36)

# 3x3 pad layout
pad = [
    ['B', 'C', 'D'],
    ['F', 'G', 'A'],
    ['C', 'D', 'E']
]

# Chords: name -> notes
chords = {
    # Tier 1
    "C": ["C", "E", "G"],
    "Dm": ["D", "F", "A"],
    "Em": ["E", "G", "B"],
    "F": ["F", "A", "C"],
    "G": ["G", "B", "D"],
    "Am": ["A", "C", "E"],
    "Bdim": ["B", "D", "F"],

    # Tier 2
    "Cmaj7": ["C", "E", "G", "B"],
    "Dm7": ["D", "F", "A", "C"],
    "Em7": ["E", "G", "B", "D"],
    "Fmaj7": ["F", "A", "C", "E"],
    "G7": ["G", "B", "D"],
    "Am7": ["A", "C", "E", "G"],
    "Bm7b5": ["B", "D", "F"],

    # Tier 3
    "Csus2": ["C", "D", "G"],
    "Csus4": ["C", "F", "G"],
    "Cadd9": ["C", "D", "E", "G"],
    "Quartal": ["C", "F", "B"],
    "Cluster": ["C", "D", "E"]
}

# Grid settings
CELL_SIZE = 50
MARGIN_TOP = 60
MARGIN_LEFT = 20
CHORD_SPACING_X = 220
CHORD_SPACING_Y = 240
CHORDS_PER_ROW = 4
CHORDS_PER_PAGE = CHORDS_PER_ROW * CHORDS_PER_ROW  # 4x4

# Pagination
chord_list = list(chords.items())
total_pages = (len(chord_list) + CHORDS_PER_PAGE - 1) // CHORDS_PER_PAGE
current_page = 0

def get_note_color(note, chord_notes):
    root = chord_notes[0]
    triad = chord_notes[:3]
    if note == root:
        return GREEN
    elif note not in triad:
        return RED
    else:
        return BLACK

def draw_page(page_idx):
    SCREEN.fill(WHITE)
    start_idx = page_idx * CHORDS_PER_PAGE
    end_idx = start_idx + CHORDS_PER_PAGE
    chunk = chord_list[start_idx:end_idx]

    for idx, (name, notes) in enumerate(chunk):
        col = idx % CHORDS_PER_ROW
        row = idx // CHORDS_PER_ROW
        start_x = MARGIN_LEFT + col * CHORD_SPACING_X
        start_y = MARGIN_TOP + row * CHORD_SPACING_Y

        # Draw chord name
        label = FONT.render(f"{name} ({', '.join(notes)})", True, BLACK)
        SCREEN.blit(label, (start_x, start_y - 40))

        # Draw 3x3 pad
        for r in range(3):
            for c in range(3):
                note = pad[r][c]
                rect_x = start_x + c * CELL_SIZE
                rect_y = start_y + r * CELL_SIZE
                pygame.draw.rect(SCREEN, GRAY, (rect_x, rect_y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(SCREEN, BLACK, (rect_x, rect_y, CELL_SIZE, CELL_SIZE), 2)

                if note in notes:
                    color = get_note_color(note, notes)
                    note_text = FONT.render(note, True, color)
                    text_rect = note_text.get_rect(center=(rect_x + CELL_SIZE/2, rect_y + CELL_SIZE/2))
                    SCREEN.blit(note_text, text_rect)

    # Draw page number
    page_label = FONT.render(f"Page {page_idx + 1}/{total_pages}", True, BLACK)
    SCREEN.blit(page_label, (WIDTH - 200, HEIGHT - 40))

# Main loop
running = True
draw_page(current_page)
pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Next page
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                current_page += 1
                if current_page >= total_pages:
                    current_page = 0  # loop back to first page
                draw_page(current_page)
                pygame.display.flip()

pygame.quit()
