import pygame
from random import randint
import os
import sys
import time
from pylsl import StreamInfo, StreamOutlet


BLACK = (0,0,0)
WHITE = (255,255,255)

WIDTH = 1000
HEIGHT = 1000

class FlankerTask():
  def __init__(self,calib):
    # screen
    self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption("Flanker Task")

    # LSL setup
    info_correct = StreamInfo('correctness','Markers',1, 0,'string','markerstream2')
    self.outlet_correct = StreamOutlet(info_correct)
    self.markers = ['Correct','Incorrect']
    # start task
    if calib:
      for i in range(4):
        time.sleep(15)
        self.start_task(True)
    else:
      info_button = StreamInfo('button_presses','Markers',1, 0,'string','markerstream1')
      self.outlet_button = StreamOutlet(info_button)
      self.start_task(False)

  def start_task(self,calib):
    options = [pygame.K_LEFT, pygame.K_RIGHT]
    count=0
    while count<20:
      self.screen.fill(BLACK) 
      pygame.display.flip()
      time.sleep(1)
      direction = self.draw_arrows()
      pygame.display.flip()
      pygame.event.set_allowed(None)
      pygame.event.set_allowed(pygame.KEYDOWN)
      pygame.event.clear(pygame.KEYDOWN)
      event = pygame.event.wait()
      pygame.event.set_blocked(pygame.KEYDOWN)
      if not calib:
        self.outlet_button.push_sample(['Button'])
      if event.type == pygame.KEYDOWN and event.key in options:
        if event.key == pygame.K_LEFT:
          user_input = 1
        elif event.key == pygame.K_RIGHT:
          user_input = 0
        if user_input == direction:
          print(self.markers[0])
          self.outlet_correct.push_sample([self.markers[0]])
        elif user_input == (direction ^ 1):
          print(self.markers[1])
          self.outlet_correct.push_sample([self.markers[1]])
        pygame.event.set_blocked(pygame.KEYDOWN)
        count+=1
      pygame.event.pump()
    if not calib: 
      self.outlet_correct.push_sample(['End'])


  def draw_arrows(self):
    stim_type = randint(0,1)    # arrow group incongruent, congruent, or neutral
    direction = randint(0,1)    # choose direction (left or right)
    segment = WIDTH/5
    flanker_coord = [(50,HEIGHT/2 - 50), (250, HEIGHT/2 - 50), (650, HEIGHT/2 -50), (850, HEIGHT/2 - 50)]
    right_arrow = pygame.transform.scale(pygame.image.load('arrow.png'), (150,100))
    left_arrow = pygame.transform.flip(right_arrow,1,0)
    arrows = [right_arrow, left_arrow]
    # DRAW
    ## central arrow:
    self.screen.blit(arrows[direction],(450, HEIGHT/2 - 50))
    if stim_type == 0:
      flank_dir = (direction ^ 1)
    elif stim_type == 1:
      flank_dir = direction

    # flanker arrows
    for coord in flanker_coord:
      self.screen.blit(arrows[flank_dir],coord)
    return direction


if __name__ == '__main__':
  calib = False
  if len(sys.argv) > 1 and sys.argv[1] == '--calib':
    calib = True
  ft = FlankerTask(calib)
  
