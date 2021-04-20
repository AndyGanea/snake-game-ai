# Author: Andrew Nicholas Ganea aka. (Andy Ganea)
# Submitted on: Wednesday, April 21, 2021
# Course Code: ICS 3U0-C, Introduction to Computer Science
# Teacher: Mr. Le
# This program is the human-controlled version of the Snake Game AI Project. Upon running the program, the user is greeted with a main menu.
# The menu has 3 options: play the game, read the instructions, and quit the game. The game is a simple adaptation of the classic snake game in Python.
# The user must use either the WASD keys or the arrows keys to change the snake's direction, and the objective of the game is to eat as much fruit as possible.
# The fruit displayed on screen can be switched with a button in the top-right of the game, and cycles through 7 different fruits.
# The game ends when the snake hits the border of the screen or if it runs into itself. The program must be restarted in order to play again.

import pygame, sys, random, time, os
from pygame.math import Vector2 # This import is to directly use Vector2 for creating vectors.
from enum import Enum # This library is used to hold the imported assets in the Asset class 

class Asset(Enum): # This class is used to stores all of the files that are needed to run the game, such as images and sounds
    
    # This constant stores the folder of the program in a variable to be called on in the rest of the class.
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
    BGMUSIC_MP3 = os.path.join(FILEDIR, 'Sounds/bgmusic.mp3')

    # Filepaths for the images of the fruits, the fruit bowl on the scoreboard, and the button that allows the user to switch between fruits.
    APPLE_PNG = os.path.join(FILEDIR, 'Graphics/apple.png')
    ORANGE_PNG = os.path.join(FILEDIR, 'Graphics/orange.png')
    BANANA_PNG = os.path.join(FILEDIR, 'Graphics/banana.png')
    GRAPES_PNG = os.path.join(FILEDIR, 'Graphics/grapes.png')
    LEMON_PNG = os.path.join(FILEDIR, 'Graphics/lemon.png')
    MANGO_PNG = os.path.join(FILEDIR, 'Graphics/mango.png')
    STRAWBERRY_PNG = os.path.join(FILEDIR, 'Graphics/strawberry.png')
    FRUITBOWL_PNG = os.path.join(FILEDIR, 'Graphics/fruitbowl.png')
    BUTTON_PNG = os.path.join(FILEDIR, 'Graphics/buttonswap.png')
    
    # Filepath for the font used, which is Google's font that is open to modification and personal use.
    FONTS = os.path.join(FILEDIR, 'Fonts/ProductSans.ttf')
    
    # Various string values to be printed in the terminal, along with the title of the game window
    FRUIT_GET_MSG = "Fruit Get!"
    FINAL_SCORE_MSG = "Your final score is: "
    THX_FOR_PLAYING_MSG = "Thanks for playing!"
    SET_CAPTION = "Andy Ganea's Snake Game | Human Player Variant"
    
    # These are the constants that determine how the game window is drawn out.
    GRID_UNIT_NUMBER = 20 # This value determines how many squares make up the grid seen on screen.
    GRID_UNIT_SIZE = 40 # This value determines how wide and tall each square of the grid is, in pixels.
    
