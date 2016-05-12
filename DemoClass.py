from Policy import *
from Architecture import *
from Environment import *
from TrainingFunction import *


class RLAgent:

    def __init__(self, environment, architecture, knowledge):  # reward?
        self.environment = environment
        self.architecture = architecture
        self.agent_function = AgentFunction(knowledge)

    @staticmethod
    def perf_check(items, n):
        if n > len(items):
            return sum(items) / len(items)
        else:
            return sum(items[-n:]) / n

    def train(self, policy, learning_function, iteration_limit):
        # these can be set for a single training session
        self.agent_function.policy = policy
        self.agent_function.training_method = learning_function

        observation = self.architecture.initial_state()

        lap_start = 0
        performance_target = 0
        laps = []

        for i in range(0, iteration_limit):
            # this is a list of dicts
            actions = self.architecture.get_actions()  # a set of possible actions (vectors)
            action = self.agent_function.evaluate(observation, actions)

            (observation, reward) = self.architecture.interact(action)

            if reward > 0:
                lap_time = i - lap_start
                laps.append(lap_time)
                print(str(RLAgent.perf_check(laps, 100)))
                lap_start = i + 1
                if lap_time < 25:
                    performance_target += 1

            self.agent_function.improve(reward)

        print("Performance target was hit in " + str(performance_target) + " times.")

        return self.agent_function

env = Maze()
arch = MazeMan(env)
agent = RLAgent(env, arch, Table())

agent.train(EpsilonGreedy(epsilon=0.1, regression=0.3), QLearn(learning_rate=0.3, discount_factor=0.99), 30000)
