# Referenced from Patrick Loeber aka. Python Engineer, https://github.com/python-engineer/snake-ai-pytorch/blob/main/helper.py
# Submitted on: Wednesday, April 21, 2021
# Course Code: ICS 3U0-C, Introduction to Computer Science
# Teacher: Mr. Le
# This helper was referenced from somewhere else because it is a very specific function in the program that only works if the user runs the file in an interactive window.
# Because plotting with matplotlib is very specific, this plot function was referenced from the above link.
# This helper draws out a graph with an x and y axis, with the x-axis containing the game number and the y-axis containing the score.

import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def plot(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    