class SNAKE: # This class contains all of the functions that control the logic of the snake itself, including its movements and drawing, along with some helper functions for sound playing.
    def __init__(self, gameScreen): # Initializes the snake and its body segment positions.
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)] # Creates the snakes body by specifying three consecutive vectors on the grid.
        self.direction = Vector2(1, 0) # The starting direction for the snake is set to right in this line.
        self.new_body_segment = False # This boolean is used inside the snake class to determine whether or not it should elongate.

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
        self.bgmusic = pygame.mixer.Sound(Asset.BGMUSIC_MP3.value)

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
                if previous_segment.x == next_segment.x: # If the segment before and after a specific body segment have the same x-coordinate, the segment must be facing vertically.
                    gameScreen.blit(self.body_v, snakeRectangle)
                elif previous_segment.y == next_segment.y: # If the segment before and after a specific body segment have the same y-coordinate, the segment must be facing horizontally.
                    gameScreen.blit(self.body_h, snakeRectangle)
                else: # This final else draws out the four corner segments of the snake's body.
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
            self.head = self.head_l # Since the four head images have been initalized previously, the flag used in the previous function can simply be updated accordingly.
        elif current_head_direction == Vector2(-1, 0):
            self.head = self.head_r
        elif current_head_direction == Vector2(0, 1):
            self.head = self.head_u
        else:
            self.head = self.head_d
    
    def update_tail_graphics(self): # This function determines which way the tail is facing, and calls on the appropriate graphic to be displayed.
        current_tail_direction = self.body[-2] - self.body[-1] # This line performs vector subtraction on the last and second last segments, resulting in one of 4 vectors.
        # This chain of if statements checks each difference, and then determines what self.tail should be.
        if current_tail_direction == Vector2(1, 0):
            self.tail = self.tail_l # This works in the same way as the update_head_graphics(), but updates the self.tail property instead
        elif current_tail_direction == Vector2(-1, 0):
            self.tail = self.tail_r
        elif current_tail_direction == Vector2(0, 1):
            self.tail = self.tail_u
        else:
            self.tail = self.tail_d

    def move_snake(self): # When the snake moves every cycle, it can either move by putting a new head in a direction and removing the tail or it keeps the tail if it is on an apple.
        if self.new_body_segment == True:
            snakeBodyCopy = self.body[:] # Creates a copy of the body segment list without the last element included.
            snakeBodyCopy.insert(0, snakeBodyCopy[0] + self.direction) # This adds a vector to the front of the list, in the direction the user inputted.
            self.body = snakeBodyCopy[:] 
            self.new_body_segment = False # This flag has to be reverted because it should only be true when the snake head is directly on the fruit.
        else: # Movement this simple can be broken down to removing the tail of the snake and re-adding that segment to the head of the snake to make a new head.
            snakeBodyCopy = self.body[:-1] # Creates a copy of the body segment list without the last element included.
            snakeBodyCopy.insert(0, snakeBodyCopy[0] + self.direction) # This adds a vector to the front of the list, in the direction the user inputted.
            self.body = snakeBodyCopy[:] # This puts the new list back into the snake body to be re-displayed.
    
    def insert_new_segment(self): # This function runs when another function in the main class runs, telling the snake that it should update a flag.
        self.new_body_segment = True 
    
    def play_eating_sound(self): # Since these sounds are triggered within the main class, it is easier to write functions for them here and then call on them in the main class.
        self.eating_sound.play()
    
    def play_death_sound(self):
        self.death_sound.play()
    
    def play_background_music(self):
        self.bgmusic.play(-1) # The -1 makes it so that the background music plays continuously as the program is being played, even in the main menu.
        pygame.mixer.music.set_volume(0.3)

class APPLE: # This class is the apple object itself, and contains all of its parameters and functions.
    def __init__(self): # This intializes the attributes of the fruit object, which is its position.
        self.random_fruit_position()
    
    def random_fruit_position(self): # This function randomizes the position of the fruit, which runs when the game starts, when the snake eats an apple, and when an apple spawns on the snake.
        self.x = random.randint(0, Asset.GRID_UNIT_NUMBER.value - 1)
        self.y = random.randint(0, Asset.GRID_UNIT_NUMBER.value - 1) # These lines place the fruit down on a random grid square position, making sure it is on screen.
        self.coords = Vector2(self.x, self.y) # Converts the two coordinates into a vector for easier use.

