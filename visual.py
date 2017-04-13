from src.discrete import Environment
from src.components import Car, StreetGraph, EuclideanNode
import matplotlib.pyplot as plt
import math
import imageio 


"""Vehicle Simulations"""
#car1 = Car((0,0),(5,5),'car1',g,3)


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
				#pritnout = c.getLinkLife(ci)
				#print(pritnout)
		return
	return


def detLinkLife(car1, car2, sGraph):
	# Joy is implenting this part.
	return 5
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
g.add_node(4,7, 'C')
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

images = []

for i in range(numIter):
  plt.figure(i)
  GRAPHSIZE = 15
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


 









