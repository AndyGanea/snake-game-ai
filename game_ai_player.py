# Author: Andrew Nicholas Ganea aka. (Andy Ganea)
# Submitted on: Wednesday, April 21, 2021
# Course Code: ICS 3U0-C, Introduction to Computer Science
# Teacher: Mr. Le
# This program is the environment that the AI uses to play the game. The file has been modified as it no longer has human player input.
# The game has been stripped down a few levels for the AI, as it has been sped up, with no main menu, and no swap fruit button.
# Other than that, most of the functions and classes are borrowed from the human player game, but the move function has been changed to get an input from the agent.
# The program finally returns the score, the game over state, and a custom reward for the agent at the end as well.

import pygame, sys, random, time, os
from pygame.math import Vector2 # This import is to directly use Vector2 for creating vectors.
import numpy as np
from enum import Enum # to hold the constants in the Asset class; 

class Asset(Enum):
    
    ## This constant stores the folder of the program in a variable to be called on in the rest of the class.
    FILEDIR = os.path.dirname(os.path.realpath('__file__'))

    # These constants are the exact location of the possible head PNGs on the user's computer, stored in lists.
    HEADU_PNG = os.path.join(FILEDIR, 'Graphics/head_u.png')
    HEADD_PNG = os.path.join(FILEDIR, 'Graphics/head_d.png')
    HEADR_PNG = os.path.join(FILEDIR, 'Graphics/head_r.png')
    HEADL_PNG = os.path.join(FILEDIR, 'Graphics/head_l.png')

    # Filepaths for the images that make up the tail of the snake.
    TAILU_PNG = os.path.join(FILEDIR, 'Graphics/tail_u.png')
    TAILD_PNG = os.path.join(FILEDIR, 'Graphics/tail_d.png')
    TAILR_PNG = os.path.join(FILEDIR, 'Graphics/tail_r.png')
    TAILL_PNG = os.path.join(FILEDIR, 'Graphics/tail_l.png')

    # Filepaths for the images that make up the body of the snake.
    BODYV_PNG = os.path.join(FILEDIR, 'Graphics/body_v.png')
    BODYH_PNG = os.path.join(FILEDIR, 'Graphics/body_h.png')
    BODYTR_PNG = os.path.join(FILEDIR, 'Graphics/body_tr.png')
    BODYTL_PNG = os.path.join(FILEDIR, 'Graphics/body_tl.png')
    BODYBR_PNG = os.path.join(FILEDIR, 'Graphics/body_br.png')
    BODYBL_PNG = os.path.join(FILEDIR, 'Graphics/body_bl.png')

    # Filepaths for the sounds played during the game.
    EAT_WAV = os.path.join(FILEDIR, 'Sounds/eat.wav')
    GAMEOVER_WAV = os.path.join(FILEDIR, 'Sounds/gameover.wav')

    # Filepaths for the image of the fruits
    APPLE_PNG = os.path.join(FILEDIR, 'Graphics/apple.png')
    
    # Filepath for the font used.
    FONTS = os.path.join(FILEDIR, 'Fonts/ProductSans.ttf')
    
    # Various string values
    APPLE_GET_MSG = "Apple Get!"
    FINAL_SCORE_MSG = "Your final score is: "
    THX_FOR_PLAYING_MSG = "Thanks for playing!"
    SET_CAPTION = "Andy Ganea's Snake Game | AI Player Variant"
    
    # Grid Sizes
    GRID_UNIT_NUMBER = 20 # This value determines how many squares make up the grid seen on screen.
    GRID_UNIT_SIZE = 40 # This value determines how wide and tall each square of the grid is, in pixels.
    
