from src.discrete import Environment
from src.components import Car, StreetGraph, EuclideanNode

import math
import matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot as plt, animation
import imageio
import os


"""Vehicle Simulations"""

def drawNodes(i, xlist, ylist, r):
  carx = xlist[i]
  cary = ylist[i]
  for j in range(len(xlist)):
    if i == j:
      continue
    deltaX = carx - xlist[j]
    deltaY = cary - ylist[j]
    dist = math.sqrt(deltaX**2 + deltaY**2)
    if dist <= r:
      plt.plot([carx, xlist[j]], [cary, ylist[j]] ,'r')
      xavg = (carx + xlist[j])/2
      yavg = (cary + ylist[j])/2
      plt.text(xavg,yavg, r'' + str(round(dist,2)))
    else:
      pass
  return

def setLinkLife(sGraph):
	# Sets Link Life of car (edges)
	assert isinstance(sGraph, StreetGraph)
	for c in sGraph._cars:
		c.resetLink()
		x, y = c.position()
		for ci in sGraph._cars:
			xi, yi = ci.position()
			dX = x - xi
			dY = y - yi
			dist = math.sqrt(dX**2 + dY**2)
			if (c == ci) | (dist > c.getRad()):
				continue
			else:
				linkVal = detLinkLife(c, ci, sGraph)
				c.setLinkLife(ci, linkVal)
				#printout = c.getLinkLife(ci)
				#print(printout)


def getVel(car, sGraph):
	x, y = car.position()
	sp = car.getSpeed()
	dest_x, dest_y = sGraph.get_xy_coords(car.getNextNode())
	vx1 = dest_x - x
	vy1 = dest_y - y
	vnorm1 = math.sqrt(vx^2 + vy^2)
	vel_x = vx / vnorm1 * sp
	vel_y = vy / vnorm1 * sp
	return vel_x, vel_y

def quadratic(a, b, c):
  d = (b**2) - (4*a*c)
  sol1 = (-b-sqrt(d))/(2*a)
  sol2 = (-b+sqrt(d))/(2*a)
  return sol1, sol2

def detLinkLife(car1, car2, sGraph):
  a_x, a_y = car1.position()
  b_x, b_y = car2.position()
  av_x, av_y = getVel(A, sGraph)
  bv_x, bv_y = getVel(B, sGraph)
  a = a_x - b_x
  b = a_y - b_y
  c = av_x - bv_x
  d = av_x - bv_y
  
  c_0 = a^2 + b^2 - car1.getRad()^2
  c_1 = 2*a*c + 2*b*d
  c_2 = c^2 + d^2
  
  try:
    return max(quadratic(c_2, c_1, c_0))
  except ZeroDivisionError:
    return inf
	#return linkVal

#Testing Car Unit 
g = StreetGraph(nodeCls = EuclideanNode)
g.add_node(1, 1, 'A')
g.add_node(11, 1, 'B')
g.add_node(11, 11, 'C')
g.add_node(1, 11, 'D')
g.add_edge('A', 'B')
g.add_edge('C', 'B')
g.add_edge('D', 'C')
g.add_edge('A', 'D')
ferrari = g.add_car('A', 'D', 'One fast car', 0.1)
f2 = g.add_car('C', 'A', 'blah2', .17)

numIter = 200 #number of driving iterations

images = []
with imageio.get_writer("movie.gif", 'GIF', mode='I', duration=.1,) as writer:
  GRAPHSIZE = 15
  ticks = range(0, GRAPHSIZE + 1)
  plt.hold(True)
  plt.grid(b = True)
  plt.xticks(ticks)
  plt.yticks(ticks)
  plt.xlim(0, GRAPHSIZE)
  plt.ylim(0, GRAPHSIZE)

  for i in range(numIter):
    print("Generating frame {}".format(i))
    
    xlist = []
    ylist = []

    for c in g._cars:
        x, y = c.position()
        xlist.append(x)
        ylist.append(y)
        plt.plot(x, y, 'bo')
        drawNodes(0, xlist,ylist, 3)
        try:
          c.drive()
        except:
          pass

    filename = 'fig' + str(i) + '.png'
    plt.savefig(filename)
    plt.clf()

    kargs = { }
    writer.append_data(imageio.imread(filename), **kargs)
    os.remove(filename)







