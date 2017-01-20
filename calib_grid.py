'''
TODO
----
  - Expand the number of possible actions to 8 (NE, SE, NW, SW)

'''



import pygame
import random
import time
import numpy as np
from pylsl import StreamInlet, StreamOutlet,StreamInfo,resolve_stream
from pygame.locals import *
# COLOR
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# screen
WIDTH = 1000
HEIGHT = 1000
MARGIN = 30
square_length = 100

# Learning
GAMMA = .2

class CalibNavigate():

  def __init__(self):
    self.dim=3
    self.margin=10
    self.square_length=100
    #
    # PYGAME
    # ------
    # Set up the window, screen, and clock

    self.screen = pygame.display.set_mode([600, 600])
    self.clock = pygame.time.Clock()

    pygame.display.set_caption("Navigation Task")
    info_correct = StreamInfo('correctness','Markers',1, 0,'string','markerstream2')
    self.outlet_correct = StreamOutlet(info_correct)
    self.markers = ['Correct','Incorrect']


    #
    # AGENT
    # ------
    # The action space consists of 4 directions of movement: Up, Down, Left, Right
    # These four actions are stored in the self.actions list as a tuple containing
    # the direction to move (in the form of (x,y) change in coordinates) and the 
    # probability of selecting this action. i.e.: [(dx,dy), probability]
    # The initial probabilities are set to .25

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
    agent_pos = (1,1) 
    for i in range(num_trials):
      print(i)
      pygame.event.get() 
        # CREATE GRID
      correct_idx = random.randint(0,3)
      self.draw_grid(correct_idx)
      pygame.time.wait(2000)

      # SELECT MOVE
      p = [.1,.1,.1,.1]
      p[correct_idx] = .70
      action_idx = np.random.choice(4,1,p=p)[0]
      print(action_idx)
      action = self.actions[action_idx]

      # MOVE AGENT
      print(action)
      self.draw_square(1,1,WHITE)
      self.draw_square(1+action[0],1+action[1],RED)

      pygame.display.flip()
      # SEND MARKER
      if action_idx == correct_idx:
        self.outlet_correct.push_sample(['Correct'])
      else:
        self.outlet_correct.push_sample(['Incorrect'])

      # PAUSE BEFORE NEXT LOOP
      pygame.time.wait(2000)
      self.draw_square(1+action[0],1+action[1],WHITE)
      self.draw_target(correct_idx,erase=True)
      pygame.display.flip()
      pygame.time.wait(1000)
      clock.tick(60)

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
    NORTH = [135,25,320,75]
    EAST = [465,110,75,320]
    SOUTH = [135,440,320,75]
    WEST = [50,110,75,320]
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
                     [125+(self.margin + self.square_length) * x + self.margin,
                      100+(self.margin + self.square_length) * y + self.margin,
                      self.square_length,
                      self.square_length])
if __name__ == '__main__':
  gn = CalibNavigate()
  