class SNAKE:
    def __init__(self, gameScreen): # Initializes the snake and its body segment positions.
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)] # Creates the snakes body by specifying three consecutive vectors on the grid.
        self.direction = Vector2(1, 0) # The starting direction for the snake is set to right in this line.
        self.new_body_segment = False

        # Imports graphics for the head of the snake in all 4 directions.
        self.head_u = pygame.image.load(Asset.HEADU_PNG.value).convert_alpha()
        self.head_d = pygame.image.load(Asset.HEADD_PNG.value).convert_alpha()
        self.head_r = pygame.image.load(Asset.HEADR_PNG.value).convert_alpha()
        self.head_l = pygame.image.load(Asset.HEADL_PNG.value).convert_alpha()

        # Imports graphics for the tail of the snake in all 4 directions.
        self.tail_u = pygame.image.load(Asset.TAILU_PNG.value).convert_alpha()
        self.tail_d = pygame.image.load(Asset.TAILD_PNG.value).convert_alpha()
        self.tail_r = pygame.image.load(Asset.TAILR_PNG.value).convert_alpha()
        self.tail_l = pygame.image.load(Asset.TAILL_PNG.value).convert_alpha()

        # Imports graphics for the main straight body segments, which can either face up and down or side to side.
        self.body_v = pygame.image.load(Asset.BODYV_PNG.value).convert_alpha()
        self.body_h = pygame.image.load(Asset.BODYH_PNG.value).convert_alpha()

        # Imports all of the body pieces that display whenever the snake makes a turn in any direction.
        self.body_tr = pygame.image.load(Asset.BODYTR_PNG.value).convert_alpha()
        self.body_tl = pygame.image.load(Asset.BODYTL_PNG.value).convert_alpha()
        self.body_br = pygame.image.load(Asset.BODYBR_PNG.value).convert_alpha()
        self.body_bl = pygame.image.load(Asset.BODYBL_PNG.value).convert_alpha()
        
        # Imports all of the sounds to be used throughout the game.
        self.eating_sound = pygame.mixer.Sound(Asset.EAT_WAV.value)
        self.death_sound = pygame.mixer.Sound(Asset.GAMEOVER_WAV.value)

        
    def draw_snake(self, gameScreen): # This function is reponsible for drawing out the rectangles that make up the snake body.
        self.update_head_graphics() # This is called to retrieve the correct head graphic before drawing it out.
        self.update_tail_graphics() # This is called to retrieve the correct tail graphic before drawing it out.
        
        for index, counter in enumerate(self.body): # This for loop cycles through the vectors stored in the self.body list and draws them all out.
            snakeXPos = int(counter.x * Asset.GRID_UNIT_SIZE.value)
            snakeYPos = int(counter.y * Asset.GRID_UNIT_SIZE.value) # This takes in the x and y position of the vector, multiplies by the grid multiplier, and sets them to new variables.
            snakeRectangle = pygame.Rect(snakeXPos, snakeYPos, Asset.GRID_UNIT_SIZE.value, Asset.GRID_UNIT_SIZE.value) # Defines the snake rectangle and gets called on as many times as there are members in the vector list.
            
            if index == 0: # This checks if the index of the body list is the first element, if so check which head graphics to display.
                gameScreen.blit(self.head, snakeRectangle) # self.head is the updating flag that comes from the next function.
            elif index == len(self.body) - 1: # Check if the index is on the tail element, which is the length of the list minus 1, as it starts counting at 0.
                gameScreen.blit(self.tail, snakeRectangle)
            else: # The else is responsible for all the body segments, as they are neither the head nor the tail.
                previous_segment = self.body[index + 1] - counter
                next_segment = self.body[index - 1] - counter # These two lines use indexing to generate a new vector based on the position of the segment behind and in front any body segment.
                if previous_segment.x == next_segment.x: # If the segment before and after a body segment have the same x-coordinate, the snake must be facing vertically.
                    gameScreen.blit(self.body_v, snakeRectangle)
                elif previous_segment.y == next_segment.y: # If the segment before and after a body segment have the same y-coordinate, the snake must be facing horizontally.
                    gameScreen.blit(self.body_h, snakeRectangle)
                else: # This final else draws out the four corner segments of the snake's body
                    if previous_segment.x == -1 and next_segment.y == -1 or previous_segment.y == -1 and next_segment.x == -1: # This checks if there is a block to the left and upwards of any given body segment, and displays the corner piece.
                        gameScreen.blit(self.body_tl, snakeRectangle)
                    if previous_segment.x == -1 and next_segment.y == 1 or previous_segment.y == 1 and next_segment.x == -1: # This checks if there is a block to the left and downwards of any given body segment, and displays the corner piece.
                        gameScreen.blit(self.body_bl, snakeRectangle)
                    if previous_segment.x == 1 and next_segment.y == -1 or previous_segment.y == -1 and next_segment.x == 1: # This checks if there is a block to the right and upwards of any given body segment, and displays the corner piece.
                        gameScreen.blit(self.body_tr, snakeRectangle)
                    if previous_segment.x == 1 and next_segment.y == 1 or previous_segment.y == 1 and next_segment.x == 1: # This checks if there is a block to the right and downwards of any given body segment, and displays the corner piece.
                        gameScreen.blit(self.body_br, snakeRectangle)

    def update_head_graphics(self): # This function determines which way the head of the snake is facing, and calls on the correct flag to draw out in the previous function.
        current_head_direction = self.body[1] - self.body[0] # This line performs vector subtraction on the head and the 1st body segment, resulting in one of 4 vectors.
        # This chain of if statements checks each difference, and then determines what self.head should be.
        if current_head_direction == Vector2(1, 0):
            self.head = self.head_l
        elif current_head_direction == Vector2(-1, 0):
            self.head = self.head_r
        elif current_head_direction == Vector2(0, 1):
            self.head = self.head_u
        else:
            self.head = self.head_d
    
    def update_tail_graphics(self): # This function determines which way the tail is facing, and calls on the appropriate graphic to be displayed.
        current_tail_direction = self.body[-2] - self.body[-1] # This line performs vector subtraction on the last and second last segments, resulting in one of 4 vectors.
        # This chain of if statements checks each difference, and then determines what self.head should be.
        if current_tail_direction == Vector2(1, 0):
            self.tail = self.tail_l
        elif current_tail_direction == Vector2(-1, 0):
            self.tail = self.tail_r
        elif current_tail_direction == Vector2(0, 1):
            self.tail = self.tail_u
        else:
            self.tail = self.tail_d

    def move_snake(self): # When the snake moves every cycle, it can either move or grow by one if it is on an apple.
        if self.new_body_segment == True:
            snakeBodyCopy = self.body[:] # Creates a copy of the body segment list without the last element included.
            snakeBodyCopy.insert(0, snakeBodyCopy[0] + self.direction) # This adds a vector to the front of the list, in the direction the user inputted.
            self.body = snakeBodyCopy[:] 
            self.new_body_segment = False # This flag has to be reverted because it should only be true when the snake head is directly on the fruit.
        else:
            snakeBodyCopy = self.body[:-1] # Creates a copy of the body segment list without the last element included.
            snakeBodyCopy.insert(0, snakeBodyCopy[0] + self.direction) # This adds a vector to the front of the list, in the direction the user inputted.
            self.body = snakeBodyCopy[:] # This puts the new list back into the snake body to be re-displayed.
    
    def insert_new_segment(self):
        self.new_body_segment = True # This flag is only set to True when the snake collides with the apple.
    
    def play_eating_sound(self): # This function allows the eating sounds to be called as a function in the main class.
        self.eating_sound.play()
    
    def play_death_sound(self):
        self.death_sound.play()

