import actions
import pygame
from common import debug
from pygame.locals import *

class ManagesInput:
    def __init__(self):
        self.joysticks = None
        self.input_source = None
        self.mappings = actions.ActionSet()
        self.actions = actions.ActionSet()
        self.buttons_pressed = []
        self.actions_active = []
        self.axis_values = {}
        self.owner = None

    def initialize_controllers(self):
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        # for joystick in self.joysticks:
            # debug(joystick.get_name(), "Found a gamepad")
        if len(self.joysticks) == 1:
            self.input_source = self.joysticks[0]
            self.actions.load_set('xbox_controller')
            self.mappings.load_set('xbox_controller_mappings')
            # debug(self.input_source.get_name(), "Setting only available joystick as default")
        elif len(self.joysticks) != 0:
            self.input_source = self.joysticks[0]
            self.actions.load_set('xbox_controller')
            self.mappings.load_set('xbox_controller_mappings')
            # debug(self.input_source.get_name(), "Setting first joystick as default")
        else:
            self.input_source = 'keyboard'
            self.mappings.load_set('keyboard')
            # debug(self.input_source, "No joystick, using keyboard as default input")
        
        init_controller = getattr(self.input_source, "init", None)
        if callable(init_controller):
            self.input_source.init()
            # debug(self.input_source.get_numbuttons(), "Available buttons for joystick")

    def get_input(self):
        if self.input_source and hasattr(self.input_source, "get_button()")and self.owner:
            for action in self.actions.current():
                if action not in ['name', 'hat', 'invert_Y']:
                    if not self.buttons_pressed.__contains__(action):
                        if action not in ['left', 'right', 'up', 'down',
                                          'Analog_X', 'Analog_Y', 'Analog_View_X', 'Analog_View_Y', 'LT', 'RT']:
                            if self.input_source.get_button(self.actions.current()[action]) == 1:
                                # debug(action, "button is pressed")
                                self.buttons_pressed.append(action)
                        elif action not in ['Analog_X', 'Analog_Y', 'Analog_View_X', 'Analog_View_Y', 'LT', 'RT']:
                            hat = self.input_source.get_hat(0)
                            if action == 'left':
                                if hat[0] == -1:
                                    self.buttons_pressed.append(action)
                                    # debug(action, "button is pressed")
                            elif action == 'right':
                                if hat[0] == 1:
                                    self.buttons_pressed.append(action)
                                    # debug(action, "button is pressed")
                            elif action == 'up':
                                if hat[1] == 1:
                                    self.buttons_pressed.append(action)
                                    # debug(action, "button is pressed")
                            elif action == 'down':
                                if hat[1] == -1:
                                    self.buttons_pressed.append(action)
                                    # debug(action, "button is pressed")
                        elif action not in ['LT', 'RT']:
                            axis = self.input_source.get_axis(self.actions.current()[action])
                            if abs(axis) > 0.2:
                                self.axis_values[action] = axis
                                # debug(action + ":" + str(axis), "Axis is moved")
                            else:
                                self.axis_values[action] = 0
                        else:
                            axis = self.input_source.get_axis(self.actions.current()[action])
                            if axis > 0.2:
                                self.axis_values[action] = axis
                                # debug(action + ":" + str(axis), "Axis is moved")
                            else:
                                self.axis_values[action] = 0
                    elif self.buttons_pressed.__contains__(action):
                        if action not in ['left', 'right', 'up', 'down',
                                          'Analog_X', 'Analog_Y', 'Analog_View_X', 'Analog_View_Y']:
                            if self.input_source.get_button(self.actions.current()[action]) == 0:
                                # debug(action, "button was released")
                                self.buttons_pressed.remove(action)
                        elif action not in ['Analog_X', 'Analog_Y', 'Analog_View_X', 'Analog_View_Y']:
                            hat = self.input_source.get_hat(0)
                            if action == 'left':
                                if hat[0] != -1:
                                    self.buttons_pressed.remove(action)
                                    # debug(action, "button is released")
                            elif action == 'right':
                                if hat[0] != 1:
                                    self.buttons_pressed.remove(action)
                                    # debug(action, "button is released")
                            elif action == 'up':
                                if hat[1] != 1:
                                    self.buttons_pressed.remove(action)
                                    # debug(action, "button is released")
                            elif action == 'down':
                                if hat[1] != -1:
                                    self.buttons_pressed.remove(action)
                                    # debug(action, "button is released")
        else:
            buttons = pygame.key.get_pressed()
            pygame_keys = {
                K_d: 'd',
                K_a: 'a',
                K_s: 's',
                K_w: 'w'
            }
            for key, value in pygame_keys.items():
                if buttons[key] and not self.buttons_pressed.__contains__(value):
                    self.buttons_pressed.append(value)
                elif self.buttons_pressed.__contains__(value):
                    self.buttons_pressed.remove(value)

        for action, mapped_key in self.mappings.current().items():
            if mapped_key in self.buttons_pressed:
                if not self.actions_active.__contains__(action):
                    self.actions_active.append(action)
            elif self.actions_active.__contains__(action):
                self.actions_active.remove(action)
