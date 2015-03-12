import pygame
import gameobject
import images
import os
from common import Size, read_dict_from_file, debug
from manage_game import game


class ManagesPlayers:
    def __init__(self):
        self.folder = "./players"
        self.players = {}

    def get_players(self):
        for dirname, dirnames, filenames in os.walk(self.folder):
            for subdirname in dirnames:
                self.players[subdirname] = Player(subdirname, os.path.join(dirname, subdirname))

    def load_player(self, player_name):
        self.players[player_name].spawn()


class Player:
    def __init__(self, name, folder):
        self.name = name
        self.folder = folder
        self.representation = None
        self.settings = read_dict_from_file(folder + "/settings.dict")
        self.charset_list = None
        self.charset_lib = {}
        self.charset = {}
        self.input = None

        self.slice_charset()
        self.spawn()
    
    def get_input(self):
        self.input.get_input()
        if self.input.buttons_pressed.__contains__("left"):
            self.representation.position.x -= 10
        if self.input.buttons_pressed.__contains__("right"):
            self.representation.position.x += 10
        if self.input.buttons_pressed.__contains__("up"):
            self.representation.position.y -= 10
        if self.input.buttons_pressed.__contains__("down"):
            self.representation.position.y += 10

    def spawn(self):
        if not self.representation:
            actual_object_size = Size(self.settings["tile_size"].width *
                                      self.settings["scale"] *
                                      game.settings.get('screen')["scale"],
                                      self.settings["tile_size"].height *
                                      self.settings["scale"] *
                                      game.settings.get('screen')["scale"])
            self.representation = gameobject.GameObject(self.settings["name"],
                                                        self.settings["position"],
                                                        actual_object_size,
                                                        self.charset_lib["default"])
            game.add(self.representation)

    def slice_charset(self):
        self.charset_list = []
        self.charset_lib = {}
        charset = images.get_image(self.settings["charset"])
        charset_rect = charset.get_rect()
        width = self.settings["tile_size"].width
        height = self.settings["tile_size"].height
        number_of_horizontal_slices = charset_rect.width / width
        number_of_vertical_slices = charset_rect.height / height

        for v in range(0, number_of_vertical_slices):
            for h in range(0, number_of_horizontal_slices):
                subsurface = charset.subsurface(pygame.Rect(
                    width * h, height * v,
                    width, height
                ))

                tile_rect = subsurface.get_rect()
                scale = game.settings.get('screen')["scale"]
                subsurface = pygame.transform.scale(subsurface, (tile_rect.width * scale, tile_rect.height * scale))
                self.charset_list.append(subsurface)

        self.charset_lib["default"] = self.charset_list[60]
        debug(self.charset_list, "Created " +
              str(number_of_horizontal_slices * number_of_vertical_slices) +
              " Tiles from " + self.settings["charset"])
