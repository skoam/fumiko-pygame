import Classes.gameobject
import os
import pygame
import Classes.images
from Classes.manage_game import game
from Classes.common import Size, Position, read_dict_from_file, debug


class ManagesLevels:
    def __init__(self):
        self.levels = {}
        self.current_level = None

    def get_levels(self):
        for dirname, dirnames, filenames in os.walk('./levels'):
            for subdirname in dirnames:
                self.levels[subdirname] = Level(subdirname, os.path.join(dirname, subdirname))

    def read_levels(self):
        for level_name, level in self.levels.items():
            level.tileset = level.settings["tileset"]
            level.heightmap = level.settings["heightmap"]
            level.terrainmap = level.settings["terrainmap"]
            if "tile_width" in level.settings:
                level.tile_width = int(level.settings["tile_width"])
            if game.settings.get('debug')['on']:
                debug(level.settings, "Loaded Level " + level_name)
            for object_name, object_settings in level.settings["gobjects"].items():
                gobject_from_level_dict = game.add(
                    Classes.gameobject.GameObject(object_name,
                                          Position(object_settings['position'][0],
                                                   object_settings['position'][1]),
                                          Size(object_settings["size"][0],
                                               object_settings["size"][1])))
                gobject_from_level_dict.chimg(object_settings["image"])

    def load_level(self, level_name):
        self.levels[level_name].slice_chipset()
        self.levels[level_name].populate()
        self.current_level = self.levels[level_name]


class Terrain:
    def __init__(self, index, height, terrain):
        self.index = index
        self.height = height
        self.terrain = terrain


class Level:
    def __init__(self, name, folder):
        self.name = name
        self.folder = folder
        self.populated = None
        self.heightmap = None
        self.terrainmap = None
        self.tileset = None
        self.tile_width = game.settings.get('levels')["default_tile_width"]
        self.terrains = []
        self.settings = read_dict_from_file(folder + "/settings.dict")

    def populate(self):
        self.populated = []
        for i in range(0, len(self.heightmap)):
            self.populated.append(Terrain(i, int(self.heightmap[i]), int(self.terrainmap[i])))

    def slice_chipset(self):
        self.terrains = []
        chipset = Classes.images.get_image(self.tileset)
        chipset_rect = chipset.get_rect()
        number_of_possible_slices = chipset_rect.width / self.tile_width

        for i in range(0, int(number_of_possible_slices)):
            subsurface = chipset.subsurface(pygame.Rect(
                self.tile_width * i, 0, self.tile_width, chipset_rect.height
            ))
            tile_rect = subsurface.get_rect()
            scale = game.settings.get("screen")["scale"]
            subsurface = pygame.transform.scale(subsurface, (tile_rect.width * scale, tile_rect.height * scale))
            self.terrains.append(subsurface)
        debug(self.terrains, "Created " + str(number_of_possible_slices) + " Tiles from " + self.tileset)
