# A structure for creating platformers with python-pygame
# There will be more documentation in the future.
# Reminder to myself: Keep commenting and/or write clean code. No messing around unless time is short.

import sys
import pygame
import Classes.level as level
import Classes.player as player
from Classes.manage_game import game


def main():
    game.manages_levels = level.ManagesLevels()
    game.manages_players = player.ManagesPlayers()
    game.start()
    game.input.initialize_controllers()
    while True:  # main game loop
        game.loop()


if __name__ == '__main__':
    main()
