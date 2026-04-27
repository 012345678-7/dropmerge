import pygame
import random
import sys
import os
import math

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

pygame.init()
W = 480
H = 800
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("掉落合成")
clock = pygame.time.Clock()
FPS = 60

LINE_Y = 180
game_over = False
gravity = 0.7

images = []
for i in range(9):
    img_path = resource_path(f"{i}.png")
    img = pygame.image.load(img_path).convert_alpha()
    img = pygame.transform.smoothscale(img, (52, 52))
    images.append(img)

balls = []
fall = None

def reset():
    global game_over, balls, fall
    game_over = False
    balls.clear()
    fall = None

reset()

while True:
    screen.fill((255, 255, 255))
    pygame.draw.line(screen, (255, 0, 0), (0, LINE_Y), (W, LINE_Y), 5)
    mx, my = pygame.mouse.get_pos()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                reset()
            else:
                if fall is None:
                    fall = {
                        "x": mx,
                        "y": LINE_Y - 40,
                        "lv": random.randint(0, 4),
                        "vy": 0
                    }

    if fall is not None:
        fall["vy"] += gravity
        fall["y"] += fall["vy"]
        stop = False

        if fall["y"] > H - 60:
            stop = True
        for b in balls:
            dis = math.hypot(fall["x"] - b["x"], fall["y"] - b["y"])
            if dis < 50:
                stop = True
                break

        if stop:
            balls.append(fall)
            fall = None

    for b in balls:
        if b["y"] < LINE_Y - 30:
            game_over = True

    new_balls = []
    for a in balls:
        merged = False
        for b in new_balls:
            if a["lv"] == b["lv"]:
                dis = math.hypot(a["x"] - b["x"], a["y"] - b["y"])
                if dis < 50:
                    new_balls.append({
                        "x": (a["x"] + b["x"]) / 2,
                        "y": (a["y"] + b["y"]) / 2,
                        "lv": min(a["lv"] + 1, 8)
                    })
                    merged = True
                    break
        if not merged:
            new_balls.append(a)
    balls = new_balls

    for b in balls:
        img = images[b["lv"]]
        rect = img.get_rect(center=(b["x"], b["y"]))
        screen.blit(img, rect)

    if fall is not None:
        img = images[fall["lv"]]
        rect = img.get_rect(center=(fall["x"], fall["y"]))
        screen.blit(img, rect)

    if game_over:
        pygame.draw.rect(screen, (200, 0, 0), (100, 300, 280, 150), 5)

    pygame.display.update()
    clock.tick(FPS)
