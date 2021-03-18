import pygame, sys, colors
from pygame.locals import *

# Start the program
pygame.init()

# FPS value
FPS = 30
FramePerSec = pygame.time.Clock()

# Display with caption
DISPLAYSURF = pygame.display.set_mode((400,400))
DISPLAYSURF.fill(colors.PASTELBLUE)
pygame.display.set_caption("Example")

# Creation of lines/shapes
pygame.draw.line(DISPLAYSURF, colors.GREEN,(150,130),(130,170))
pygame.draw.line(DISPLAYSURF, colors.GREEN,(150,130),(170,170))
pygame.draw.line(DISPLAYSURF, colors.BLUE,(130,170),(170,170))
pygame.draw.circle(DISPLAYSURF, colors.BLACK,(100,50),30)
pygame.draw.circle(DISPLAYSURF, colors.BLACK,(200,50),30)
pygame.draw.rect(DISPLAYSURF, colors.RED,(110,260,80,5))

"""
while True:
    pygame.display.update()
    for event in pygame.event.get():
        pygame.quit()
        sys.exit()
    FramePerSec.tick(FPS)
    
"""