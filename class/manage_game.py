import pygame
from pygame.locals import *
from common import Size, Position, random_id, read_dict_from_file, debug


class ManagesSettings:
    def __init__(self):
        self.fullscreen = False
        self.screensize = {'x': 800, 'y': 600}
        self.frames_per_second = 60
        self.debug = True

        self.levels = {
            'default_tile_width': 32,
            'default_height': self.screensize["x"] / 1.5
        }

        self.screen = {
            'scale': 2
        }


class ManagesPygame:
    def __init__(self, settings):
        self.settings = settings
        self.manages_levels = None
        self.manages_players = None
        self.joysticks = None
        self.game_objects = {}

        self.input = {
            'joystick': None,
            'up': None,
            'down': None,
            'left': None,
            'right': None
        }

        pygame.init()
        pygame.display.init()

        self.fps = self.settings.frames_per_second
        self.clock = pygame.time.Clock()
        self._display = pygame.display.set_mode((self.settings.screensize['x'],
                                                 self.settings.screensize['y']), self.settings.fullscreen)

        if self.settings.debug:
            debug(self, "Initialized Manages Pygame")

        pygame.display.set_caption('NoName Platformer')

    def initialize_controllers(self):
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for joystick in self.joysticks:
            debug(joystick.get_name(), "Found a gamepad")
        if len(self.joysticks) == 1:
            self.input['joystick'] = self.joysticks[0]
            debug(self.input['joystick'].get_name(), "Setting only available joystick as default")
        elif len(self.joysticks) != 0:
            self.input['joystick'] = self.joysticks[0]
            debug(self.input['joystick'].get_name(), "Setting first joystick as default")
        else:
            self.input['joystick'] = 'keyboard'
            debug(self.input['joystick'], "No joystick, using keyboard as default input")

    def draw_screen(self):
        for name, game_object in self.game_objects.items():
            self._display.blit(game_object.image, game_object.rect)
        if self.manages_levels:
            current_level = self.manages_levels.current_level
            tiles = current_level.populated
            for i in range(0, len(tiles)):
                scale = self.settings.screen["scale"]
                position = Position(current_level.tile_width * scale * i,
                                    self.settings.levels["default_height"] + -10 * tiles[i].height)
                size = Size(current_level.tile_width * scale, 300)
                tile_sprite = current_level.terrains[tiles[i].terrain]
                self._display.blit(tile_sprite, pygame.Rect(position.x,
                                                            position.y,
                                                            size.width, size.height))

    def add(self, game_object):
        if game_object.name not in self.game_objects:
            self.game_objects[game_object.name] = game_object
            if self.settings.debug:
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

    def loop(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.terminate()

        pygame.display.update()
        self.draw_screen()
        self.clock.tick(self.fps)


game = ManagesPygame(ManagesSettings())
