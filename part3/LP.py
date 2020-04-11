class LinearProgram:

	def initialize_states(self):
		for enemy_health in range(5):
			for number_of_arrows in range(4):
				for stamina in range(3):
					self.states.append((enemy_health, number_of_arrows, stamina))		
	
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
				if stamina > 0 and number_of_arrows < 3:
					cur_possible_actions.append(self.actions["DODGE"])
				if stamina < 2:
					cur_possible_actions.append(self.actions["RECHARGE"])
			cur_possible_actions.sort()
			self.possible_actions[cur_state] = cur_possible_actions

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
				return 1
			elif action == "RECHARGE":
				return 0.8
			elif action == "DODGE":
				return 1
			elif action == "SHOOT":
				return 1
		else:
			if action == "NOOP":
				return 0
			elif action == "RECHARGE":
				if final_number_of_arrows == initial_number_of_arrows and final_stamina == initial_stamina + 1 and final_enemy_health == initial_enemy_health:
					return -0.8
				else:
					return 0
			elif action == "DODGE":
				if initial_stamina == 2:
					if final_number_of_arrows == initial_number_of_arrows and (final_stamina == initial_stamina - 1 or final_stamina == initial_stamina - 2) and final_enemy_health == initial_enemy_health:
						return -0.1
					elif final_number_of_arrows == initial_number_of_arrows + 1 and (final_stamina == initial_stamina - 1 or final_stamina == initial_stamina - 2) and final_enemy_health == initial_enemy_health:
						return -0.4
					else:
						return 0
				else:
					if (final_number_of_arrows == initial_number_of_arrows or final_number_of_arrows == initial_number_of_arrows + 1) and (final_stamina == initial_stamina - 1) and final_enemy_health == initial_enemy_health:
						return -0.5
					else:
						return 0
			elif action == "SHOOT":
				if final_number_of_arrows == initial_number_of_arrows - 1 and final_stamina == initial_stamina - 1 and final_enemy_health == initial_enemy_health:
					return -0.5
				elif final_number_of_arrows == initial_number_of_arrows - 1 and final_stamina == initial_stamina - 1 and final_enemy_health == initial_enemy_health - 1:
					return -0.5
				else:
					return 0

	def initialize_Amatrix(self):
		for final_state in self.states:
			cur_list = []
			for initial_state in self.states:
				for action in self.possible_actions[initial_state]:
					cur_list.append(self.flow(initial_state, final_state, action))
			self.A.append(cur_list);

	def initialize_reward(self):
		for cur_state in self.states:
			for action in self.possible_actions[cur_state]:
				enemy_health = cur_state[0]
				if enemy_health == 0:
					self.reward.append(0)
				else:
					self.reward.append(self.penalty)


	def __init__(self):
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

linearProgram = LinearProgram()
linearProgram.initialize_states()
linearProgram.initialize_possible_actions()
linearProgram.initialize_Amatrix()
linearProgram.initialize_reward()
print(linearProgram.reward)
