from src.discrete import Environment
from src.components import Car, StreetGraph, EuclideanNode
import matplotlib.pyplot as plt
import math
import imageio 


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

	
#plt.plot(x, y, 'bo')

#ALL THIS NEEDS TO BE IN EVERY PLOT
#GRAPHSIZE = 10
#ticks = range(0, GRAPHSIZE + 1)
#x = [1,6,8,1,0,3,6,3,5]
#y = [1,3,5,6,2,7,0,3,1]
#plt.hold(True)

#plt.grid(b = True)
#plt.xticks(ticks)
#plt.yticks(ticks)
#plt.xlim(0, GRAPHSIZE)
#plt.ylim(0, GRAPHSIZE)
#drawNodes(4, x, y, 6)


#Testing Car Unit 
g = StreetGraph()
g.add_node(3, 0, 'A')
g.add_node(2, 12, 'B')
g.add_node(4, 7, 'C')
g.add_edge('A', 'B', 10)
g.add_edge('C', 'B', 10)

ferrari = Car('A', 'B', 'ferrari', g, 1.25, 6)
toyota = Car('A', 'B', 'toyota', g, 1, 6)
honda = Car('C' , 'B', 'honda', g, .6, 6)
g.add_car(ferrari)
g.add_car(toyota)
g.add_car(honda)
# ferrari = g.add_car('A', 'B', 'One fast car', 0.5)
# f2 = g.add_car('A', 'B', 'blah2', 1)

numIter = 6 #number of driving iterations
GRAPHSIZE = 15
images = []

for i in range(numIter):
  plt.figure(i)
  ticks = range(0, GRAPHSIZE + 1)
  plt.hold(True)
  plt.grid(b = True)
  plt.xticks(ticks)
  plt.yticks(ticks)
  plt.xlim(0, GRAPHSIZE)
  plt.ylim(0, GRAPHSIZE)

  xlist = []
  ylist = []

  for c in g._cars:
      x, y = c.position()
      xlist.append(x)
      ylist.append(y)
      plt.plot(x, y, 'bo')
      drawNodes(0, xlist,ylist, c.getRad())
      c.drive()

  filename = 'fig' + str(i) + '.png'
  plt.savefig(filename)
  images.append(imageio.imread(filename))

setLinkLife(g)
exportname = "movie.gif"
kargs = { 'duration': 2 }
imageio.mimsave(exportname, images, 'GIF', **kargs)


 









