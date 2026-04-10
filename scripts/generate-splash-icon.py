#!/usr/bin/env python3
"""
Generate splash-icon.png matching the PerkUp icon.png style:
- Warm orange/amber gradient background
- Golden coin/stamp element (simplified)
- Stars scattered with motion trails to suggest movement
- Sparkle accent marks
- 600x600px (3x for Retina, displayed at 200px)
"""

import math
import random
from PIL import Image, ImageDraw, ImageFilter

WIDTH = 600
HEIGHT = 600
CENTER = (WIDTH // 2, HEIGHT // 2)

# Color palette extracted from icon.png
BG_TOP = (196, 100, 28)       # Warm dark orange
BG_BOTTOM = (224, 140, 45)    # Lighter orange
COIN_GOLD = (235, 195, 60)    # Bright gold
COIN_DARK = (200, 155, 35)    # Darker gold shadow
COIN_EDGE = (180, 130, 30)    # Edge ticks
STAR_GOLD = (245, 210, 80)    # Star fill
STAR_OUTLINE = (210, 170, 50) # Star edge
SPARKLE_WHITE = (255, 240, 220, 180)  # Warm sparkle
GLOW_AMBER = (255, 200, 80, 40)


def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def draw_gradient(draw, width, height, top, bottom):
    for y in range(height):
        t = y / height
        color = lerp_color(top, bottom, t)
        draw.line([(0, y), (width, y)], fill=color)


def draw_star(draw, cx, cy, outer_r, inner_r, points=5, fill=STAR_GOLD, outline=STAR_OUTLINE, rotation=0):
    coords = []
    for i in range(points * 2):
        angle = math.radians(rotation + i * 180 / points - 90)
        r = outer_r if i % 2 == 0 else inner_r
        coords.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(coords, fill=fill, outline=outline)


def draw_motion_trail(draw, cx, cy, star_r, direction_angle, trail_length, alpha_img):
    """Draw a fading trail behind a star to suggest motion."""
    trail_draw = ImageDraw.Draw(alpha_img)
    steps = 8
    for i in range(steps, 0, -1):
        offset = trail_length * (i / steps)
        ox = cx + offset * math.cos(math.radians(direction_angle))
        oy = cy + offset * math.sin(math.radians(direction_angle))
        trail_r = star_r * (0.3 + 0.4 * (1 - i / steps))
        alpha = int(60 * (1 - i / steps))
        trail_draw.ellipse(
            [ox - trail_r, oy - trail_r, ox + trail_r, oy + trail_r],
            fill=(245, 210, 80, alpha)
        )


def draw_sparkle(draw, cx, cy, size, color=SPARKLE_WHITE):
    """Draw a 4-point sparkle/cross accent."""
    arm = size
    thin = max(1, size // 6)
    # Vertical
    draw.line([(cx, cy - arm), (cx, cy + arm)], fill=color, width=thin)
    # Horizontal
    draw.line([(cx - arm, cy), (cx + arm, cy)], fill=color, width=thin)
    # Small diagonal accents
    d = arm * 0.5
    draw.line([(cx - d, cy - d), (cx + d, cy + d)], fill=color, width=max(1, thin - 1))
    draw.line([(cx + d, cy - d), (cx - d, cy + d)], fill=color, width=max(1, thin - 1))


def draw_coin(draw, cx, cy, radius):
    """Draw a simplified golden coin with star cutout and notched edge."""
    # Outer shadow
    for i in range(6, 0, -1):
        shadow_alpha = 30 - i * 4
        sr = radius + i * 2
        draw.ellipse(
            [cx - sr, cy - sr, cx + sr, cy + sr],
            fill=lerp_color(BG_TOP, (0, 0, 0), 0.15)
        )

    # Main coin body - gradient effect via concentric circles
    for r in range(radius, 0, -1):
        t = 1 - r / radius
        color = lerp_color(COIN_DARK, COIN_GOLD, t * 0.8 + 0.1)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)

    # Highlight arc (top-left)
    highlight_r = int(radius * 0.85)
    draw.ellipse(
        [cx - highlight_r, cy - highlight_r, cx + highlight_r - 20, cy + highlight_r - 20],
        fill=None, outline=lerp_color(COIN_GOLD, (255, 255, 230), 0.4), width=3
    )

    # Edge notches (tick marks around perimeter)
    notch_count = 60
    for i in range(notch_count):
        angle = math.radians(i * 360 / notch_count)
        inner = radius - 12
        outer = radius - 2
        x1 = cx + inner * math.cos(angle)
        y1 = cy + inner * math.sin(angle)
        x2 = cx + outer * math.cos(angle)
        y2 = cy + outer * math.sin(angle)
        draw.line([(x1, y1), (x2, y2)], fill=COIN_EDGE, width=2)

    # Inner ring
    inner_ring_r = int(radius * 0.72)
    draw.ellipse(
        [cx - inner_ring_r, cy - inner_ring_r, cx + inner_ring_r, cy + inner_ring_r],
        fill=None, outline=COIN_EDGE, width=2
    )

    # Star cutout in center
    draw_star(draw, cx, cy, int(radius * 0.45), int(radius * 0.2),
              fill=lerp_color(COIN_DARK, BG_TOP, 0.5), outline=COIN_EDGE, rotation=0)

    # Smaller highlight star overlay
    draw_star(draw, cx - 5, cy - 5, int(radius * 0.35), int(radius * 0.15),
              fill=lerp_color(COIN_GOLD, (255, 255, 200), 0.3),
              outline=None, rotation=0)


def main():
    random.seed(42)  # Reproducible layout

    # Base layer with gradient
    img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    bg = Image.new('RGB', (WIDTH, HEIGHT))
    bg_draw = ImageDraw.Draw(bg)
    draw_gradient(bg_draw, WIDTH, HEIGHT, BG_TOP, BG_BOTTOM)

    # Add subtle radial vignette
    for r in range(max(WIDTH, HEIGHT), 0, -2):
        t = r / max(WIDTH, HEIGHT)
        if t > 0.5:
            alpha = int(40 * (t - 0.5) * 2)
            bg_draw.ellipse(
                [CENTER[0] - r, CENTER[1] - r, CENTER[0] + r, CENTER[1] + r],
                fill=None, outline=lerp_color(BG_BOTTOM, BG_TOP, t)
            )

    img = bg.convert('RGBA')

    # Motion trail layer (RGBA for alpha)
    trail_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))

    # Star definitions: (cx, cy, size, motion_angle, trail_length)
    # Stars emanating outward from the coin area, suggesting "perks flying out"
    stars = [
        # Large prominent stars
        (380, 130, 42, 225, 60),   # top-right, trail toward bottom-left
        (310, 270, 36, 210, 50),   # mid-right
        (420, 350, 28, 235, 45),   # right
        # Medium stars
        (480, 180, 22, 240, 35),
        (350, 450, 24, 220, 40),
        (470, 480, 18, 230, 30),
        # Small stars
        (520, 100, 14, 250, 25),
        (540, 300, 12, 245, 20),
        (440, 540, 10, 215, 18),
        (510, 440, 11, 230, 22),
    ]

    draw = ImageDraw.Draw(img)

    # Draw motion trails first (behind stars)
    for cx, cy, size, angle, trail_len in stars:
        draw_motion_trail(draw, cx, cy, size, angle, trail_len, trail_layer)

    img = Image.alpha_composite(img, trail_layer)
    draw = ImageDraw.Draw(img)

    # Draw the coin (left-center, partially cut off like the icon)
    coin_radius = 170
    coin_cx = 140
    coin_cy = HEIGHT // 2
    draw_coin(draw, coin_cx, coin_cy, coin_radius)

    # Draw stars on top
    for cx, cy, size, angle, trail_len in stars:
        inner = size * 0.42
        draw_star(draw, cx, cy, size, inner, fill=STAR_GOLD, outline=STAR_OUTLINE)

    # Sparkle accents (small cross marks scattered between stars)
    sparkles = [
        (345, 190, 8), (455, 260, 6), (395, 420, 7),
        (530, 160, 5), (490, 380, 6), (560, 520, 4),
        (320, 530, 5), (410, 100, 5), (555, 250, 4),
    ]
    for sx, sy, sz in sparkles:
        draw_sparkle(draw, sx, sy, sz)

    # Add a subtle golden glow around the coin
    glow_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    for r in range(coin_radius + 40, coin_radius, -1):
        alpha = int(25 * (1 - (r - coin_radius) / 40))
        glow_draw.ellipse(
            [coin_cx - r, coin_cy - r, coin_cx + r, coin_cy + r],
            fill=(255, 210, 80, alpha)
        )
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(8))
    # Composite glow behind coin
    final = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    final = Image.alpha_composite(final, img)

    # Save as PNG (no transparency for splash — flatten to BG)
    flat = Image.new('RGB', (WIDTH, HEIGHT), (210, 120, 36))
    flat.paste(final, mask=final.split()[3])

    output_path = '/Users/vikas/Documents/PerkUp/assets/images/splash-icon.png'
    flat.save(output_path, 'PNG', optimize=True)
    print(f'Saved splash-icon.png ({flat.size[0]}x{flat.size[1]}) to {output_path}')


if __name__ == '__main__':
    main()
