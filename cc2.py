import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
NUM_COLUMNS = 6
NUM_ROWS = 4
GUTTER_SIZE = 10
PANEL_MAX_WIDTH = 3
PANEL_MAX_HEIGHT = 2
BG_COLOR = (242, 242, 242)
PANEL_COLOR = (255, 255, 255)
PANEL_BORDER_COLOR = (0, 0, 0)

colWidth = (WIDTH - (NUM_COLUMNS + 1) * GUTTER_SIZE) / NUM_COLUMNS
rowHeight = (HEIGHT - (NUM_ROWS + 1) * GUTTER_SIZE) / NUM_ROWS
occupied = [[False for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Comic Layout")

def canPlacePanel(col, row, colSpan, rowSpan):
    if col + colSpan > NUM_COLUMNS or row + rowSpan > NUM_ROWS:
        return False

    for r in range(row, row + rowSpan):
        for c in range(col, col + colSpan):
            if occupied[r][c]:
                return False
    return True

def createPanel(col, row, colSpan, rowSpan):
    x = col * (colWidth + GUTTER_SIZE) + GUTTER_SIZE
    y = row * (rowHeight + GUTTER_SIZE) + GUTTER_SIZE
    w = colSpan * colWidth + (colSpan - 1) * GUTTER_SIZE
    h = rowSpan * rowHeight + (rowSpan - 1) * GUTTER_SIZE
    
    pygame.draw.rect(screen, PANEL_COLOR, (x, y, w, h))
    pygame.draw.rect(screen, PANEL_BORDER_COLOR, (x, y, w, h), 2)

    for r in range(row, row + rowSpan):
        for c in range(col, col + colSpan):
            occupied[r][c] = True

def generateLayout():
    for row in range(NUM_ROWS):
        for col in range(NUM_COLUMNS):
            if not occupied[row][col]:
                colSpan = min(1 + random.randint(0, PANEL_MAX_WIDTH), NUM_COLUMNS - col)
                rowSpan = min(1 + random.randint(0, PANEL_MAX_HEIGHT), NUM_ROWS - row)

                if canPlacePanel(col, row, colSpan, rowSpan):
                    createPanel(col, row, colSpan, rowSpan)

def fillGaps():
    for row in range(NUM_ROWS):
        for col in range(NUM_COLUMNS):
            if not occupied[row][col]:
                for cs in range(PANEL_MAX_WIDTH, 0, -1):
                    for rs in range(PANEL_MAX_HEIGHT, 0, -1):
                        if canPlacePanel(col, row, cs, rs):
                            createPanel(col, row, cs, rs)
                            break

# Main Loop
running = True
screen.fill(BG_COLOR)
generateLayout()
fillGaps()
pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # Press 's' key to save the image
                pygame.image.save(screen, "comic_layout.png")

pygame.quit()