class APPLE: # This class is the apple object itself, and contains all of its parameters and functions.
    def __init__(self): # This intializes the attributes of the fruit object, which is its position.
        self.random_fruit_position()
    
    def random_fruit_position(self): # This function basically randomizes the position of the fruit, which runs every time the condition in the main loop happens.
        self.x = random.randint(0, Asset.GRID_UNIT_NUMBER.value - 1)
        self.y = random.randint(0, Asset.GRID_UNIT_NUMBER.value - 1) # These lines place the fruit down on a random grid square position.
        self.coords = Vector2(self.x, self.y) # Converts the two coordinates into a vector for easier use.

class AI_GAME:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512) # Uses these values to make the sound sync up with the actions.
        pygame.init() # Initalizes pygame, and makes it ready to use later.
        pygame.display.set_caption(Asset.SET_CAPTION.value) # Sets the title of the window to the specified text
        
        self.gameScreen = pygame.display.set_mode((Asset.GRID_UNIT_NUMBER.value * Asset.GRID_UNIT_SIZE.value, Asset.GRID_UNIT_NUMBER.value * Asset.GRID_UNIT_SIZE.value)) # Draws out the game window 800 pixels wide and high, also the surface on which game elements are placed.
        self.clock = pygame.time.Clock() # Creates a clock object that dictates frame rate in the main loop.
        self.reset_game_assets()
        
    def reset_game_assets(self): # This is a new function, and it needs to be included since every time the AI dies, it should respawn with a new snake, not close the entire program.
        self.appleImg = pygame.image.load(Asset.APPLE_PNG.value).convert_alpha()
        self.scoreFont = pygame.font.Font(Asset.FONTS.value, 35) 
        
        SCREEN_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(SCREEN_UPDATE, 250)  # The custom event set above only triggers every 250 milliseconds.
        
        self.snake = SNAKE(self.gameScreen)
        self.apple = APPLE() # For the entire game logic to happen in this class, a snake and fruit need to be created from previous classes.
        self.frame_iteration = 0
        self.score = 0
        self.reward = 0
        self.gameOver = False # All of these values need to be set to 0 or False for the game to reset properly.
    
    def update_snake_position(self): # This function is responsible for moving the snake based on the function created in the snake class.
        self.snake.move_snake()
        self.check_apple_eaten()
        if self.check_fail_condition() or self.frame_iteration > 100 * len(self.snake.body): # The game also ends if the snake does nothing for an extended period of time, or it "starves".
            self.snake.play_death_sound()
            self.reward = -10 # The reward for dying is -10, so it makes the snake want to avoid dying for as long as possible to get as much reward.
            self.gameOver = True
        
    def draw_entities(self): # This function draws out the apple and the snake, as defined by the functions in the previous classes.
        self.draw_grass_tiles()
        self.draw_apple()
        self.snake.draw_snake(self.gameScreen) 
        self.draw_scoreboard() # The scoreboard and grass tiles are also drawn out in this function.
    
    def check_apple_eaten(self): # This function checks if the apple is eaten, and this is checked every single time the snake's position is updated. 
        if self.apple.coords == self.snake.body[0]:
            self.apple.random_fruit_position() # This checks if the apple is at the same position as the front of the snake, if it is, it randomizes the position again
            self.snake.insert_new_segment() # This method elongates the snake by one square if it eats an apple.
            self.snake.play_eating_sound()
            self.score += 1
            self.reward = 10 # If the snake eats the fruit, it not only gets a point, but a hidden reward used to train the AI is also set to 10.
        
        for counter in self.snake.body[1:]: # If a fruit spawns anywhere on the snake's body, that would be confusing, so it places a new fruit so it's outside of the body.
            if counter == self.apple.coords:
                self.apple.random_fruit_position()

    def check_fail_condition(self): # This function checks if the snake hit the walls or itself, and then presents a game over.
        is_game_over = False
        if not(0 <= self.snake.body[0].x < Asset.GRID_UNIT_NUMBER.value) or not(0 <= self.snake.body[0].y < Asset.GRID_UNIT_NUMBER.value): # This if statement checks if the head of the snake is outside of the boundaries of the grid, being 0 to 20 squares.
            is_game_over = True
            return is_game_over
        
        for counter in self.snake.body[1:]: # This for loop checks if any of the snake body segments collided into the head, because that is one of the fail conditions of snake.
            if counter == self.snake.body[0]: # The if statement is included because the head could crash into any of the segments to end the game.
                is_game_over = True
                break
                
        return is_game_over # This returns True if the snake dies, and is used in updaate_snake_position() to update self.gameOver, which is then passed onto the agent.
        
    def check_fail_condition_point(self, any_point): # This function is used in the agent to detect whether the snake will crash into a certain point.
        if not(0 <= any_point.x < Asset.GRID_UNIT_NUMBER.value) or not(0 <= any_point.y < Asset.GRID_UNIT_NUMBER.value): # This is very similar to checking if the head is in danger, but each point around the head is passed in instead.
            return True
            
        for counter in self.snake.body: 
            if counter == any_point:
                return True
        
        return False
    
    def draw_grass_tiles(self): # This function is responsible for drawing out the alternating tiles that make up the background.
        dark_grass_colour = (142, 204, 57) # This tuple holds the darker green colour that constrasts the lighter green tiles in the pattern.
        for row in range(Asset.GRID_UNIT_NUMBER.value):
            if row % 2 == 0: # In every even row of the game, it will draw a darker tile, further drawing them on only even columns as well.
                for column in range(Asset.GRID_UNIT_NUMBER.value):
                    if column % 2 == 0:
                        grassRect = pygame.Rect(column * Asset.GRID_UNIT_SIZE.value, row * Asset.GRID_UNIT_SIZE.value, Asset.GRID_UNIT_SIZE.value, Asset.GRID_UNIT_SIZE.value)
                        pygame.draw.rect(self.gameScreen, dark_grass_colour, grassRect) # The rectangles only exist in every other column, so they are drawn here using the previous colour and rectangle. 
            else: # In all of the odd rows of the game, the program has to draw squares on all of the odd columns, which is what the else does.
                for column in range(Asset.GRID_UNIT_NUMBER.value):
                    if column % 2 != 0:
                        grassRect = pygame.Rect(column * Asset.GRID_UNIT_SIZE.value, row * Asset.GRID_UNIT_SIZE.value, Asset.GRID_UNIT_SIZE.value, Asset.GRID_UNIT_SIZE.value)
                        pygame.draw.rect(self.gameScreen, dark_grass_colour, grassRect)

    def draw_apple(self): # This function defines how and where the fruit will be displayed.
        appleRectangle = pygame.Rect(self.apple.coords.x * Asset.GRID_UNIT_SIZE.value, self.apple.coords.y * Asset.GRID_UNIT_SIZE.value, Asset.GRID_UNIT_SIZE.value, Asset.GRID_UNIT_SIZE.value) # This defines the apple as a rectangle with an x and y position from the vector, and dimensions from the grid size.
        self.gameScreen.blit(self.appleImg, appleRectangle) # This line actually draws out the fruit on the main screen using the image object that is declared later.
        
    def draw_scoreboard(self): # This function draws out a score in the bottom right of the screen, technically it is extremely rare for someone to win, so this game is programmed for getting a high score.
        scoreboardText = str(len(self.snake.body) - 3) # The score is always equal to 3 minus the amount of segments in the snake, as it starts off with 3 segments.
        scoreboardSurface = self.scoreFont.render(scoreboardText, True, (56, 74, 12))
        score_x = int(Asset.GRID_UNIT_SIZE.value * Asset.GRID_UNIT_NUMBER.value - 60)
        score_y = int(Asset.GRID_UNIT_SIZE.value * Asset.GRID_UNIT_NUMBER.value - 40) # These two lines place the top left edge of the score near the bottom right of the screen.
        scoreRectangle = scoreboardSurface.get_rect(center = (score_x, score_y)) # Creates a rectangle on the scoreboard's surface in the center of it
        appleRect = self.appleImg.get_rect(midright = (scoreRectangle.left, scoreRectangle.centery)) # This puts an apple next to the score to make it more interesting to look at.
        backgroundRectangle = pygame.Rect(appleRect.left, appleRect.top, appleRect.width + scoreRectangle.width + 5, appleRect.height)
        pygame.draw.rect(self.gameScreen, (167,217,72), backgroundRectangle) # This line draws out the backdrop of the scoreboard
        self.gameScreen.blit(scoreboardSurface, scoreRectangle)
        self.gameScreen.blit(self.appleImg, appleRect)
        pygame.draw.rect(self.gameScreen, (56, 74, 12), backgroundRectangle, 2) # This line is responsible for drawing a border around the scoreboard to make it easier to see.

    def _instruction(self, command): # The action passed into play_step() further gets passed into here, and it processes and returns what direction the snake should move next.
        next_move = Vector2(0, 0)
        # Comments in this function are to clarify each line to make them less confusing to read, as it deals a lot with vectors.

        if self.snake.direction.y == 1: # This checks if the snake is currently moving down
            if command[0] == 1: # straight ahead command passed in from model
                next_move = Vector2(0, 1) # keep moving on positive y direction
            elif command[1] == 1: # turn right command passed in from model
                next_move = Vector2(-1, 0) # start moving on negative x direction
            elif command[2] == 1: # turn left command passed in from model
                next_move = Vector2(1, 0) # start moving on positive x direction
            else:
                next_move = Vector2(0, 1) # keep moving on positive y direction
                
        elif self.snake.direction.y == -1: # Snake moving up
            if command[0] == 1: # straight ahead command passed in from model
                next_move = Vector2(0, -1) # keep moving on negative y direction
            elif command[1] == 1: # turn right command passed in from model
                next_move = Vector2(1, 0) # start moving on positive x direction
            elif command[2] == 1: # turn left command passed in from model
                next_move = Vector2(-1, 0) # start moving on negative x direction
            else:
                next_move = Vector2(0, -1) # keep moving on negative y direction

        if self.snake.direction.x == 1: # Snake moving right
            if command[0] == 1: # straight ahead command passed in from model
                next_move = Vector2(1, 0) # keep moving on positive x direction
            elif command[1] == 1: # turn right command passed in from model
                next_move = Vector2(0, 1) # start moving on positive y direction
            elif command[2] == 1: # turn left command passed in from model
                next_move = Vector2(0, -1) # start moving on negative y direction
            else:
                next_move = Vector2(1, 0) # keep moving on positive x direction
        
        elif self.snake.direction.x == -1: # Snake moving left
            if command[0] == 1: # straight ahead command passed in from model
                next_move = Vector2(-1, 0) # keep moving in the negative x direction
            elif command[1] == 1: # turn right command passed in from model
                next_move = Vector2(0, -1) # start moving in the negative y direction
            elif command[2] == 1: # turn left command passed in from model
                next_move = Vector2(0, 1) # start moving in the positive y direction
            else:
                next_move = Vector2(-1, 0) # keep moving in the negative x direction
        
        return next_move # The direction is then returned as self.snake.direction, and that is passed into update_snake_position() to move the snake.

    def play_step(self, action): # The play_step function now takes in an action from the agent to move according to the AI.
        self.frame_iteration += 1 # frame_iteration is incremented every time the snake moves, and if it gets above a certain value, the environment kills off the snake to avoid infinite looping.
        self.reward = 0
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Checks if the user hit the "X" in the top right
                pygame.quit()
                sys.exit() # These two lines make sure that the game window is closed.

        self.snake.direction = self._instruction(action) # The direction is now generated by the above function, not by keyboard presses.
        self.update_snake_position()
            
        # 2. move
        self.gameScreen.fill((167,217,72)) # Sets the main game screen to a green color.
        self.draw_entities() # Draws both the snake and the apple using the main class.
        pygame.display.update() # Updates the graphics for the entire loop before iterating
        self.clock.tick(60) # Limits the frame rate based on the clock object to 60 FPS.
        return self.reward, self.gameOver, self.score # These parameters need to be returned to the agent for further processing.