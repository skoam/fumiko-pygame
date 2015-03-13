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
        self.manages_levels = None
        self.manages_players = None
        self.game_objects = {}

        pygame.init()
        pygame.display.init()
        
        self.physics_controllers = None
        def initialize_physics():
            self.physics_controllers = []

        initialize_physics()

        self.fps = self.settings.get('performance')['frames_per_second']
        self.clock = pygame.time.Clock()
        self._display = pygame.display.set_mode((self.settings.get('screen')['screen_size']['x'],
                                                 self.settings.get('screen')['screen_size']['y']),
                                                self.settings.get('screen')['windowed'])

        if self.settings.get('debug')['on']:
            debug(self, "Initialized Manages Pygame")

        pygame.display.set_caption('NoName Platformer')

    def draw_screen(self):
        if self.manages_levels:
            current_level = self.manages_levels.current_level
            self._display.fill(pygame.Color(current_level.settings["background_color"]))
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
        else:
            self._display.fill(pygame.Color("black"))

        for name, game_object in self.game_objects.items():
            self._display.blit(game_object.image, game_object.rect)

    def update_objects(self):
        for name, game_object in self.game_objects.items():
            game_object.update_rect()
            game_object.get_physics()

    def update_players(self):
        for player_name, player in self.manages_players.players.items():
            if player.input:
                player.get_input()
            else:
                player.input = input.ManagesInput()
                player.input.initialize_controllers()
                player.input.owner = player_name

    def update_physics(self):
        for controller in self.physics_controllers:
            controller.check_for_collision()

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

        self.update_physics()
        self.update_players()
        self.update_objects()
        self.draw_screen()
        self.clock.tick(self.fps)


game = ManagesPygame()
