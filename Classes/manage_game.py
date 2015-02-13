import sys
import pygame
import input
from pygame.locals import *
from common import Size, Position, debug


class ManagesSettings:
    def __init__(self):
        self.settings = {
            'debug': {
                'on': True
            },
            'performance': {
                'frames_per_second': 60
            },
            'screen': {
                'windowed': True,
                'screen_size': {'x': 800, 'y': 600},
                'scale': 2
            },
            'levels': {
                'default_tile_width': 32,
                'default_height': None
            }
        }

        self.settings['levels']['default_height'] = self.settings['screen']['screen_size']["x"] / 1.5

    def get(self, name):
        return self.settings[name]


class ManagesPygame:
    def __init__(self):
        self.settings = ManagesSettings()
        self.input = input.ManagesInput()
        self.manages_levels = None
        self.manages_players = None
        self.game_objects = {}

        pygame.init()
        pygame.display.init()

        self.fps = self.settings.get('performance')['frames_per_second']
        self.clock = pygame.time.Clock()
        self._display = pygame.display.set_mode((self.settings.get('screen')['screen_size']['x'],
                                                 self.settings.get('screen')['screen_size']['y']),
                                                self.settings.get('screen')['windowed'])

        if self.settings.get('debug')['on']:
            debug(self, "Initialized Manages Pygame")

        pygame.display.set_caption('NoName Platformer')

    def draw_screen(self):
        for name, game_object in self.game_objects.items():
            self._display.blit(game_object.image, game_object.rect)
        if self.manages_levels:
            current_level = self.manages_levels.current_level
            tiles = current_level.populated
            for i in range(0, len(tiles)):
                scale = self.settings.get('screen')['scale']
                position = Position(current_level.tile_width * scale * i,
                                    self.settings.get('levels')["default_height"] + -10 * tiles[i].height)
                size = Size(current_level.tile_width * scale, 300)
                tile_sprite = current_level.terrains[tiles[i].terrain]
                self._display.blit(tile_sprite, pygame.Rect(position.x,
                                                            position.y,
                                                            size.width, size.height))

    def add(self, game_object):
        if game_object.name not in self.game_objects:
            self.game_objects[game_object.name] = game_object
            if self.settings.get('debug')['on']:
                debug(game_object, "Added Game Object")
            return game_object
        else:
            return self.game_objects[game_object.name]

    def start(self):
        self.manages_levels.get_levels()
        self.manages_levels.read_levels()
        self.manages_levels.load_level("Level_1_Start")
        self.manages_players.get_players()
        self.manages_players.load_player("Fumiko")

    @staticmethod
    def terminate():
        pygame.quit()
        sys.exit()

    def loop(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.terminate()

        pygame.display.update()
        self.input.get_input()

        self.draw_screen()
        self.clock.tick(self.fps)


game = ManagesPygame()



