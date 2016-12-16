import pygame
import random
import time

#ENVIRONMENTAL VARIABLES FOR GAME
#colors
BLACK = (0,0,0)     	# background
WHITE = (255,255,255) # agent
GREEN = (0, 255, 0)   # goal
RED = (255, 0, 0)     # mistake

# screen
width = 1000
height = 1000
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Simple Error Task")
# recentangle side length:
length = 80

# Positions of goal [x1,y1, x2,y2]
TOP = [rect_x - length/2, 0, length,length]
BOTTOM = [rect_x - length/2, height-length, length,length]
RIGHT = [width - length, rect_y - length/2, length, length]
LEFT = [0, rect_y - length/2, length, length]
positions = [TOP, BOTTOM, RIGHT, LEFT]

# Starting position of the rectangle
rect_x = width / 2
rect_y = height / 2
initial_pos = [rect_x - length/2, rect_y - length/2, length, length]

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

class Environment():
	def __init__(self):

		# Loop until the user clicks the close button.
		self.done = False
		 
	def run(self):
		# -------- Main Program Loop -----------
		while not done:
			# --- Event Processing
			for event in pygame.event.get():
					if event.type == pygame.QUIT:
							done = True

			#temporary: randomly pick the goal
			goal = positions[0]
			action = positions[random.randint(0,3)]
			current_pos = initial_pos[:]

			screen.fill(BLACK)	
			pygame.draw.rect(screen, WHITE, current_pos) 	#agent
			pygame.draw.rect(screen, GREEN, goal)				#goal
			pygame.display.flip()
			time.sleep(1)
			while current_pos not in positions:
				# Set the screen background
				screen.fill(BLACK)

				# Draw the rectangles
				pygame.draw.rect(screen, WHITE, current_pos) 	#agent
				pygame.draw.rect(screen, GREEN, goal)				#goal

				# --- Wrap-up
				# Limit to 60 frames per second
				clock.tick(60)

				# next position:
				for i, (a,b) in enumerate(zip(action,current_pos)):
					if a-b > 0:
						current_pos[i] += 10
					elif a-b < 0:
						current_pos[i] -= 10
				pygame.display.flip()

			# draw the last frame of the trial
			screen.fill(BLACK)	
			pygame.draw.rect(screen, WHITE, current_pos) 	#agent
			pygame.draw.rect(screen, GREEN, goal)				#goal
			pygame.display.flip()
			time.sleep(.5)

 		self.exit()

 	def exit(self):
		# Close everything down
		pygame.display.quit()
		pygame.quit()


env = Environment()
env.run()