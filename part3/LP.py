import numpy as np
import sys
import cvxpy as cp

class LinearProgram:

    def __init__(self):
        self.MAX_ENEMY_HEALTH = 4
        self.MAX_ARROWS = 3
        self.MAX_STAMINA = 2

        self.order_of_states = ["enemy_health", "number_of_arrows", "stamina"]

        self.actions = {
            "NOOP": 0,
            "RECHARGE": 1,
            "DODGE": 2,
            "SHOOT": 3
        }

        self.convert_back = {
            0: "NOOP",
            1: "RECHARGE",
            2: "DODGE",
            3: "SHOOT"
        }

        self.states = []
        self.A = []
        self.reward = []
        self.possible_actions = {}
        self.penalty = -10
        self.alpha = []
        self.total_actions = 0

        self.initialize_states()
        self.initialize_possible_actions()
        self.initialize_Amatrix()
        self.initialize_reward()
        self.initialize_alpha()

    def initialize_states(self):
        self.states = [(enemy_health, number_of_arrows, stamina) for enemy_health in range(
            self.MAX_ENEMY_HEALTH + 1) for number_of_arrows in range(self.MAX_ARROWS + 1) for stamina in range(self.MAX_STAMINA + 1)]

    def initialize_possible_actions(self):
        for cur_state in self.states:
            enemy_health = cur_state[0]
            number_of_arrows = cur_state[1]
            stamina = cur_state[2]
            cur_possible_actions = []
            if enemy_health == 0:
                cur_possible_actions.append(self.actions["NOOP"])
            else:
                if number_of_arrows > 0 and stamina > 0:
                    cur_possible_actions.append(self.actions["SHOOT"])
                if stamina > 0:
                    cur_possible_actions.append(self.actions["DODGE"])
                if stamina < self.MAX_STAMINA:
                    cur_possible_actions.append(self.actions["RECHARGE"])
            cur_possible_actions.sort()
            self.possible_actions[cur_state] = cur_possible_actions
            self.total_actions += len(cur_possible_actions)

    def flow(self, initial_state, final_state, action):
        initial_enemy_health = initial_state[0]
        initial_number_of_arrows = initial_state[1]
        initial_stamina = initial_state[2]

        final_enemy_health = final_state[0]
        final_number_of_arrows = final_state[1]
        final_stamina = final_state[2]

        action = self.convert_back[action]

        if initial_state == final_state:

            if action == "NOOP":
                return 1.0

            elif action == "RECHARGE":
                return 0.8

            elif action == "DODGE":
                return 1.0

            elif action == "SHOOT":
                return 1.0

        else:

            if action == "NOOP":
                return 0.0

            elif action == "RECHARGE":

                if final_number_of_arrows == initial_number_of_arrows and final_stamina == initial_stamina + 1 and final_enemy_health == initial_enemy_health:
                    return -0.8

                else:
                    return 0.0

            elif action == "DODGE":

                if initial_stamina == self.MAX_STAMINA:

                    if final_number_of_arrows == self.MAX_ARROWS and initial_number_of_arrows == self.MAX_ARROWS and final_stamina == initial_stamina - 1 and final_enemy_health == initial_enemy_health:
                        return -0.8

                    elif final_number_of_arrows == self.MAX_ARROWS and initial_number_of_arrows == self.MAX_ARROWS and final_stamina == initial_stamina - 2 and final_enemy_health == initial_enemy_health:
                        return -0.2

                    elif final_number_of_arrows == initial_number_of_arrows and final_enemy_health == initial_enemy_health:
                        if final_stamina == initial_stamina - 1:
                            return -0.16

                        elif final_stamina == initial_stamina - 2:
                            return -0.04

                        else:
                            return 0.0

                    elif final_number_of_arrows == initial_number_of_arrows + 1 and final_enemy_health == initial_enemy_health:
                        if final_stamina == initial_stamina - 1:
                            return -0.64

                        elif final_stamina == initial_stamina - 2:
                            return -0.16

                        else:
                            return 0.0

                    else:
                        return 0.0

                else:

                    if final_number_of_arrows == self.MAX_ARROWS and initial_number_of_arrows == self.MAX_ARROWS and final_stamina == initial_stamina - 1 and final_enemy_health == initial_enemy_health:
                        return -1

                    elif (final_number_of_arrows == initial_number_of_arrows or final_number_of_arrows == initial_number_of_arrows + 1) and (final_stamina == initial_stamina - 1) and final_enemy_health == initial_enemy_health:
                        return -0.5

                    else:
                        return 0.0

            elif action == "SHOOT":

                if final_number_of_arrows == initial_number_of_arrows - 1 and final_stamina == initial_stamina - 1 and final_enemy_health == initial_enemy_health:
                    return -0.5

                elif final_number_of_arrows == initial_number_of_arrows - 1 and final_stamina == initial_stamina - 1 and final_enemy_health == initial_enemy_health - 1:
                    return -0.5

                else:
                    return 0.0

    def initialize_Amatrix(self):
        for final_state in self.states:
            cur_list = []
            for initial_state in self.states:
                for action in self.possible_actions[initial_state]:
                    cur_list.append(
                        self.flow(initial_state, final_state, action))
            cur_list = np.array(cur_list)
            self.A.append(cur_list)

        self.A = np.array(self.A)

    def initialize_reward(self):
        for cur_state in self.states:
            for action in self.possible_actions[cur_state]:
                enemy_health = cur_state[0]
                if enemy_health == 0:
                    self.reward.append(0)
                else:
                    self.reward.append(self.penalty)

        self.reward = np.array(self.reward)

    def initialize_alpha(self):
        for cur_state in self.states:
            health = cur_state[0]
            arrows = cur_state[1]
            stamina = cur_state[2]

            if health == self.MAX_ENEMY_HEALTH and arrows == self.MAX_ARROWS and stamina == self.MAX_STAMINA:
                self.alpha.append(1.0)
            else:
                self.alpha.append(0.0)
        self.alpha = np.array(self.alpha)
        self.alpha = np.expand_dims(self.alpha, axis=1)

    def solve(self):
        x = cp.Variable(shape = (self.total_actions, 1), name = 'x')
        # print(self.alpha.shape)
        print(cp.matmul(self.A, x))
        constraints = [cp.matmul(self.A, x) == self.alpha]
        objective = cp.Maximize(cp.matmul(self.reward, x))
        problem = cp.Problem(objective, constraints)

        solution = problem.solve()
        print(solution)

        print(x.value)


linearProgram = LinearProgram()
opt = np.get_printoptions()
np.set_printoptions(threshold=sys.maxsize)
print(linearProgram.A)
np.set_printoptions(**opt)
print()
print(np.sum(np.sum(linearProgram.A, 0)))
# print(linearProgram.total_actions)
linearProgram.solve()