class HUMAN_GAME: # This class brings the previous two classes together, and makes it so that the the snake and the apple interact correctly, as well as the rest of the game.
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512) # Uses these values to make the sound sync up with the actions.
        pygame.init() # Initalizes pygame, and is a required line to start any game in pygame.
        pygame.display.set_caption(Asset.SET_CAPTION.value) # Sets the title of the game window to the specified text in the Asset class.
        
        self.gameScreen = pygame.display.set_mode((Asset.GRID_UNIT_NUMBER.value * Asset.GRID_UNIT_SIZE.value, Asset.GRID_UNIT_NUMBER.value * Asset.GRID_UNIT_SIZE.value)) # Draws out the game window 800 pixels wide and long, also the surface on which game elements are placed.
        self.clock = pygame.time.Clock() # Creates a clock object that dictates frame rate in the main loop.
        
        self.appleImg = pygame.image.load(Asset.APPLE_PNG.value).convert_alpha() # All of the different fruit images have to be loaded in from the Asset class and then converted to be used properly.
        self.orangeImg = pygame.image.load(Asset.ORANGE_PNG.value).convert_alpha()
        self.bananaImg = pygame.image.load(Asset.BANANA_PNG.value).convert_alpha()
        self.grapesImg = pygame.image.load(Asset.GRAPES_PNG.value).convert_alpha()
        self.lemonImg = pygame.image.load(Asset.LEMON_PNG.value).convert_alpha()
        self.mangoImg = pygame.image.load(Asset.MANGO_PNG.value).convert_alpha()
        self.strawberryImg = pygame.image.load(Asset.STRAWBERRY_PNG.value).convert_alpha()
        self.fruitBowlImg = pygame.image.load(Asset.FRUITBOWL_PNG.value).convert_alpha()

        self.scoreFont = pygame.font.Font(Asset.FONTS.value, 35) # This imports Google's font to use for the scoreboard.

        SCREEN_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(SCREEN_UPDATE, 120) # The custom event set above only triggers every 120 milliseconds, and controls the smoothness and speed of the snake's movement.
        
        self.snake = SNAKE(self.gameScreen) # The screen has to be passed into the snake class for the snake to be drawn on the correct surface.
        self.apple = APPLE() # For the entire game logic to happen in this class, a snake and fruit need to be created from previous classes.
        self.button = BUTTON((212, 172, 13), 740, 20, 40, 40, 0) # A button has to be created, but it's position, dimensions, and times pressed are initialized here instead of inside the button.
        pygame.display.set_icon(self.snake.head_d)
        self.snake.play_background_music()
    
    def update_snake_position(self): # This function is responsible for calling on the functions that move the snake programmatically, but not visually
        self.snake.move_snake() # The snake moves every time the program graphics update.
        self.check_apple_eaten() # Every time the snake move it could either be on top of an apple or not, so this function has to be called on as well.
        self.check_fail_condition() # The program has to check whether the game is over every time it updates as well.
    
    def draw_entities(self): # This function draws out the apple and the snake, as well as the grass tiles and the scoreboard, which need to be update to actually output something to the user.
        self.draw_grass_tiles()
        self.draw_apple()
        self.snake.draw_snake(self.gameScreen)
        self.button.draw_button(self.gameScreen) # The function that draws out the button resides in the button class.
        self.draw_scoreboard()
    
    def check_apple_eaten(self): # This function checks if the apple is eaten, and this is checked every single time the snake's position is updated. 
        if self.apple.coords == self.snake.body[0]: # This if statement compares the vector of the apple's coordinates to see if it the same position as the snake head's coordinates.
            print(Asset.FRUIT_GET_MSG.value)
            self.apple.random_fruit_position() # Since the apple is eaten, the apple is "gone", so to simulate this, the game just places a new apple object at a random location.
            self.snake.insert_new_segment() # This function elongates the snake by one square if it eats an apple, as this is the visual behaviour of eating the fruit.
            self.snake.play_eating_sound() 
        
        for counter in self.snake.body[1:]: # If a fruit spawns anywhere on the snake's body, that would be confusing, so it places a new fruit so it's outside of the body.
            if counter == self.apple.coords:
                self.apple.random_fruit_position()

    def check_fail_condition(self): # This function checks if the snake hit the walls or itself, and then moves over to the game over function.
        if not(0 <= self.snake.body[0].x < Asset.GRID_UNIT_NUMBER.value) or not(0 <= self.snake.body[0].y < Asset.GRID_UNIT_NUMBER.value): # This if statement checks if the head of the snake is outside of the boundaries of the grid, being 0 to 20 squares.
            self.end_game()
        
        for counter in self.snake.body[1:]: # This for loop checks if any of the snake body segments collided into the head, because that is one of the fail conditions of snake.
            if counter == self.snake.body[0]: # The if statement is included because the head could crash into any of the segments to end the game.
                self.end_game()
        
    def end_game(self): # This function is called if either of the fail conditions are met, and it simply closes the program much like the "x" button does. This would also run if the player beat the game, as the snake is forced to crash into itself if it fills the entire screen.
        self.snake.play_death_sound()
        print(Asset.FINAL_SCORE_MSG.value + str(len(self.snake.body) - 3)) # The ending score displayed in the terminal is just 3 minus the length of the snake since the snake originally had 3 segments.
        print(Asset.THX_FOR_PLAYING_MSG.value)
        time.sleep(0.5) # This wait is included for the death sound to have enough time to play before the game window closes
        pygame.quit()
        sys.exit()
    
    def draw_grass_tiles(self): # This function is responsible for drawing out the alternating tiles that make up the background.
        dark_grass_colour = (142, 204, 57) # This tuple holds the darker green colour that constrasts the lighter green tiles in the pattern.
        for row in range(Asset.GRID_UNIT_NUMBER.value):
            if row % 2 == 0: # In every even row of the game, this function will draw a slightly darker time every two tiles at a time.
                for column in range(Asset.GRID_UNIT_NUMBER.value):
                    if column % 2 == 0: # In all of the even rows, the darker colored tiles should be the ones in the even colums.
                        grassRect = pygame.Rect(column * Asset.GRID_UNIT_SIZE.value, row * Asset.GRID_UNIT_SIZE.value, Asset.GRID_UNIT_SIZE.value, Asset.GRID_UNIT_SIZE.value)
                        pygame.draw.rect(self.gameScreen, dark_grass_colour, grassRect) # The rectangles only exist in every other column, so they are drawn here using the above colour and rectangle. 
            else: # In all of the odd rows of the game, the program has to draw squares on all of the odd columns, which is what the else does.
                for column in range(Asset.GRID_UNIT_NUMBER.value):
                    if column % 2 != 0:
                        grassRect = pygame.Rect(column * Asset.GRID_UNIT_SIZE.value, row * Asset.GRID_UNIT_SIZE.value, Asset.GRID_UNIT_SIZE.value, Asset.GRID_UNIT_SIZE.value)
                        pygame.draw.rect(self.gameScreen, dark_grass_colour, grassRect)
  
    def draw_apple(self): # This function defines how and where the fruit will be displayed, and actually draws out the correct fruit.
        fruitRectangle = pygame.Rect(self.apple.coords.x * Asset.GRID_UNIT_SIZE.value, self.apple.coords.y * Asset.GRID_UNIT_SIZE.value, Asset.GRID_UNIT_SIZE.value, Asset.GRID_UNIT_SIZE.value) # This defines the apple as a rectangle with an x and y position from the vector, and dimensions from the grid size.
        if self.button.times_clicked == 0:
            self.gameScreen.blit(self.appleImg, fruitRectangle) # This line actually draws out the fruit on the main screen using the image object that is declared later.
        elif self.button.times_clicked == 1: # The button in the top right of the game screen increments a counter, and that counter dictates the different types of fruits drawn out
            self.gameScreen.blit(self.orangeImg, fruitRectangle)
        elif self.button.times_clicked == 2:
            self.gameScreen.blit(self.bananaImg, fruitRectangle)
        elif self.button.times_clicked == 3:
            self.gameScreen.blit(self.grapesImg, fruitRectangle) 
        elif self.button.times_clicked == 4:
            self.gameScreen.blit(self.lemonImg, fruitRectangle) 
        elif self.button.times_clicked == 5:
            self.gameScreen.blit(self.mangoImg, fruitRectangle) 
        else:
            self.gameScreen.blit(self.strawberryImg, fruitRectangle)  
        
    def draw_scoreboard(self): # This function draws out a score in the bottom right of the screen, technically it is extremely rare for someone to win, so this game is programmed for getting a high score.
        scoreboard_score_text = str(len(self.snake.body) - 3) # The score is always equal to 3 minus the amount of segments in the snake, as it starts off with 3 segments.
        scoreboardSurface = self.scoreFont.render(scoreboard_score_text, True, (56, 74, 12))
        score_x = int(Asset.GRID_UNIT_SIZE.value * Asset.GRID_UNIT_NUMBER.value - 60)
        score_y = int(Asset.GRID_UNIT_SIZE.value * Asset.GRID_UNIT_NUMBER.value - 40) # These two lines place the top left edge of the score near the bottom right of the screen.
        scoreRectangle = scoreboardSurface.get_rect(center = (score_x, score_y)) # Creates a rectangle on the scoreboard's surface in the center of it
        fruitBowlRect = self.fruitBowlImg.get_rect(midright = (scoreRectangle.left, scoreRectangle.centery)) # This puts an apple next to the score to make it more interesting to look at.
        backgroundRectangle = pygame.Rect(fruitBowlRect.left - 5, fruitBowlRect.top, fruitBowlRect.width + scoreRectangle.width + 10, fruitBowlRect.height) # This creates a rectangle in which the fruit bowl and score are put in.
        pygame.draw.rect(self.gameScreen, (167,217,72), backgroundRectangle) # This line draws out the backdrop of the scoreboard, so it is different than the main game.
        self.gameScreen.blit(scoreboardSurface, scoreRectangle) # The background rectangle of the scoreboard must first be placed on the main game screen.
        self.gameScreen.blit(self.fruitBowlImg, fruitBowlRect) # The image of the fruit bowl is then placed on top of the previous rectangle.
        pygame.draw.rect(self.gameScreen, (56, 74, 12), backgroundRectangle, 2) # This line is responsible for drawing a border around the scoreboard to make it easier to see.

    def play_step(self): # This is the main game function, and is what is repeated in the main game loop.

        # 1. The first priority on each frame of the game is to collect user input and run through game logic.
        for event in pygame.event.get(): # This for loop continuously checks all of the events that pygame is raising, and will raise flags based on what happens at each frame.
            SCREEN_UPDATE = pygame.USEREVENT # This event is a custom user event, and is named SCREEN_UPDATE to be used in this function.
            pos = pygame.mouse.get_pos() # This returns the exact pixel position of the mouse as a tuple to pos.

            if event.type == pygame.QUIT: # Checks if the user hit the "X" in the top right
                pygame.quit()
                sys.exit() # These two lines make sure that the game window is closed.
            if event.type == SCREEN_UPDATE: # This event happens every 120 milliseconds, which determines how smooth the snake moves.
                self.update_snake_position()
            if event.type == pygame.MOUSEBUTTONDOWN: # This checks if the user clicks on a button, and increments a counter that is the logic behind which fruit is displayed.
                if self.button.cursor_touching(pos): # The button should only be clicked if the left mouse button is pressed down, and if it is over the button.
                    self.button.times_clicked = (self.button.times_clicked + 1) % 7 # The button counter is incremeted but put though mod 7 so the counter only goes up to 7 before wrapping around.
            if event.type == pygame.MOUSEMOTION: # This event checks if the user has their mouse hovering over the button, so the program darkens the button to give back an output.
                if self.button.cursor_touching(pos):
                    self.button.color = (191, 155, 10)
                else: # If the user is not touching the button, it should stay on its original color.
                    self.button.color = (212, 172, 13)
            if event.type == pygame.KEYDOWN: # This if statement checks for any key presses on the keyboard, being the arrow keys.
                if event.key == pygame.K_UP or event.key == pygame.K_w: # If statement for up arrow key and w key.
                    if self.snake.direction.y != 1: # This if statement makes it so that the snake can only go up if it is not currently facing down, as it would collide into itself.
                        self.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s: # If statement for down arrow key and s key.
                    if self.snake.direction.y != -1:
                        self.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT or event.key == pygame.K_a: # If statement for left arrow key and a key. 
                    if self.snake.direction.x != 1:
                        self.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d: # If statement for right arrow key and d key.
                    if self.snake.direction.x != -1:
                        self.snake.direction = Vector2(1, 0)

        # 2. After getting the user's input, the program needes to draw out the elements on the screen to simulate animation.
        self.gameScreen.fill((167,217,72)) # Sets the main game screen to a green color.
        self.draw_entities() # Draws the snake, the apple, the alternating green tiles, and the scoreboard.
        pygame.display.update() # Updates the graphics for the entire loop before iterating
        self.clock.tick(60) # Limits the frame rate based on the clock object to 60 FPS.

