'''
Calib_Grid
------------------
This is an environment for collecting calibration data for the grid navigation task. If offers a simplified version of the 
'''



import pygame
import random
import time
import numpy as np
import sys
from pylsl import StreamInlet, StreamOutlet,StreamInfo,resolve_stream
import vis_data

# COLOR
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# screen
WIDTH = 1000
HEIGHT = 1000

# Learning
GAMMA = .2

class CalibGrid():

  def __init__(self):

    #
    # PYGAME
    # ------
    # Set up the window, screen, and clock

    self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
    self.clock = pygame.time.Clock()
    pygame.display.set_caption("TRAINING")
    self.square_length = 200
    self.margin = 10
    #
    # LABSTREAMINGLAYER
    # -------
    # Set up communication with NeuroPype
    #
    # Input Stream:
    #      name = 'error_feedback'
    #      Accepts feedback from NeuroPype regarding whether an error potential was
    #      detected after the agent performed an action
    # Output Stream
    #      name = 'action_stream'
    #      Sends a marker to NeuroPype when an action has been performed by the agent.
    #      This tells NeuroPype to look for feedback on that particular action

    # LSL setup
    info_correct = StreamInfo('correctness','Markers',1, 0,'string','markerstream2')
    self.outlet_correct = StreamOutlet(info_correct)
    self.markers = ['Correct','Incorrect']

    #
    # AGENT
    # ------
    # The action space consists of 4 directions of movement: North, East, South, West
    # These four actions are stored in the self.actions list as a tuple containing
    # the direction to move (in the form of (x,y) change in coordinates) and the 
    # probability of selecting this action. i.e.: [(dx,dy), probability]
    # The training probabilities are set to .25

    init_prob = .25
    print(init_prob)
    self.actions = [
        (0,-1),   #North
        (1,0),    #East
        (0,1),    #South
        (-1,0)    #West
     ]

    # Initialize the task
    pygame.init()
    self.run_loop()

  def run_loop(self):
    '''
    run_loop
    ----------
    This function contains the main loop of the task. Each time the loop runs, every
    object in the task screen needs to be redrawn (this is achieved using draw_square()).
    The loop continues to update the screen until the agent reaches the goal.

    '''
    num_trials = 100
    agent_pos = (1,1)    # initial coordinates of the agent (x,y)

    # MAIN LOOP
    for i in range(num_trials):
      # CREATE GRID
      correct_idx = random.randint(0,3)
      self.draw_grid(correct_idx)
      time.sleep(2)

      # SELECT MOVE
      action_idx = random.randint(0,3)
      action = self.actions[action_idx]

      # MOVE AGENT
      print(action)
      print("DAEWEWR")
      self.draw_square(1,1,WHITE)
      self.draw_square(1+action[0],1+action[1],RED)

      pygame.display.flip()
      
      # SEND MARKER
      if action_idx == correct_idx:
        self.outlet_correct.push_sample(['Correct'])
      else:
        self.outlet_correct.push_sample(['Incorrect'])
      

      # PAUSE BEFORE NEXT LOOP
      time.sleep(2)
      self.draw_square(1+action[0],1+action[1],WHITE)
      self.draw_target(correct_idx,erase=True)
      print('daw')
      pygame.display.flip()
      time.sleep(1)


  def draw_grid(self,correct_idx):
    for row in range(3):
      for column in range(3):
          self.draw_square(column,row,WHITE)

    # INSERT AGENT
    self.draw_square(1,1,RED)
    self.draw_target(correct_idx)

    # DRAW CURRENT SCREEN
    pygame.display.flip()
  
  def draw_target(self,dir_idx,erase=False):
    NORTH = [210,0,620,200]
    EAST = [740,210,200,620]
    SOUTH = [210,740,620,200]
    WEST = [0,210,200,620]
    directions = [NORTH,EAST,SOUTH,WEST]
    if not erase:
      color = GREEN
    else:
      color = BLACK
    pygame.draw.rect(self.screen,
                     color,
                      directions[dir_idx])

  def draw_square(self,x,y,color):
    pygame.draw.rect(self.screen,
                     color,
                     [200+(self.margin + self.square_length) * x + self.margin,
                      200+(self.margin + self.square_length) * y + self.margin,
                      self.square_length,
                      self.square_length])



if __name__ == '__main__':
  gn = CalibGrid()
  


