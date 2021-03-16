# -*- coding: utf-8 -*-

# marcos.diaz.cast@gmail.com

import pygame
import sys
import os
import player
import game
import util
import interface
from config import Config
from pygame.locals import *

KEYMAP = {
    'up'   :273,
    'down' :274,
    'right':275,
    'left' :276,
    'reset':114 # 'r'
}

def end():
    pygame.quit()
    os.sys.exit(0)

def run_game(level):
    main_clock = pygame.time.Clock()
    itrface = interface.Interface()
    human_player, game_board = itrface.load_level(level)
    while True:
        # Event manager
        for event in pygame.event.get():
            if event.type == QUIT:
                end()
            elif event.type == KEYDOWN:
                #print(event.key)
                if event.key == KEYMAP['up']:
                    new_pos = human_player.get_position(to='up')
                    if game_board.is_valid(*new_pos):
                        human_player.up()
                    else:
                        box = game_board.get_box(*new_pos)
                        if box:
                            new_pos = box.get_position(to='up')
                            if game_board.is_valid(*new_pos):
                                human_player.up()
                                box.up()
                    break
                    
                if event.key == KEYMAP['down']:
                    new_pos = human_player.get_position(to='down')
                    if game_board.is_valid(*new_pos):
                        human_player.down()
                    else:
                        box = game_board.get_box(*new_pos)
                        if box:
                            new_pos = box.get_position(to='down')
                            if game_board.is_valid(*new_pos):
                                human_player.down()
                                box.down()
                    break
                    
                if event.key == KEYMAP['right']:
                    new_pos = human_player.get_position(to='right')
                    if game_board.is_valid(*new_pos):
                        human_player.right()
                    else:
                        box = game_board.get_box(*new_pos)
                        if box:
                            new_pos = box.get_position(to='right')
                            if game_board.is_valid(*new_pos):
                                human_player.right()
                                box.right()
                    break
                    
                if event.key == KEYMAP['left']:
                    new_pos = human_player.get_position(to='left')
                    if game_board.is_valid(*new_pos):
                        human_player.left()
                    else:
                        box = game_board.get_box(*new_pos)
                        if box:
                            new_pos = box.get_position(to='left')
                            if game_board.is_valid(*new_pos):
                                human_player.left()
                                box.left()
                                
                if event.key == KEYMAP['reset']:
                    human_player, game_board = util.load_level(level)
                    
        itrface.draw(human_player, game_board)
        
        if game_board.lvlcompleted():
            end()
        
        pygame.display.flip()
        main_clock.tick(100)

if __name__ == '__main__':
    run_game('1.lvel')
