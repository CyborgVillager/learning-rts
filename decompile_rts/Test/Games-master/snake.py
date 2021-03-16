# -*- coding: utf-8 -*-

import os
import random
import pygame
from pygame.locals import *

pygame.display.init()
window = pygame.display.set_mode((300, 300))
clear  = window.copy()
sizepoint = 10
direction = 1
snake  = [(15, 15)]
apple  = [(5, 5)]

while True:
    pygame.time.wait(250)

    for eventos in pygame.event.get():
        if eventos.type == QUIT:
            pygame.quit()
            os.sys.exit(0)
        elif eventos.type == KEYDOWN:
            if eventos.key == 273:
                direction = 1
            elif eventos.key == 274:
                direction = 2
            elif eventos.key == 275:
                direction = 3
            elif eventos.key == 276:
                direction = 4

    window.blit(clear, (0, 0))

    for node in snake:
        x, y = node
        pygame.draw.rect(window, (255, 255, 255), ((x * sizepoint, y * sizepoint), (sizepoint, sizepoint)), 1)

    x, y = apple[0]
    pygame.draw.rect(window, (255, 0, 0), ((x * sizepoint, y * sizepoint), (sizepoint, sizepoint)), 1)

    if direction == 1:
        x, y = snake[0]
        y -= 1
        y = 29 if y < 0 else y
        snake.insert(0, (x, y))

    elif direction == 2:
        x, y = snake[0]
        y += 1
        y = 0 if y > 29 else y
        snake.insert(0, (x, y))

    elif direction == 3:
        x, y = snake[0]
        x += 1
        x = 0 if x > 29 else x
        snake.insert(0, (x, y))

    elif direction == 4:
        x, y = snake[0]
        x -= 1
        x = 29 if x < 0 else x
        snake.insert(0, (x, y))

    if snake[0] in snake[1:]:
        print("Has perdido")
        pygame.quit()
        os.sys.exit(0)

    if snake[0] != apple[0]:
        snake.pop(len(snake) - 1)

    else:
        apple.pop(0)
        apple.append((random.randint(0, 29), (random.randint(0, 29))))

    pygame.display.flip()
