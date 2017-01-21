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
import os
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
    self.margin=10
    self.square_length=100


    os.environ['SDL_VIDEO_CENTERED'] = '1'
    #
    # PYGAME
    # ------
    # Set up the window, screen, and clock

    self.screen = pygame.display.set_mode([1000, 1000])
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
    pygame.time.wait(5000)
    self.actions = [
        (1,0),    #East
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
    num_trials = 350
    agent_pos = (1,1) 
    for i in range(num_trials):
      print(i)
      pygame.event.get() 
      # CREATE GRID
      correct_idx = random.randint(0,1)
      self.draw_grid(correct_idx)
      pygame.time.wait(2000)

      # SELECT MOVE
      p = [.2,.2]
      p[correct_idx] = .80
      action_idx = np.random.choice(2,1,p=p)[0]
      action = self.actions[action_idx]

      # MOVE AGENT
      self.draw_square(2,1,WHITE)
      self.draw_square(2+action[0],1,RED)

      pygame.display.flip()
      # SEND MARKER
      if action_idx == correct_idx:
        self.outlet_correct.push_sample(['Correct'])
      else:
        self.outlet_correct.push_sample(['Incorrect'])

      # PAUSE BEFORE NEXT LOOP
      pygame.time.wait(2000)
      self.draw_square(2+action[0],1,WHITE)
      self.draw_target(correct_idx,erase=True)
      pygame.display.flip()
      pygame.time.wait(1000)

  def draw_grid(self,correct_idx):
    # self.draw_square(0,1,BLACK)
    for column in range(0,5):
        if correct_idx == 0 and column==4:
          self.draw_square(column,1,GREEN)
          # self.draw_square(0,1,BLACK)
          print('test1')
        elif correct_idx==1 and column==0:
          self.draw_square(column,1,GREEN)
          self.draw_square(3,1,BLACK)
          print('test2')
        elif column>0 or column<4:
          self.draw_square(column,1,WHITE)
      

    # INSERT AGENT
    self.draw_square(2,1,RED)

    # DRAW CURRENT SCREEN
    pygame.display.flip()
  
  def draw_target(self,dir_idx,erase=False):
    if dir_idx==0:
      column=4
    else:
      column=0
    if not erase:
      color = GREEN
    else:
      color = WHITE
    self.draw_square(column,1,color)

  def draw_square(self,x,y,color):
    pygame.draw.rect(self.screen,
                     color,
                     [225+(self.margin + self.square_length) * x + self.margin,
                      300+(self.margin + self.square_length) * y + self.margin,
                      self.square_length,
                      self.square_length])
if __name__ == '__main__':
  gn = CalibNavigate()
  


