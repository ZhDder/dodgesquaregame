import torch
import numpy as np
import random
import collections

'''
Update 8/10/2025
- Changed the memory data structure from list to deque for a more efficient usage
- Changed the eps decay behaviour: Instead of lowering per frame, which is too much, it is now lowered per episode.
- Lowered eps_decay rate to 0.995 for a quicker decay as now it updates less often.
'''

class Agent(torch.nn.Module):

    def __init__(self, n_actions = 8, eps = 1.0, min_eps = 0.05, eps_decay = 0.995, memory_size = 1000):
        super(Agent, self).__init__()

        self.n_actions = n_actions #Number of possible actions: up, down, left, right, top_left, top_right, down_right, down_left = 8
        self.memory_size = memory_size
        self.step_count = 0
        self.target_update_frequency = 100  #Update target network every 100 steps

        #Epsilon-Greedy: For exploration(random action) and exploitation(best action)
        self.eps = eps
        self.min_eps = min_eps
        self.eps_decay = eps_decay

        #Store past experiences, check the 'remember' function.
        self.memory = collections.deque(maxlen=self.memory_size)

        #For Bellman's equation
        self.gamma = 0.95

        self.batch_size = 32
        
        self.q_network = torch.nn.Sequential(
                torch.nn.Linear(42, 128), #Input layer: (pos_x, pos_y, positions of maximum 20 enemies...)
                torch.nn.ReLU(),
                torch.nn.Dropout(0.2),
                torch.nn.Linear(128,64),
                torch.nn.ReLU(),
                torch.nn.Linear(64, n_actions) #Output layer: 8 possible positions: up, down, left, right, diagonals
        )

        self.target_network = torch.nn.Sequential(
                torch.nn.Linear(42, 128), #Input layer: (pos_x, pos_y, positions of maximum 20 enemies...)
                torch.nn.ReLU(),
                torch.nn.Dropout(0.2),
                torch.nn.Linear(128,64),
                torch.nn.ReLU(),
                torch.nn.Linear(64, n_actions) #Output layer: 8 possible positions: up, down, left, right, diagonals
        )

        # Copy weights to target network
        self.target_network.load_state_dict(self.q_network.state_dict())

        self.learning_rate = 0.0005
        self.optimizer = torch.optim.Adam(self.parameters(), lr=self.learning_rate)
        self.criterion = torch.nn.MSELoss()

    def forward(self, x):
        return self.q_network(x)
    
    def select_action(self, state):
        #Epsilon-Greedy
        if np.random.rand() < self.eps:
            #exploration
            action = np.random.randint(self.n_actions)
        else:
            #exploitation
            with torch.no_grad():
                q_vals = self.q_network(torch.tensor(state).unsqueeze(0).float())
                action = torch.argmax(q_vals).item()

        #eps decay
        
        return action
    
    def decay_epsilon(self):
        if self.eps > self.min_eps:
            self.eps *= self.eps_decay
    
    #Now, before the training loop, there's an important idea to mention. For each iteration, if we only consider the last action taken, its reward and other values, which all
    # together forms an 'experience', the training will likely not be as stable as if we consider some prior experiences too.
    # For this last idea, we need a way to store the experiences and include them (maybe not all) in the training loop. 

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self): #Usage of memories to train. 
        if len(self.memory) < self.batch_size: 
            return None
        #Not enough experiences gained, just keep moving

        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.from_numpy(np.array(states)).float()
        actions = torch.tensor(actions).int()
        rewards = torch.tensor(rewards).float()
        next_states = torch.from_numpy(np.array(next_states)).float()
        dones = torch.tensor(dones).float()

        q_vals = self.q_network(states)

        with torch.no_grad():
            next_q_vals = self.target_network(next_states)
            max_next_q = torch.max(next_q_vals, dim=1)[0]
        target_q = rewards + (self.gamma * max_next_q * (1 - dones))

        q_vals_for_actions = q_vals.gather(1, actions.long().unsqueeze(1)).squeeze()
        loss = self.criterion(q_vals_for_actions, target_q)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.step_count += 1
        if self.step_count > self.target_update_frequency:
            self.target_network.load_state_dict(self.q_network.state_dict())
            self.step_count = 0

        return loss.item()

