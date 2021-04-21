# Referenced from Patrick Loeber aka. Python Engineer, https://github.com/python-engineer/snake-ai-pytorch/blob/main/helper.py
# Submitted on: Wednesday, April 21, 2021
# Course Code: ICS 3U0-C, Introduction to Computer Science
# Teacher: Mr. Le
# This helper was referenced from somewhere else because it is a very specific function in the program that only works if the user runs the file in an interactive window.
# Because plotting with matplotlib is very specific, this plot function was referenced from the above link.
# This helper draws out a graph with an x and y axis, with the x-axis containing the game number and the y-axis containing the score.

import matplotlib.pyplot as plt
from IPython import display

plt.ion() # Turns the interactive mode of the plot on.

def plot(scores, mean_scores): # This is the plot function that is referenced in the agent file, so it takes in two inputs.
    display.clear_output(wait=True)
    display.display(plt.gcf()) # Gets the current figure of the graph.
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score') # Sets the labels of the x-axis and the y-axis to always be Number of Games and Score respectively.
    plt.plot(scores)
    plt.plot(mean_scores) # Uses the library module to actually plot, but this is different than the main function it is within, since plot() will be called outside this file.
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1])) # The first two arguments of .text() tell the program where to plot the data, and str(scores[-1]) is the text which is being drawn.
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    
