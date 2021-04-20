# Author: Andy Ganea, with reference from Patrick Loeber aka. Python Engineer, https://github.com/python-engineer/snake-ai-pytorch/blob/main/agent.py
# Submitted on: Wednesday, April 21, 2021
# Course Code: ICS 3U0-C, Introduction to Computer Science
# Teacher: Mr. Le
# This is a modified version of the agent program by Python Engineer, which I've borrowed the model and helper from. This modified version uses by own snake environment, much different than the one used by Patrick Loeber.
# The main changes are the get_state() function in class Agent, and the train_agent() function in the main file, and the get_action() function in class Agent.
# As such, these are the functions that I would like to be assessed on for this file, as the others have been borrowed.


import torch
import random
import numpy as np
from collections import deque # custom data structure; an extremely optimized list for storing AI memory 
from game_ai_player import AI_GAME, APPLE, Asset # Imports the main game, assets, and apple class from the environment file.
from model import Linear_QNet, QTrainer
from helper import plot
import pygame

# Parameter List
MAXIMUM_MEMORY = 100_000 # 100,000 items can be stored in the custom deque memory structure
MAXIMUM_BATCH_SIZE = 1000
LEARNING_RATE = 0.001 # Learning rate, which is a hyperparameter used to dictate how much change the model occurs between each step.

class Agent: # This class contains the agent that plays the agent-controlled game, and the necessary functions to get the snake's game state and to move the snake accordingly without player input.
    
    def __init__(self):
        self.games_played = 0 # Tracks how many games the AI has played.
        self.switch_to_long_term_memory_counter = 0 # Parameter to control the randomness
        self.gamma = 0.9 # Parameter discount rate (must be smaller than 1) as per the deep learning equation.
        self.memory = deque(maxlen=MAXIMUM_MEMORY) # deque memory limited to MAX_SIZE and it automatically removes memory if it overflows
        self.model = Linear_QNet(11, 256, 3) # 11 is the input size, 256 is the hidden size, and 3 is the output size
        self.trainer = QTrainer(self.model, lr=LEARNING_RATE, gamma=self.gamma)
    
    def get_state(self, game):
        snake_head = game.snake.body[0]
        # These points need to be calculated all around the snake head to sense if it will die if it moves in a certain direction.
        point_left = snake_head + pygame.math.Vector2(-1, 0)
        point_right = snake_head + pygame.math.Vector2(1, 0)
        point_up = snake_head + pygame.math.Vector2(0, -1)
        point_down = snake_head + pygame.math.Vector2(0, 1)
        
        # These four boolean values check which direction the snake is currently moving in.
        moving_left = game.snake.direction.x == -1
        moving_right = game.snake.direction.x == 1
        moving_up = game.snake.direction.y == -1
        moving_down = game.snake.direction.y == 1
        
        state = [ # The state is a list of 11 boolean elements, and is what the model takes in to predict the next move.
            # If any of these conditions are True, there is a danger straight ahead.
            (moving_right and game.check_fail_condition_point(point_right)) or
            (moving_left and game.check_fail_condition_point(point_left)) or
            (moving_up and game.check_fail_condition_point(point_up)) or
            (moving_down and game.check_fail_condition_point(point_down)),
            
            # If any of these conditions are True, there is a danger to the square relatively to the right of the snake head.
            (moving_up and game.check_fail_condition_point(point_right)) or
            (moving_down and game.check_fail_condition_point(point_left)) or
            (moving_left and game.check_fail_condition_point(point_up)) or
            (moving_right and game.check_fail_condition_point(point_down)),
            
            # If any of these conditions are True, there is a danger to the square relatively to the left of the snake head.
            (moving_down and game.check_fail_condition_point(point_right)) or
            (moving_up and game.check_fail_condition_point(point_left)) or
            (moving_right and game.check_fail_condition_point(point_up)) or
            (moving_left and game.check_fail_condition_point(point_down)),
            
            # Only one of these conditions will be 1 in the list, and that tells the agent what direction the snake is currently 
            moving_left,
            moving_right,
            moving_down,
            moving_up,
            
            # This is similar to the previous four members of the list, but this time multiple can be 1, since if the food is down and right from the snake head, the end of the list is [0, 1, 0, 1]
            game.apple.x < game.snake.body[0].x, # There is a piece of food to the left of the head
            game.apple.x > game.snake.body[0].x, # There is a piece of food to the left of the head
            game.apple.y < game.snake.body[0].y, # There is a piece of food above the head
            game.apple.y > game.snake.body[0].y # There is a piece of food below the head
            ]
        
        return np.array(state, dtype=int) # This converts the entire list, which contains True or False booleans, to just 0s or 1s.
    
    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over)) # Appends all of this information to the deque defined at the beginning
    
    def train_long_memory(self):
        if len(self.memory) > MAXIMUM_BATCH_SIZE :
            long_term_memory_sample = random.sample(self.memory, MAXIMUM_BATCH_SIZE ) # Since each element in the snake's memory is stored as a tuple, this random sampling returns a list of tuples.
        else:
            long_term_memory_sample = self.memory
        
        states, actions, rewards, next_states, game_overs = zip(*long_term_memory_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)
    
    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)
    
    def get_action(self, state):
        self.switch_to_long_term_memory_counter = 80 - self.games_played # This is just a subtracting constant that determines when the snake goes from moving randomly to moving based on the model.
        current_move = [0,0,0]
        if random.randint(0, 200) < self.switch_to_long_term_memory_counter: # As the number of games gets smaller, this condition is less and less likely to be true, so it will eventually switch over to the model.
            move_index = random.randint(0, 2) # This just makes the move either randomly straight, left, or right with no logic behind it.
            current_move[move_index] = 1
        else:
            current_model_state = torch.tensor(state, dtype=torch.float)
            prediction = self.model(current_model_state)
            move_index = torch.argmax(prediction).item()
            current_move[move_index] = 1
        
        return current_move
        
