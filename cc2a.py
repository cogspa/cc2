from PIL import Image, ImageDraw
import random

import os

def get_save_filename(base_filename="comic_layout.png"):
    """Return an incremented filename if the base file already exists."""
    if not os.path.exists(base_filename):
        return base_filename

    # Split filename into name and extension
    name, extension = os.path.splitext(base_filename)

    # Increment the filename until an unused one is found
    counter = 1
    new_name = "{}_{:02}{}".format(name, counter, extension)
    while os.path.exists(new_name):
        counter += 1
        new_name = "{}_{:02}{}".format(name, counter, extension)

    return new_name


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
sequence_number = 1


colWidth = round((WIDTH - (NUM_COLUMNS + 1) * GUTTER_SIZE) / NUM_COLUMNS)
rowHeight = round((HEIGHT - (NUM_ROWS + 1) * GUTTER_SIZE) / NUM_ROWS)

occupied = [[False for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

def canPlacePanel(col, row, colSpan, rowSpan):
    if col + colSpan > NUM_COLUMNS or row + rowSpan > NUM_ROWS:
        return False

    for r in range(row, row + rowSpan):
        for c in range(col, col + colSpan):
            if occupied[r][c]:
                return False
    return True

def random_color():
    """Return a random RGB color."""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
def random_line_pattern(draw, x, y, w, h):
    """Fill the area with random line patterns."""
    num_lines = random.randint(5, 15)
    line_width = random.randint(1, 5)
    spacing = random.randint(5, 20)
    vertical = random.choice([True, False])
    
    if vertical:
        for i in range(num_lines):
            start_x = x + i * spacing
            if start_x > x + w:
                break
            draw.line([(start_x, y), (start_x, y+h)], fill=random_color(), width=line_width)
    else:
        for i in range(num_lines):
            start_y = y + i * spacing
            if start_y > y + h:
                break
            draw.line([(x, start_y), (x+w, start_y)], fill=random_color(), width=line_width)

def random_dot_pattern(draw, x, y, w, h):
    """Fill the area with random dot patterns."""
    num_dots = random.randint(50, 200)
    for _ in range(num_dots):
        dot_x = x + random.randint(0, w)
        dot_y = y + random.randint(0, h)
        dot_radius = random.randint(1, 5)
        draw.ellipse([(dot_x-dot_radius, dot_y-dot_radius), 
                      (dot_x+dot_radius, dot_y+dot_radius)], 
                      fill=random_color(), outline=None)


def createPanel(col, row, colSpan, rowSpan):
    global sequence_number  # to update the sequence number

    x = col * (colWidth + GUTTER_SIZE) + GUTTER_SIZE
    y = row * (rowHeight + GUTTER_SIZE) + GUTTER_SIZE
    w = colSpan * colWidth + (colSpan - 1) * GUTTER_SIZE
    h = rowSpan * rowHeight + (rowSpan - 1) * GUTTER_SIZE
    
    draw.rectangle([(x, y), (x+w, y+h)], fill=random_color(), outline=PANEL_BORDER_COLOR)


    # Add sequence number to the rectangle
    text_size = draw.textsize(str(sequence_number))
    text_x = x + (w - text_size[0]) / 2
    text_y = y + (h - text_size[1]) / 2
    draw.text((text_x, text_y), str(sequence_number), fill=PANEL_BORDER_COLOR)

    sequence_number += 1  # Increment the sequence number for the next rectangle

    for r in range(row, row + rowSpan):
        for c in range(col, col + colSpan):
            occupied[r][c] = True

    pattern_type = random.choice(["line", "dot"])
    if pattern_type == "line":
        random_line_pattern(draw, x, y, w, h)
    elif pattern_type == "dot":
        random_dot_pattern(draw, x, y, w, h)


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

generateLayout()
fillGaps()
img.save(get_save_filename())

img.show()
