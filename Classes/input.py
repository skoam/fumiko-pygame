import pygame
from common import debug


class ManagesInput:
    def __init__(self):
        self.joysticks = None
        self.input_source = None

        self.input = {
            'up': None,
            'down': None,
            'left': None,
            'right': None
        }

        self.input_config = {
            '0': 'B',
            '1': 'A',
            '2': 'C'
        }

    def initialize_controllers(self):
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for joystick in self.joysticks:
            debug(joystick.get_name(), "Found a gamepad")
        if len(self.joysticks) == 1:
            self.input_source = self.joysticks[0]
            debug(self.input_source.get_name(), "Setting only available joystick as default")
        elif len(self.joysticks) != 0:
            self.input_source = self.joysticks[0]
            debug(self.input_source.get_name(), "Setting first joystick as default")
        else:
            self.input_source = 'keyboard'
            debug(self.input_source, "No joystick, using keyboard as default input")

        if self.input_source.init:
            self.input_source.init()

    def get_input(self):
        if self.input_source and self.input_source.get_button:
            if self.input_source.get_button(0) == 1:
                debug(self.input_config['0'], "button is pressed")