# -*- coding: utf-8 -*-

# marcos.diaz.cast@gmail.com

import pygame
from pygame.locals import *
from config import Config

pygame.mixer.init()

hit  = pygame.mixer.Sound(Config.path_hitsound)
goal = pygame.mixer.Sound(Config.path_goalsound)

