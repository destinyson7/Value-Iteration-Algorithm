def get_states():
    all_state = {}
    for health in range(5):
        for arrows in range(4):
            for stamina in range(3):
                state = str(health) + str(arrows) + str(stamina)
                all_state[state] = 0

    return all_state


transition_prob = {}
for health in range(5):
    for arrows in range(4):
        for stamina in range(3):

            state = str(health) + str(arrows) + str(stamina)
            transition_prob[state] = {"SHOOT": get_states(), "DODGE": get_states(), "RECHARGE": get_states()}

# print(transition_prob)
for health in range(5):
    for arrows in range(4):
        for stamina in range(3):

            state = str(health) + str(arrows) + str(stamina)
            # Recharge
            next_state1 = str(health) + str(arrows) + str(stamina)
            next_state2 = str(health) + str(arrows) + str(min(2, stamina + 1))
            transition_prob[state]["RECHARGE"][next_state1] += 0.2
            transition_prob[state]["RECHARGE"][next_state2] += 0.8

            # Dodge
            if(stamina == 0):
                continue
            next_state1 = str(health) + str(arrows) + str(max(stamina - 1, 0))
            next_state2 = str(health) + str(arrows) + str(max(stamina - 2, 0))
            next_state3 = str(health) + str(min(arrows + 1, 3)) + str(max(stamina - 1, 0))
            next_state4 = str(health) + str(min(arrows + 1, 3)) + str(max(stamina - 2, 0))
            transition_prob[state]["DODGE"][next_state1] += 0.16
            transition_prob[state]["DODGE"][next_state2] += 0.04
            transition_prob[state]["DODGE"][next_state3] += 0.64
            transition_prob[state]["DODGE"][next_state4] += 0.16

            # Shoot
            if(arrows == 0):
                continue
            next_state1 = str(max(health - 1, 0)) + str(max(arrows - 1, 0)) + str(max(stamina - 1, 0))
            next_state2 = str(max(health, 0)) + str(max(arrows - 1, 0)) + str(max(stamina - 1, 0))
            transition_prob[state]["SHOOT"][next_state1] += 0.5
            transition_prob[state]["SHOOT"][next_state2] += 0.5


# print(transition_prob)
