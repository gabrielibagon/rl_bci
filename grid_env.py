'''
TODO
----


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

class GridNavigate():

  def __init__(self,n):

    #
    # PYGAME
    # ------
    # Set up the window, screen, and clock

    self.dim = n
    self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
    self.clock = pygame.time.Clock()
    pygame.display.set_caption("Navigation Task")
    self.square_length = 800/self.dim
    self.margin = 100/self.dim
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

    action_stream = StreamInfo('action','Markers',1,0,'string','task_marker_stream')
    self.action_outlet = StreamOutlet(action_stream)

    ########## COMMENT OUT FOR DEBUGGING ############
    # feedback_stream = resolve_stream('name', 'error_feedback')
    # self.feedback_inlet = StreamInlet(feedback_stream[0])
    ########## COMMENT OUT FOR DEBUGGIN###########

    #
    # AGENT
    # ------
    # The action space consists of 4 directions of movement: Up, Down, Left, Right
    # These four actions are stored in the self.actions list as a tuple containing
    # the direction to move (in the form of (x,y) change in coordinates) and the 
    # probability of selecting this action. i.e.: [(dx,dy), probability]
    # The initial probabilities are set to .25
    init_prob = 1.0/8.0
    print(init_prob)
    self.actions = [
        [(0,-1), init_prob],   #North
        [(1,-1), init_prob],   #NorthEast
        [(1,0), init_prob],     #East
        [(1,1), init_prob],    #SouthEast
        [(0,1), init_prob],    #South
        [(-1,1), init_prob],   #SouthWest
        [(-1,0), init_prob],     #West
        [(-1,-1), init_prob]  #NorthWest
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

    DONE = False                  # determines if the task is finished
    agent_pos = (0,self.dim-1)    # initial coordinates of the agent (x,y)
    goal_pos = (self.dim-1,0)      # initial coordinates of the goal (x,y)
    num_step = 1                  # temporarily make step always 1
    # INITIALIZE GRID
    self.draw_grid(agent_pos,goal_pos)
    #time.sleep(.1)
 
    # FIRST MOVE
    pos_t0 = agent_pos
    agent_pos, idx_action = self.move_agent(agent_pos)
    steps = 1
    # MAIN LOOP
    while not DONE:
      pos_t1 = agent_pos

      feedback=None

      # CREATE GRID
      self.draw_grid(agent_pos,goal_pos)

      # SEND MARKER
      self.action_outlet.push_sample(['movement'])

      ########## COMMENT OUT FOR DEBUGGING ############
      # RECEIVE FEEDBACK
      # while feedback is None:
      #  feedback,timestamp = self.feedback_inlet.pull_sample()
      ########## COMMENT OUT FOR DEBUGGING ############
      waiting = True
      pygame.event.clear()
      while waiting:
        events = pygame.event.get()
        for event in events:
          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
              print('correct')
              waiting = False
              feedback = 'correct'
            elif event.key == pygame.K_LEFT:
              print('incorrect')
              waiting = False
              feedback = 'incorrect'
      pygame.event.clear()
      # UPDATE ACTION TABLE
      self.update_action_table(feedback,pos_t0,pos_t1,idx_action,num_step)

      # CHECK IF FINISHED
      if agent_pos == goal_pos:
        print("DONE")
        DONE = True
        lines = []
        for action in self.actions:
          lines.append(action[1])
        vis_data.vector(lines)
        break
      # UPDATE AGENT POSITION
      pos_t0 = agent_pos
      agent_pos,idx_action = self.move_agent(agent_pos)
      # PAUSE BEFORE NEXT LOOP
      #time.sleep(.1)
      steps+=1
    print(steps)
    return(steps)
  def draw_grid(self,agent_pos,goal_pos):
    for row in range(self.dim):
      for column in range(self.dim):
          self.draw_square(column,row,WHITE)

    # INSERT GOAL
    self.draw_square(goal_pos[0],goal_pos[1],GREEN)

    # INSERT AGENT
    self.draw_square(agent_pos[0],agent_pos[1],RED)

    # DRAW CURRENT SCREEN
    pygame.display.flip()

  def update_action_table(self,feedback,pos_t0,pos_t1,idx_action,num_step):
    '''
    update_action_table
    -------------------
    Updates the probabilities of the actions.

    These are some of the rules of the update: 
      1. Positive feedback for an action increases the probability that that action
          will be selected in the future. It decreases the opposite action, and slight
          increases it's neighbors.
      2. The probability change is proportional to the size of the board
      3. As more steps are taken, the increase/decrease in probability becomes more drastic. 
         This is to allow fine tuning of actions as the object moves closer to its target.

    '''
    effect = .1 / self.dim
    n = .5
    #print(idx_action)
    if feedback == 'correct':
      c = 1
    else:
      c = -1
    self.print_action_table()
    # reward or punish correct action
    self.actions[idx_action][1] = self.actions[idx_action][1]+ (effect * c)
    # reward or punish neighboring actions
    idx_neighbor = (idx_action+1)%8
    self.actions[idx_neighbor][1] = self.actions[idx_neighbor][1]+(effect * c * n) 
    idx_neighbor = (idx_action-1)%8
    self.actions[idx_neighbor][1] = self.actions[idx_neighbor][1]+(effect * c * n)
    # reward or punish opposite action
    anti_idx = (idx_action+4) % 8
    self.actions[anti_idx][1] = self.actions[anti_idx][1]+(effect * -1 * c)
    anti_neighbor = (anti_idx+1) % 8
    # reward or punish neighboring actions
    self.actions[anti_neighbor][1] = self.actions[anti_neighbor][1] + (effect * -1 * c * n)
    anti_neighbor = (anti_idx-1) % 8
    self.actions[anti_neighbor][1] = self.actions[anti_neighbor][1] + (effect * -1 *  c * n)
    self.print_action_table()

  def print_action_table(self):
    action_list = ['north','northeast','east','southeast','south','southwest','west','northwest'] 
    
    prob_sum =0
    for idx,action in enumerate(self.actions):
      print(action_list[idx], action[1])
      prob_sum+=action[1]
    print(prob_sum)
  def move_agent(self,agent_pos):
    decision = []
    decision[:] = self.actions
    if agent_pos[0] == 0:
      del decision[5:]
    elif agent_pos[0] == (self.dim-1):
      del decision[1:4]
    if agent_pos[1] == 0:
      del decision[0:2]
      del decision[5]
    elif agent_pos[1] == (self.dim-1):
      if (agent_pos[0] == 0):
        del decision[3:]
      elif agent_pos[0] == (self.dim-1):
        del decision[1:3]
        del decision[1]
      else:
        del decision[3:6]

    weighted_decision = []
    # weight random selection
    for element in decision:
      weighted_decision += [element[0]] * int(element[1] * 1000)
    choice = random.choice(weighted_decision)
    
    agent_pos = (agent_pos[0] + choice[0], agent_pos[1] + choice[1])
    
    #get index of choice
    for i,j in enumerate(self.actions):
        if choice == j[0]:
          idx_action = i

    return agent_pos, idx_action

  def draw_square(self,x,y,color):
    pygame.draw.rect(self.screen,
                     color,
                     [(self.margin + self.square_length) * x + self.margin,
                      (self.margin + self.square_length) * y + self.margin,
                      self.square_length,
                      self.square_length])



if __name__ == '__main__':
  nd = 6
  if len(sys.argv) > 1:
    nd = int(sys.argv[1])
  gn = GridNavigate(nd)
  