def train_agent():
    plot_scores = [] # List to plot the scores
    plot_mean_scores = [] # List to plot the mean scores
    total_score = 0 # Initializes the total score that the snake will achieve per game.
    new_record = 0 # Initializes the best score the snake has achieved so far.
    agent = Agent() # An object from the Agent class needs to be initialized in the main agent loop.
    game = AI_GAME() # The game from the environment also needs to be initialized.
    while True:
        # Get the current state of the game.
        state_old = agent.get_state(game)
        
        # Get the action that should be executed at this state of the game.
        current_move = agent.get_action(state_old)
        
        # This actually moves the snake on the screen, and takes in the state right after the move/
        reward, game_over, score = game.play_step(current_move)
        state_new = agent.get_state(game)

        # Trains short memory using the self.trainer method defined above.
        agent.train_short_memory(state_old, current_move, reward, state_new, game_over)
        
        # The snake also needs to remember these states in the deque to actually learn over generations.
        agent.remember(state_old, current_move, reward, state_new, game_over)
        
        if game_over: # This if statement runs whenever the agent-controlled snake dies, and contains the logic of making constantly growing generations.
            game.reset_game_assets()
            agent.games_played += 1
            agent.train_long_memory() # After each death, the snake not only needs to remember what happened after each move, but the strategies it used that do work and that don't work.
            
            if score > new_record: # If the snake gets a new high score, this needs to be saved in the model.
                new_record = score
                agent.model.save()
            
            plot_scores.append(score) # Appends the score to a list called scores for plotting
            total_score += score
            mean_score = total_score / agent.games_played # Calculates the average score over all of the games played
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores) # Calls the plot function and actually plots out the two values


if __name__ == '__main__': # This train function will run if and only if agent.py is the file running, so the user doesn't accidently break the program by running the other files.
    train_agent()
    