class BUTTON: # This class contains all of the required helper function to draw out the button and to click on the button.
    def __init__(self, color, x, y, width, height, times_clicked): # Since the button object is created in the main class, it's parameters are passed in from the class and processed in the init here.
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.times_clicked = times_clicked
        self.buttonImg = pygame.image.load(Asset.BUTTON_PNG.value).convert_alpha() # This imports the imgae that is overlayed on top of the button.

    def draw_button(self, game_screen): # This draws out the button on the screen, including the backdrop and the image.
        buttonRectangle = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(game_screen, self.color, buttonRectangle) # This draws the slightly orange rectangle which differentiates the button from the game.
        game_screen.blit(self.buttonImg, buttonRectangle)
    
    def cursor_touching(self, pos): # This function checks if the user is hovering over the button.
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height: # If these conditions are met, then the mouse cursor is within the box.
                return True
        
        return False

def text_format(message, textFont, textSize, textColor): # This helper function allows the programmer to pass in all of the parameters of their text, and then return the rendered text.
    newFont = pygame.font.Font(textFont, textSize) # This generates the actual font using the library and the font size.
    newText = newFont.render(message, 1, textColor) # This line actually renders the font using the text, anti-aliasing, and text color.

    return newText


def main_menu(main_game_screen): # This function draws out and defines the main menu, and is what is run when the program runs.

    current_option = "start" # This makes it so that the default option that is selected when the game starts is the "start" option.
    menu_font = Asset.FONTS.value
    main_menu_clock = pygame.time.Clock() # Since the main game's clock was defined using self, a new clock has to be defined in this function.
    instructions_toggle_counter = 0 # This flag is incremented every time the player wants instructions, and draws out the necessary text.

    while True: # This while true loop makes sure that the menu is continually displayed until an option is picked.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN: # This event checks if any key on the keyboard is pressed, but not a specific one.
                if event.key == pygame.K_1:
                    current_option = "start"
                elif event.key == pygame.K_2:
                    current_option = "instructions"
                elif event.key == pygame.K_3: # The user must use the 1, 2, and 3 keys to select an option, but they do not trigger the option yet.
                    current_option = "quit"
                if event.key == pygame.K_RETURN: # The options only trigger when enter is pressed, and different enters are queued based on what the user is hovering.
                    if current_option == "start":
                        while True: # If the user enters on start, the main game loop then occurs right here using play_step()
                            game.play_step()
                    elif current_option == "instructions": # When the counter is odd, the instructions display, and when it's even, the instructions are not displayed.
                        instructions_toggle_counter += 1
                    elif current_option == "quit": # This gives the user the option to quit from the main menu, along with presses the "X" in the top right of the window.
                        pygame.quit()
                        quit()

        main_game_screen.fill((167,217,72))
        # Since the draw grass tiles function needed self as a parameter in the main class, it has to be manually re-written here in order to display on the main menu.
        dark_grass_colour = (142, 204, 57) # This tuple holds the darker green colour that constrasts the lighter green tiles in the pattern.
        for row in range(Asset.GRID_UNIT_NUMBER.value):
            if row % 2 == 0: # In every even row of the game, it will draw a darker tile, further drawing them on only even columns as well.
                for column in range(Asset.GRID_UNIT_NUMBER.value):
                    if column % 2 == 0:
                        grassRect = pygame.Rect(column * Asset.GRID_UNIT_SIZE.value, row * Asset.GRID_UNIT_SIZE.value, Asset.GRID_UNIT_SIZE.value, Asset.GRID_UNIT_SIZE.value)
                        pygame.draw.rect(main_game_screen, dark_grass_colour, grassRect) # The rectangles only exist in every other column, so they are drawn here using the above colour and rectangle. 
            else: # In all of the odd rows of the game, the program has to draw squares on all of the odd columns, which is what the else does.
                for column in range(Asset.GRID_UNIT_NUMBER.value):
                    if column % 2 != 0:
                        grassRect = pygame.Rect(column * Asset.GRID_UNIT_SIZE.value, row * Asset.GRID_UNIT_SIZE.value, Asset.GRID_UNIT_SIZE.value, Asset.GRID_UNIT_SIZE.value)
                        pygame.draw.rect(main_game_screen, dark_grass_colour, grassRect)

        title = text_format("Andy's Snake Game", menu_font, 70, (0, 0, 255)) # This holds the text that is displayed as the main game title.
        
        if current_option == "start": # These if else statements color the main options either black of white depending on if the user is hovering over them or not.
            text_start = text_format("1 - START", menu_font, 55, (255, 255, 255))
        else:
            text_start = text_format("1 - START", menu_font, 55, (0, 0, 0))
        if current_option == "instructions":
            text_instr = text_format("2 - INSTRUCTIONS", menu_font, 55, (255, 255, 255))
        else:
            text_instr = text_format("2 - INSTRUCTIONS", menu_font, 55, (0, 0, 0))
        if current_option == "quit":
            text_quit = text_format("3 - QUIT", menu_font, 55, (255, 255, 255))
        else:
            text_quit = text_format("3 - QUIT", menu_font, 55, (0, 0, 0))

        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        quit_rect = text_quit.get_rect() # All of the text options have to be converted into rectangles for them to be positioned correctly.

        # This final section draws out all of the main text using .blit
        main_game_screen.blit(title, (400 - (title_rect[2]/2), 120))
        main_game_screen.blit(text_start, (400 - (start_rect[2]/2), 300))
        main_game_screen.blit(text_instr, (170, 360)) # Since the word instructions is much longer than the rest of the options, positioning it using the rect parameters would not look nice, so it has been hard-coded.
        main_game_screen.blit(text_quit, (400 - (quit_rect[2]/2), 420))

        if (instructions_toggle_counter % 2) == 1: # If the user clicked on the instructions button, all of the game instructions will appear beneath the three main options.
            text_instructions_one = text_format("Use the WASD or Arrow Keys to move your snake around.", menu_font, 24, (0, 0, 0))
            text_instructions_two = text_format("Guide your snake so that it can eat as many delicious fruits as possible!", menu_font, 24, (0, 0, 0))
            text_instructions_three = text_format("Use the button on the top right to switch between different fruits!", menu_font, 24, (0, 0, 0))
            text_instructions_four = text_format("The snake dies if it collides into itself or the window borders.", menu_font, 24, (0, 0, 0))
            text_instructions_five = text_format("Each fruit eaten is one point, so reach for the top score!", menu_font, 24, (0, 0, 0))
           
            main_game_screen.blit(text_instructions_one, (10, 500))
            main_game_screen.blit(text_instructions_two, (10, 550))
            main_game_screen.blit(text_instructions_three, (10, 600))
            main_game_screen.blit(text_instructions_four, (10, 650))
            main_game_screen.blit(text_instructions_five, (10, 700)) # These five lines blit out all of the instructions spaced out evenly from each other.
        
        pygame.display.update() # display.update has to be run after each frame to make sure that the text stays on the screen.
        main_menu_clock.tick(60) # Since the clock object in the main class was defined using self, a different clock defined outside of the class has to be used for the main menu, even though they are both set to 60 FPS.

# This is the main game loop, and is actually what is continually running, which immediately runs into the main_menu function, which contains the main while loop.
if __name__ == '__main__':
    game = HUMAN_GAME()
    main_menu(game.gameScreen) 
    pygame.quit()