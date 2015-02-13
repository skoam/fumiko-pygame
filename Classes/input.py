import actions
import pygame
from common import debug


class ManagesInput:
    def __init__(self):
        self.joysticks = None
        self.input_source = None
        self.actions = actions.ActionSet()
        self.buttons_pressed = []

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

        init_controller = getattr(self.input_source, "init", None)
        if callable(init_controller):
            self.input_source.init()

    def get_input(self):
        if self.input_source and self.input_source.get_button:
            for action in self.actions.current():
                if (not self.buttons_pressed.__contains__(action) and action != 'name' and
                        self.input_source.get_button(self.actions.current()[action]) == 1):
                    debug(action, "button is pressed")
                    self.buttons_pressed.append(action)
                elif (self.buttons_pressed.__contains__(action) and action != 'name' and
                        self.input_source.get_button(self.actions.current()[action]) == 0):
                    debug(action, "button was released")
                    self.buttons_pressed.remove(action)