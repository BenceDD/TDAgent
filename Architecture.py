from collections import defaultdict
import itertools


class Architecture:
    def __init__(self):
        self._manipulators = {}

    def get_actions(self):
        """
        Gives the Descartes product of all the possible values of all manipulators
        :return: set of action vectors
        """
        interpretation_intervals = [self._manipulators[k].get_interpretation_interval() for k in self._manipulators]
        return itertools.product(*interpretation_intervals)  # create the product of each intervals


class WoodCutter(Architecture):

    def __init__(self, forest_environment):
        super().__init__()

        # save the environment for later... (it might be not necessary)
        self.forest = forest_environment

        # add a manipulators
        gardener = DiscreteActionHandler()
        gardener.set_action_handler(0, forest_environment.wait_one_more_year)
        gardener.set_action_handler(1, forest_environment.cut_down_trees)
        self._manipulators['gardener'] = gardener

    def interact(self, action_vector):
        """
        Observes the environment after executes the action in the parameter.
        :param action_vector: array of action indexes indexed by manipulator ID's, which a "composite" action.
        :return: observation of the environment, and the reward
        """
        # TODO: is it OK to return with this?
        try:
            if len(action_vector) != len(self._manipulators):
                raise ValueError

            reward = 0

            for manipulator_name in action_vector:  # interact with the environment with manipulators one by one
                manipulator_action = self._manipulators[manipulator_name].sample(action_vector[manipulator_name])
                reward += manipulator_action()

            return self.forest.tree_age, reward

        except (KeyError, ValueError):
            print('Action vector does not fit for the manipulators!')
            raise


class DiscreteActionHandler:
    def __init__(self):
        self._action_table = defaultdict(lambda: lambda: print("Unimplemented action!"))

    def sample(self, action_name):
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



from Environment import *

env = WoodCutterEnvironment()
wc = WoodCutter(env)

print(wc.interact({}))


"""