from Classes.common import read_dict_from_file


class ActionSet:
    def __init__(self):
        self.action_sets = {}
        self.current_set = None
        self.load_set('default_actions')

    def change_set(self, action_set):
        self.current_set = self.action_sets[action_set]

    def add_set(self, action_set):
        self.action_sets[action_set['name']] = action_set

    def load_set(self, name):
        action_set = read_dict_from_file('./settings/' + name + '.dict')
        self.action_sets[action_set['name']] = action_set
        self.current_set = self.action_sets[action_set['name']]

    def current(self):
        return self.current_set