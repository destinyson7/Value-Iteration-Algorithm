from transition_prob import *

# print(transition_prob)

num_h = 2
num_a = 2
num_s = 2
gamma = 0.1
delta = 0.0000000001
reward = -2.5
terminal_reward = 10

actions = ["SHOOT", "DODGE", "RECHARGE"]


def value_iteration():
    utilities = {}

    for health in range(num_h):
        for arrows in range(num_a):
            for stamina in range(num_s):

                state = str(health) + str(arrows) + str(stamina)
                utilities[state] = 0

    iterations = 0

    while True:
        # new_utilities = utilities
        new_utilities = {}

        print("iteration=", iterations)

        for health in range(num_h):
            for arrows in range(num_a):
                for stamina in range(num_s):
                    cur_state = str(health) + str(arrows) + str(stamina)
                    if health == 0:
                        new_utilities[cur_state] = 0
                        continue
                    cur_max = -1000000000000

                    for action in actions:

                        if action == "SHOOT":
                            if stamina == 0 or arrows == 0:
                                continue

                        elif action == "DODGE" and stamina == 0:
                            continue

                        cur = reward
                        consider = False

                        for h in range(num_h):
                            for a in range(num_a):
                                for s in range(num_s):

                                    new_state = str(h) + str(a) + str(s)

                                    if transition_prob[cur_state][action][new_state] != 0:
                                        consider = True

                                    if h == 0 and transition_prob[cur_state][action][new_state] != 0:
                                        cur += terminal_reward
                                    cur += gamma * transition_prob[cur_state][action][new_state] * utilities[new_state]

                        if consider and cur_max < cur:
                            cur_max = cur

                    new_utilities[cur_state] = cur_max

        # print(utilities)
        # print()
        # print()
        # print(new_utilities)

        for health in range(1, num_h):
            for arrows in range(num_a):
                for stamina in range(num_s):

                    cur_state = str(health) + str(arrows) + str(stamina)

                    cur_max = -100000000000
                    cur_action = ""

                    for action in actions:

                        if action == "SHOOT":
                            if stamina == 0 or arrows == 0:
                                continue

                        elif action == "DODGE" and stamina == 0:
                            continue

                        cur = reward

                        consider = False

                        for h in range(num_h):
                            for a in range(num_a):
                                for s in range(num_s):
                                    new_state = str(h) + str(a) + str(s)

                                    if transition_prob[cur_state][action][new_state] != 0:
                                        consider = True

                                    if h == 0 and transition_prob[cur_state][action][new_state] != 0:
                                        cur += terminal_reward

                                    cur += gamma * transition_prob[cur_state][action][new_state] * new_utilities[new_state]

                        # print(cur, cur_max)
                        if consider and cur_max < cur:
                            cur_max = cur
                            cur_action = action

                    print(cur_state, cur_action, new_utilities[cur_state])

        converged = True

        for i in utilities:
            if abs(new_utilities[i] - utilities[i]) > delta:
                converged = False
                break

        if converged:
            break

        utilities = new_utilities
        iterations += 1
        print()
        print()


value_iteration()
