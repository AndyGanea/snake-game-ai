# Snake Game Computer Science Final Summative

Author: Andrew Nicholas Ganea
Date of Submission: Wednesday, April 21, 2021
Version: 1.6
Unit: 6 - Culminating
Programming Language: Python 3.9.2 64-bit

## Program Description

This is an implementation of the well-known Snake Game in Python, with assets based off of Google's web version of the same game.
The main game environment was created using PyGame, and the AI was created using PyTorch, Matplotlib, and IPython.
The program can be run in two different ways, via a human-controlled version of the game, or an AI-controlled version of the game.
Upon running game_human_player.py and going through the main menu, the game can be played normally at a comfortable speed.
The objective of the game is to guide the snake to eat as much fruit as possible, attempting to get a high score.
The game is over when the snake collides with the boundaries of the screen, or if it collides into itself.
Upon running agent.py in an interactive window, you can witness an AI first attempt to learn the environment around it, and then exploit it to get the best score.

## Program Assumptions

In the main menu of the human-controlled game, the program assumes that the user will use the 1, 2, and 3 keys to navigate the menu.
The program also assumes that the user wants to use the WASD or arrow keys to control the game.
The program assumes that the user knows how to read and understand English to read the instructions, but no English proficiency is required to play the game.
The program finally assumes that the user has the correct version of Python installed on their computer will all of the libraries installed as well.

## Features of the Program

The human-controlled program starts off with a main menu and presents the user with the option to start the game, to read instructions, or to quit the game.
Once in the game, the user can control the snake using the WASD or arrow keys on their keyboard, and the snake graphics update according to the snake's movement.
The human-controlled program also has a button that allows the user to swap out which fruit they want to eat, and it provides the user with 7 different fruits to pick from.
The human-controlled program's background music plays throughout the program's duration, and has sounds for eating the fruit as well as ending the game.
The AI-controlled program takes the environment from the human-controlled game and strips away the music, button, and main menu.
In this program, the user can watch as a Deep Q Learning algorithm takes control and tries to learn the game to become better than any human ever could at snake.
After enough games, the AI swaps from exploration to exploitation, as it learns new strategies on how to survive the longest and eat the most fruit.
The AI model then saves itself in a model folder in the main directory as a .pth file.

## Restrictions

On the main menu, the user can only navigate the options using the 1, 2, and 3 keys, and not with the arrow keys or mouse.
The user also does not have the option to change the keybinds of the game, they must use the WASD or arrow keys to control it.
Once a game has been ended, there is no option for the user to restart the game, they must restart the program to play again.
The game window can be exited at any time using the "X" in the top right of the screen, but there is no keybind to exit the game.
If the snake is moving in a certain direction, the user is unable to move the snake directly into itself, thereby ending the game at a normal position.

## Known Errors

In the human-controlled game, the speed that the game loop iterates at the and the speed the graphics update are different to make the game easy enough to play.
This means that in one graphics update of the game, the user can introduce two unique keyboard inputs. 
If the snake is moving right, the user can press up or down to bypass the restriction, and then immediately press left, making the snake ram into itself.
Due to how the model of the AI-controlled game is made, some generations will simply run around in circles or patterns, avoiding the fruit as long as possible before starving.
This is because the AI is incentivized to survive as long as possible, and delaying how fast it dies by going in these patterns gives it a better reward.

## Implementation Details

To play the game, you first need to clone or download this repository from Github. 
After that, sse the package manager [pip](https://pip.pypa.io/en/stable/) to install the following libraries:
```bash
pip install pygame
pip install torch torchvision
pip install matplotlib ipython
```
To run the human-controlled version, simply run game_human_player.py
To run the AI-controlled version, agent.py needs to be run in an interactive window for the graph to be displayed.

## Additional Files

Along with this README file and the two files listed above, the program also comes with the environment, helper, and model to run the AI-controlled version of the game.
The Fonts, Sounds, and Graphics folder are used to store the .ttf, .png, .mp3, and .wav files required for the game to run.