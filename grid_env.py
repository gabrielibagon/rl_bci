'''
TODO
----
  - Expand the number of possible actions to 8 (NE, SE, NW, SW)

'''



import pygame
import random
import time
from pylsl import StreamInlet, StreamOutlet,StreamInfo,resolve_stream

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

    self.actions = [
        ((0,-1), .125),   #North
        ((1,-1), .125),   #NorthEast
        ((-1,-1), .125),  #NorthWest
        ((0,1), .125),    #South
        ((1,1), .125),    #SouthEast
        ((-1,1), .125),   #SouthWest
        ((1,0),.125),     #East
        ((-1,0),.125)     #West
    ]
    self.vector = [0.0]


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
    time.sleep(1)

    # FIRST MOVE
    pos_t0 = agent_pos
    agent_pos, idx_action = self.move_agent(agent_pos)

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
      tmp_feedback = ['correct'] * 8 +['incorrect'] * 2
      feedback = random.choice(tmp_feedback)
      ########## COMMENT OUT FOR DEBUGGING ############

      # UPDATE ACTION TABLE
      self.update_action_table(feedback,pos_t0,pos_t1,idx_action,num_step)

      # CHECK IF FINISHED
      if agent_pos == goal_pos:
        print("DONE")
        DONE = True

      # UPDATE AGENT POSITION
      pos_t0 = agent_pos
      agent_pos,idx_action = self.move_agent(agent_pos)
      # PAUSE BEFORE NEXT LOOP
      time.sleep(1)
  
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
    # if feedback == 'correct':
    #  for i,a in enumerate(self.actions):
    #    if a[0] == action:
    #      self.actions[i] = (self.actions[i][0],self.actions[i][1]+.10)
    #      if i == 0:
    #        j = 1;
    #      elif i ==1:
    #        j = 0;
    #      elif i == 2:
    #        j = 3
    #      elif i == 3:
    #        j = 2
    #      self.actions[i] = (self.actions[j][0],self.actions[j][1]-.10)
    
    alpha = .15 / self.dim
    reward = num_step * alpha    
    harsh_punishment = -1*num_step * alpha / 2
    reg_punishment = harsh_punishment / 2
    print(idx_action)
    if feedback == 'correct':
      # reward correct action
      self.actions[idx_action] = (self.actions[idx_action][0],self.actions[idx_action][1]+reward)
      # punish incorrect action
      for i in range(len(self.actions)):
        if i != idx_action:
          if idx_action/2 and i/2:
            self.actions[i]= (self.actions[i][0],self.actions[i][1]+harsh_punishment)
          else: 
            self.actions[i]= (self.actions[i][0],self.actions[i][1]+reg_punishment)
    elif feedback == 'incorrect':
       # reward correct action
      self.actions[idx_action] = (self.actions[idx_action][0],self.actions[idx_action][1]+harsh_punishment)
      # punish incorrect action
      for i in range(len(self.actions)):
        if i != idx_action:
          if idx_action/2 and i/2:
            self.actions[i]= (self.actions[i][0],self.actions[i][1]+reward)
          else: 
            self.actions[i]= (self.actions[i][0],self.actions[i][1]+reg_punishment)      
    print(self.actions)



    

  def move_agent(self,agent_pos):
    decision = []
    decision[:] = self.actions
    print(decision)
    print(len(decision))
    if agent_pos[0] == 0:
      del decision[2]
      del decision[4]
      del decision[5]
    elif agent_pos[0] == (self.dim-1):
      del decision[1]
      del decision[3]
      del decision[4]
    if agent_pos[1] == 0:
      del decision[0]
      del decision[0]
      del decision[0]
    elif agent_pos[1] == (self.dim-1):
      if (agent_pos[0] == 0):
        del decision[2]
        del decision[2]
      elif agent_pos[0] == (self.dim-1):
        del decision[2]
        del decision[2]
      else:
        del decision[3]
        del decision[3]
        del decision[3]

    weighted_decision = []
    # weight random selection
    for element in decision:
      weighted_decision += [element[0]] * int(element[1] * 100)
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
                     [(MARGIN + square_length) * x + MARGIN,
                      (MARGIN + square_length) * y + MARGIN,
                      square_length,
                      square_length])



if __name__ == '__main__':
  gn = GridNavigate(6)



