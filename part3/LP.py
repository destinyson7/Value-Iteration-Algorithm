class LinearProgram:
	def initialize_states(self):
		for enemy_health in range(5):
			for number_of_arrows in range(4):
				for stamina in range(3):
					self.states.append([enemy_health, number_of_arrows, stamina])				
	
	def initialize_possible_states(self):
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
			self.possible_actions.append(cur_possible_actions)

	def __init__(self):
		self.order_of_states = ["enemy_health", "number_of_arrows", "stamina"]
		self.actions = {
			"NOOP": 0,
			"RECHARGE": 1,
			"DODGE": 2,
			"SHOOT": 3
		}
		self.states = []
		self.A = []
		self.possible_actions = []

linearProgram = LinearProgram()
linearProgram.initialize_states()
linearProgram.initialize_possible_states()
print(linearProgram.possible_actions)
