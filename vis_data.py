import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from mpl_toolkits.axes_grid.axislines import SubplotZero
def vector(dataset):
  fig = plt.figure(1)

  a =np.array([0,0,3,2])
  ax = SubplotZero(fig,111)
  fig.add_subplot(ax)
#  for direction in ["xzero", "yzero"]:
#    ax.axis[direction].set_axisline_style("-|>")
#    ax.axis[direction].set_visible(True)
#  plt.locator_params(nbins=0)
#  plt.axis('equal')
  for direction in ["left", "right", "bottom", "top"]:
    ax.axis[direction].set_visible(False)
#  ax.axis('off')
  
    
  n = [0,0,0,dataset[0]]
  ne = [0,0,dataset[1]*np.cos(0.785398), dataset[1]*np.sin(0.785398)]
  e = [0,0,dataset[2],0]
  se = [0,0,dataset[3]*np.cos(0.785398),-1*dataset[3]*np.sin(0.785398)]
  s = [0,0,0,-1*dataset[4]]
  sw = [0,0,-1*dataset[5]*np.cos(0.785398),-1*dataset[5]*np.sin(0.785398)]
  w = [0,0,-1*dataset[6],0]
  nw =[0,0,-1*dataset[7]*np.cos(0.785398),dataset[7]*np.sin(0.785398)]
  X,Y,U,V = zip(*np.array([n,ne,e,se,s,sw,w,nw]))
  ax.quiver(X,Y,U,V, units='xy',scale=1)
  ax.set_xlim([-.75,.75])
  ax.set_ylim([-.75,.75])
  plt.draw()
  plt.show()

