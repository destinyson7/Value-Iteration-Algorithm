import numpy as np

num_h = 5
num_a = 4
num_s = 3

states = np.array([(health, arrows, stamina) for health in range(num_h)
                   for arrows in range(num_a)
                   for stamina in range(num_s)])


def get_states():
    all_state = {}
    for health, arrows, stamina in states:
        all_state[tuple([health, arrows, stamina])] = 0

    return all_state


transition_prob = {}

for health, arrows, stamina in states:
    transition_prob[tuple([health, arrows, stamina])] = {"SHOOT": get_states(), "DODGE": get_states(), "RECHARGE": get_states()}


for health, arrows, stamina in states:
    state = tuple([health, arrows, stamina])

    # RECHARGE

    next_state1 = tuple([health, arrows, stamina])
    next_state2 = tuple([health, arrows, min(num_s - 1, stamina + 1)])

    transition_prob[state]["RECHARGE"][next_state1] += 0.2
    transition_prob[state]["RECHARGE"][next_state2] += 0.8

    # DODGE

    if(stamina == 0):
        continue

    next_state1 = tuple([health, arrows, max(stamina - 1, 0)])
    next_state2 = tuple([health, arrows, max(stamina - 2, 0)])
    next_state3 = tuple([health, min(arrows + 1, num_a - 1), max(stamina - 1, 0)])
    next_state4 = tuple([health, min(arrows + 1, num_a - 1), max(stamina - 2, 0)])

    transition_prob[state]["DODGE"][next_state1] += 0.16
    transition_prob[state]["DODGE"][next_state2] += 0.04
    transition_prob[state]["DODGE"][next_state3] += 0.64
    transition_prob[state]["DODGE"][next_state4] += 0.16

    # SHOOT

    if(arrows == 0):
        continue

    next_state1 = tuple([max(health - 1, 0), max(arrows - 1, 0), max(stamina - 1, 0)])
    next_state2 = tuple([max(health, 0), max(arrows - 1, 0), max(stamina - 1, 0)])

    transition_prob[state]["SHOOT"][next_state1] += 0.5
    transition_prob[state]["SHOOT"][next_state2] += 0.5


# print(transition_prob)
