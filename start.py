# A structure for creating platformers with python-pygame
# There will be more documentation in the future.
# Reminder to myself: Keep commenting and/or write clean code. No messing around unless time is short.

import sys
import pygame
import level
import player
from manage_game import game


def main():
    game.manages_levels = level.ManagesLevels()
    game.manages_players = player.ManagesPlayers()
    game.start()
    game.initialize_controllers()
    while True:  # main game loop
        game.loop()


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
