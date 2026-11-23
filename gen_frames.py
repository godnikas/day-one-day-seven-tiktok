#!/usr/bin/env python3
"""NEON DODGE - tiny agent-built dodger game, rendered as video frames.

Day 1 (frames 0-239, 8s): same map, same start, 3 slow grey blocks, no coins.
Day 7 (frames 240-644, 13.5s): same map/start, 14 fast coloured blocks,
gold coins, particle trails, combo counter, score climbing fast.
Camera is static in both: the change is the story.
Deterministic: fixed seed, positions are pure functions of frame index.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 540, 960
FPS = 30
DAY1_FRAMES = 240          # 8.0 s
TOTAL_FRAMES = 645         # 21.5 s
OUT = "/tmp/neondodge/frames"

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

rng = random.Random(42)

# ---- precomputed spawns: (spawn_t, x, speed, size, colour) ----
BLOCK_COLOURS = ["#ff2e88", "#22d3ee", "#facc15", "#fb923c", "#a78bfa"]
spawns = []
for i in range(14):
    spawns.append({
        "t": 0.5 + i * 0.55 + rng.uniform(-0.15, 0.15),
        "x": rng.randint(40, W - 40),
        "speed": rng.uniform(240, 430),
        "size": rng.randint(34, 56),
        "colour": BLOCK_COLOURS[i % len(BLOCK_COLOURS)],
    })
coins = [{"t": 1.0 + i * 0.9, "x": rng.randint(50, W - 50),
          "speed": 200.0} for i in range(12)]
stars = [(rng.randint(0, W), rng.randint(0, 700)) for _ in range(70)]


def player_x(t: float) -> float:
    """Same flight path on day 1 and day 7 (identical start, identical map)."""
    return 270 + 95 * math.sin(t * 0.85) + 28 * math.sin(t * 2.3)


def base_bg(day7: bool) -> Image.Image:
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        f = y / H
        r = int(11 + 14 * f)
        g = int(16 + 10 * f)
        b = int(38 + 34 * f)
        d.line([(0, y), (W, y)], fill=(r, g, b))
    # faint grid
    for gx in range(0, W + 1, 60):
        d.line([(gx, 0), (gx, H)], fill=(24, 32, 66))
    for gy in range(0, H + 1, 60):
        d.line([(0, gy), (W, gy)], fill=(24, 32, 66))
    if day7:
        for (sx, sy) in stars:
            d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(180, 200, 255))
    # ground line
    d.rectangle([0, 900, W, 906], fill=(34, 211, 238) if day7 else (90, 100, 130))
    return img


def draw_frame(n: int) -> Image.Image:
    t = n / FPS
    day7 = n >= DAY1_FRAMES
    img = base_bg(day7)
    d = ImageDraw.Draw(img, "RGBA")
    f_title = ImageFont.truetype(BOLD, 34)
    f_small = ImageFont.truetype(BOLD, 24)
    f_score = ImageFont.truetype(MONO, 40)

    px, py = player_x(t), 830

    # falling blocks (day 1: first 3, slow + grey; day 7: all 14, fast + colour)
    active = spawns[:3] if not day7 else spawns
    for b in active:
        age = t - b["t"]
        if age < 0:
            continue
        speed = 120.0 if not day7 else b["speed"]
        y = -40 + ((age * speed) % 1000)  # loop: endless falling blocks
        s = b["size"]
        col = "#8a93a6" if not day7 else b["colour"]
        d.rounded_rectangle([b["x"] - s / 2, y - s / 2, b["x"] + s / 2, y + s / 2],
                            radius=8, fill=col, outline=(255, 255, 255), width=2)
        if day7:  # motion trail
            d.rectangle([b["x"] - s / 2 + 6, y - s / 2 - 26,
                         b["x"] + s / 2 - 6, y - s / 2 - 4], fill=col + "55")

    # coins (day 7 only)
    if day7:
        for c in coins:
            age = t - c["t"]
            if age < 0:
                continue
            y = -30 + ((age * c["speed"]) % 1000)  # loop: endless coins
            d.ellipse([c["x"] - 14, y - 14, c["x"] + 14, y + 14],
                      fill=(250, 204, 21), outline=(255, 255, 255), width=2)
            d.text((c["x"] - 6, y - 10), "$", font=f_small, fill=(120, 80, 0))

    # particles trailing the player (day 7 only)
    if day7:
        for k in range(8):
            pt = t - k * 0.045
            tx = player_x(pt)
            d.ellipse([tx - 5, 852 + k * 7, tx + 5, 862 + k * 7],
                      fill=(34, 211, 238, max(0, 200 - k * 25)))

    # player ship (same in both)
    d.polygon([(px, py - 26), (px - 22, py + 18), (px + 22, py + 18)],
              fill=(34, 211, 238), outline=(255, 255, 255), width=2)
    d.ellipse([px - 6, py - 4, px + 6, py + 8], fill=(255, 255, 255))

    # HUD last so text stays readable over the action
    tag = "DAY 7" if day7 else "DAY 1"
    d.text((24, 22), "NEON DODGE", font=f_title, fill=(255, 255, 255))
    d.text((W - 130, 26), tag, font=f_small,
           fill=(255, 46, 136) if day7 else (150, 160, 190))
    score = int(t * 47) if day7 else int(t * 3)
    d.text((24, 70), f"SCORE {score:05d}", font=f_score, fill=(250, 204, 21))
    if day7:
        d.text((24, 122), "COMBO x7", font=f_small, fill=(34, 211, 238))

    return img


def main():
    import os
    os.makedirs(OUT, exist_ok=True)
    for n in range(TOTAL_FRAMES):
        draw_frame(n).save(f"{OUT}/f{n:04d}.png")
        if n % 100 == 0:
            print(f"frame {n}/{TOTAL_FRAMES}")
    print(f"done: {TOTAL_FRAMES} frames in {OUT}")


if __name__ == "__main__":
    main()
