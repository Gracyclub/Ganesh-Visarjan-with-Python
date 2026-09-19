import sys
import math
import pygame
from PIL import Image

# Initialize Pygame
pygame.init()

# Window Configuration
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ganpati Visarjan Animation")

clock = pygame.time.Clock()
FPS = 60

# Colors
BG_COLOR = (248, 246, 240)       # Paper tone
TEXT_COLOR = (35, 35, 35)
WATER_COLOR_DARK = (50, 50, 50)
WATER_COLOR_MID = (100, 100, 100)
WATER_COLOR_LIGHT = (160, 160, 160)

WATER_LEVEL = 480  # Y position where water surface starts

# Load and prepare 'bappa.jpg' with transparent background
try:
    pil_img = Image.open("bappaa.jpg").convert("RGBA")
except FileNotFoundError:
    print("Error: Could not find 'bappa.jpg'. Please place it in the same directory.")
    sys.exit()

# Auto-remove white/light background from JPEG
data = pil_img.getdata()
new_data = []
for item in data:
    # Check if pixel is bright/white
    if item[0] > 220 and item[1] > 220 and item[2] > 220:
        new_data.append((255, 255, 255, 0))  # Fully transparent
    else:
        new_data.append(item)
pil_img.putdata(new_data)

# Resize idol
target_width = 300
aspect_ratio = pil_img.height / pil_img.width
target_height = int(target_width * aspect_ratio)
pil_img = pil_img.resize((target_width, target_height), Image.Resampling.LANCZOS)

# Convert PIL Image to Pygame Surface
raw_str = pil_img.tobytes("raw", "RGBA")
ganesha_surf = pygame.image.fromstring(raw_str, pil_img.size, "RGBA")

# Fonts
font_title = pygame.font.SysFont("georgia", 36, bold=True)
font_sub = pygame.font.SysFont("georgia", 24, italic=True)

# Animation parameters
start_y = WATER_LEVEL - target_height + 20
end_y = WATER_LEVEL + 50
curr_y = float(start_y)
speed = 0.6  # Submerging speed
start_delay = 60  # Wait for 1 second before submerging
elapsed_frames = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Press 'R' to restart animation
                curr_y = float(start_y)
                elapsed_frames = 0

    elapsed_frames += 1

    # Update position (Visarjan movement)
    if elapsed_frames > start_delay:
        if curr_y < end_y:
            curr_y += speed

    # 1. Fill background
    screen.fill(BG_COLOR)

    # 2. Draw Top Headings
    title_surface = font_title.render("Ganpati Bappa Morya!", True, TEXT_COLOR)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_surface, title_rect)

    if elapsed_frames > 40:
        sub_surface = font_sub.render("Agle baras tu jaldi aa...", True, TEXT_COLOR)
        sub_rect = sub_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(sub_surface, sub_rect)

    # 3. Draw Ganesha Idol
    g_x = (SCREEN_WIDTH - target_width) // 2
    screen.blit(ganesha_surf, (g_x, int(curr_y)))

    # 4. Water Mask (Hides everything beneath the water line)
    mask_rect = pygame.Rect(0, WATER_LEVEL, SCREEN_WIDTH, SCREEN_HEIGHT - WATER_LEVEL)
    pygame.draw.rect(screen, BG_COLOR, mask_rect)

    # 5. Draw Animated Ripples
    t = elapsed_frames * 0.05
    w1 = math.sin(t * 1.5) * 3
    w2 = math.cos(t * 1.2) * 2.5
    w3 = math.sin(t * 0.9) * 2

    center_x = SCREEN_WIDTH // 2

    # Concentric ellipses to mimic water ripples
    pygame.draw.ellipse(screen, WATER_COLOR_DARK, (center_x - 85, WATER_LEVEL - 9 + w1, 170, 18), 3)
    pygame.draw.ellipse(screen, WATER_COLOR_MID, (center_x - 145, WATER_LEVEL - 15 + w2, 290, 30), 2)
    pygame.draw.ellipse(screen, WATER_COLOR_LIGHT, (center_x - 210, WATER_LEVEL - 21 + w3, 420, 42), 2)
    pygame.draw.ellipse(screen, WATER_COLOR_LIGHT, (center_x - 270, WATER_LEVEL - 27, 540, 54), 1)

    # Update screen
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()