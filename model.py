# Referenced from Patrick Loeber aka. Python Engineer, https://github.com/python-engineer/snake-ai-pytorch/blob/main/model.py
# Submitted on: Wednesday, April 21, 2021
# Course Code: ICS 3U0-C, Introduction to Computer Science
# Teacher: Mr. Le
# This model was referenced from somewhere else due to its complexity and of the advanced AI concepts required for the AI to work.
# This entire file was practically referenced from the link above, and as such I wish for it to not be included in the marking of the project.
# The model contains two classes, one base class for forward propagation, and one for the actual trainer that uses tensors.

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Linear_QNet(nn.Module): # This is the base class for all neural networks, and contains the layers of the network.
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.first_linear_layer = nn.Linear(input_size, hidden_size) # The first linear layer contains the input layer and the hidden layer.
        self.second_linear_layer = nn.Linear(hidden_size, output_size) # The second linear layer contains the hidden layer and the output layer.
        
    def forward(self, x): # This function acts as the forward propagation through the network
        x = F.relu(self.first_linear_layer(x))
        x = self.second_linear_layer(x)
        return x
    
    def save(self, file_name='model.pth'): # This helper function saves the model in its current state for later use.
        model_folder_path = './model'
        if not os.path.exists(model_folder_path): # Creates a new directory called model_folder_path
            os.makedirs(model_folder_path)
            
        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name) # Saves the model as a dictionary in the file provided above.

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr # Stores the learning rate
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss() # Implements Mean Squared Error as the Loss Function
    
    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float) # Converts 4 of the 5 inputs into tensors
        
        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0) # Forces an extra dimension into the tensors if the length of any of the inputs is 1.
            done = (done, )
        
        pred = self.model(state) # Predicts the current Q values using the current state of the environment.
        
        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]: # This calculates the new Q values using the Bellman Equation.
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))
                
            target[idx][torch.argmax(action[idx]).item()] = Q_new
            
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward() # Applies backwards propagation through the network
        
        self.optimizer.step()
