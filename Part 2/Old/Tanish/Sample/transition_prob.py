num_h = 2
num_a = 2
num_s = 2


def get_states():
    all_state = {}
    for health in range(num_h):
        for arrows in range(num_a):
            for stamina in range(num_s):
                state = str(health) + str(arrows) + str(stamina)
                all_state[state] = 0

    return all_state


transition_prob = {}
for health in range(num_h):
    for arrows in range(num_a):
        for stamina in range(num_s):

            state = str(health) + str(arrows) + str(stamina)
            transition_prob[state] = {"SHOOT": get_states(), "DODGE": get_states(), "RECHARGE": get_states()}

# print(transition_prob)
for health in range(num_h):
    for arrows in range(num_a):
        for stamina in range(num_s):

            state = str(health) + str(arrows) + str(stamina)
            # Recharge
            next_state2 = str(health) + str(arrows) + str(min(1, stamina + 1))
            transition_prob[state]["RECHARGE"][next_state2] += 1

            # Dodge
            if(stamina == 0):
                continue
            next_state1 = str(health) + str(arrows) + str(max(stamina - 1, 0))
            next_state2 = str(health) + str(arrows) + str(max(stamina - 2, 0))
            transition_prob[state]["DODGE"][next_state1] += 0.8
            transition_prob[state]["DODGE"][next_state2] += 0.2

            # Shoot
            if(arrows == 0):
                continue
            next_state1 = str(max(health - 1, 0)) + str(max(arrows - 1, 0)) + str(max(stamina - 1, 0))
            next_state2 = str(max(health, 0)) + str(max(arrows - 1, 0)) + str(max(stamina - 1, 0))
            transition_prob[state]["SHOOT"][next_state1] += 0.5
            transition_prob[state]["SHOOT"][next_state2] += 0.5

# print(transition_prob)
