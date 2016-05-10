from collections import defaultdict
import itertools


class Architecture:
    def __init__(self):
        self._manipulators = {}

    def get_actions(self):
        """
        Gives the Descartes product of all the possible values of all manipulators
        :return: set of action vectors (tuples)
        """
        interpretation_intervals = [self._manipulators[k].get_interpretation_interval() for k in self._manipulators]
        return [x for x in itertools.product(*interpretation_intervals)]  # create the product of each intervals


class WoodCutter(Architecture):

    def __init__(self, forest_environment):
        super().__init__()

        # save the environment for later... (it might be not necessary)
        self.forest = forest_environment

        # add a manipulators
        gardener = DiscreteActionHandler()
        gardener.set_action_handler('wait', forest_environment.wait_one_more_year)
        gardener.set_action_handler('cut_and_plant', forest_environment.cut_down_trees)
        self._manipulators['gardener'] = gardener

    def interact(self, action_vector):
        """
        Observes the environment after executes the action in the parameter.
        :param action_vector: tuple of action indexes indexed by manipulator ID's, which a "composite" action.
        :return: observation of the environment, and the reward
        """
        try:
            if len(action_vector) != len(self._manipulators):
                raise ValueError

            # this is a special way for this situation:
            reward = 0
            # TODO: this can be in the superclass: execute_and_sum_reward
            tuple_index = 0  # for the iteration on the tuple
            for manipulator_name in self._manipulators:
                manipulator_action = self._manipulators[manipulator_name].get_action_handler(action_vector[tuple_index])
                reward += manipulator_action()
                tuple_index += 1

            print(self.forest.money)

            return self.forest.tree_age, reward  # tree age is the observation

        except (KeyError, ValueError):
            print('Action vector does not fit for the manipulators!')
            raise

    def initial_state(self):
        return self.forest.tree_age


class MazeMan(Architecture):

    def __init__(self, maze):
        super().__init__()
        self.maze = maze
        self.position = MazeMan.initial_state()
        self._manipulators['walk'] = {'up': self._up}

    def interact(self, action_vector):
        action_id = action_vector['walk']
        action = self._manipulators['walk'][action_id]
        action()

        in_finish = self.position['x'] == 1 and self.position['y'] == 9
        if in_finish:
            return self.position, 10
        else:
            return self.position, 0

    def get_actions(self):
        actions = {}
        x = self.position['x']
        y = self.position['y']

        if self.maze.get_area(x - 1, y) == 1:
            actions['up'] = self._up

        if self.maze.get_area(x + 1, y) == 1:
            actions['down'] = self._down

        if self.maze.get_area(x, y - 1) == 1:
            actions['left'] = self._left

        if self.maze.get_area(x, y + 1) == 1:
            actions['right'] = self._right

        self._manipulators['walk'] = actions
        # TODO: should return the descartes product...
        return self._manipulators['walk'].keys()

    def _up(self):
        self.position['x'] -= 1

    def _down(self):
        self.position['x'] += 1

    def _left(self):
        self.position['y'] -= 1

    def _right(self):
        self.position['y'] += 1

    @staticmethod
    def initial_state():
        return {'x': 9, 'y': 1}


class DiscreteActionHandler:
    def __init__(self):
        self._action_table = defaultdict(lambda: lambda: print("Unimplemented action!"))

    def get_action_handler(self, action_name):
        """
        Get the action for the execution by index/id.
        :param action_name: Action index/id
        :return: The action with the given name
        """
        return self._action_table[action_name]

    def set_action_handler(self, action_name, action_handler):
        """
        Set action for an action ID.
        :param action_name: Index on the action
        :param action_handler: A function which has to be executed for the given action ID/index
        :return: None
        """
        self._action_table[action_name] = action_handler

    def get_interpretation_interval(self):
        """
        Returns all the possible action ID's.
        :return: List of possible keys
        """
        return self._action_table.keys()

"""
class ContinuousActionHandler:
    def __init__(self, name, resolution):
        self.name = name
        self.resolution = resolution
        self._action_table = defaultdict(lambda: lambda: print("Unimplemented action!"))

    def sample(self, sample_point):
        for points in self.get_interpretation_interval():
            (begin, end) = points
            if begin < sample_point < end:
                return self._action_table[points]

    def set_action_handler(self, interval, action_handler):
        (begin, end) = interval
        if end < begin:
            raise Exception("Starting point of interval must be lower than ending point!")

        for i in self._action_table:
            (i_begin, i_end) = i
            if i_begin <= interval.end or interval.begin <= i_end:
                raise Exception("Intervals shouldn't overlap each other!")

        self._action_table[interval] = action_handler

    def get_interpretation_interval(self):
        pass

"""
from Environment import *

maze = MazeEnvironment()
mm = MazeMan(maze)

print(mm.get_actions())
mm.interact({'walk': 'up'})
print(mm.get_actions())
mm.interact({'walk': 'up'})
print(mm.get_actions())
mm.interact({'walk': 'up'})
print(mm.get_actions())
mm.interact({'walk': 'up'})
print(mm.get_actions())
