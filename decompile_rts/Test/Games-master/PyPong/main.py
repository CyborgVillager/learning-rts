# -*- coding: utf-8 -*-

# marcos.diaz.cast@gmail.com

import pygame, sys, os
from pygame.locals import *
from config import Config
from ball import Ball
from racket import Racket
from interface import Interface

def end():
    pygame.quit()
    os.sys.exit(0)

def start(size):
    main_clock = pygame.time.Clock()
    pygame.display.init()
    window  = pygame.display.set_mode(size)
    window_ = window.copy() 
    b = Ball()
    r_right   = Racket('R')
    r_left    = Racket('L')
    while True:
        # Event manager
        for event in pygame.event.get():
            if event.type == QUIT:
                end()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    pass
            elif event.type == KEYDOWN:
                #print(event.key)
                if event.key == 273: # Direction key up
                    r_right.direction = 'up'
                    break
                if event.key == 274: # Direction key down
                    r_right.direction = 'down'
                    break
            r_right.direction = False
                    
        window.blit(window_, (0, 0))
        r_right.draw(window)
        r_right.update()
        r_left.computerAI(b)
        r_left.draw(window)
        r_left.update()
        b.draw(window)
        b.update()
        b.collides(r_right, r_left)
        Interface.draw(window, r_left.mark, r_right.mark)
        pygame.display.flip()
        main_clock.tick(100)

start((Config.widthwindow, Config.heightwindow))
