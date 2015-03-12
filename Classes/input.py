import actions
import pygame
from common import debug


class ManagesInput:
    def __init__(self):
        self.joysticks = None
        self.input_source = None
        self.actions = actions.ActionSet()
        self.buttons_pressed = []
        self.axis_values = {}
        self.owner = None

    def initialize_controllers(self):
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        # for joystick in self.joysticks:
            # debug(joystick.get_name(), "Found a gamepad")
        if len(self.joysticks) == 1:
            self.input_source = self.joysticks[0]
            # debug(self.input_source.get_name(), "Setting only available joystick as default")
        elif len(self.joysticks) != 0:
            self.input_source = self.joysticks[0]
            # debug(self.input_source.get_name(), "Setting first joystick as default")
        else:
            self.input_source = 'keyboard'
            # debug(self.input_source, "No joystick, using keyboard as default input")

        init_controller = getattr(self.input_source, "init", None)
        if callable(init_controller):
            self.input_source.init()
            # debug(self.input_source.get_numbuttons(), "Available buttons for joystick")

    def get_input(self):
        if self.input_source and self.input_source.get_button and self.owner:
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
                                debug(action, "button was released")
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
