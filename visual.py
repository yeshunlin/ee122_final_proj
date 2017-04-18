from src.discrete import Environment
from src.components import Car, StreetGraph, EuclideanNode, RoutingGraph

import math
import matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot as plt, animation
import imageio
import os
import random

"""Vehicle Simulations"""

"""
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
      plt.text(xavg,yavg, str(round(dist,2)))
    else:
      pass
  return
  """

def drawNodes(sGraph):
	assert isinstance(sGraph, StreetGraph)
	xlist = []
	ylist = []
	rlist = []
	for c in sGraph._cars: #takes all car positions into a list
		x, y = c.position()
		radius = c.getRad()
		xlist.append(x)
		ylist.append(y)
		rlist.append(radius)
	if len(xlist) != 0: #if nonempty
		i = 0
		carx = xlist[i]
		cary = ylist[i]
	else:
		return

	for i in range(len(xlist)): #we are looking at the i-th car
		for j in range(len(xlist)): #run through all j to plot relationship with i
			if i == j: #if equal, don't do anything
				continue
			deltaX = carx - xlist[j]
			deltaY = cary - ylist[j]
			dist = math.sqrt(deltaX**2 + deltaY**2)
			if dist <= rlist[i]:
				plt.plot([carx, xlist[j]], [cary, ylist[j]] ,'r', mew = 3)
				xavg = (carx + xlist[j])/2
				yavg = (cary + ylist[j])/2
				#plt.text(xavg,yavg, str(round(dist,2)))  ##replace as LinkLife 
				carx = xlist[i]
				cary = ylist[i]
			else:
				pass


def drawRoads(sGraph):
	assert isinstance(sGraph, StreetGraph)
	for n in sGraph._nodes:
		x, y = n.position()
		for neighbor in n._neighbors:
			nbr_x, nbr_y = neighbor.position()
			plt.plot([x, nbr_x], [y, nbr_y], 'c-', alpha = 0.6, linewidth = 3)

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
  av_x, av_y = getVel(car1, sGraph)
  bv_x, bv_y = getVel(car2, sGraph)
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
g.add_node(1, 1, '0')
g.add_node(10, 1, '1')
g.add_node(10, 10, '2')
g.add_node(1, 10, '3')
g.add_node(10, 20, '4')
g.add_node(1, 20, '5')
g.add_node(20, 1, '6')
g.add_node(20, 10, '7')
g.add_node(20, 20, '8')
g.add_edge('0', '2')
g.add_edge('2', '8')

def genEdge(sGraph):
	xcoord = []
	ycoord = []
	xdict = dict()
	ydict = dict()
	label = []
	for n in g._nodes:
		x, y = n.position()
		xcoord.append(x)
		ycoord.append(y)
		label.append(n.label())
	for i in range(0, len(xcoord)):
		if xcoord[i] not in xdict.keys():
			xdict[xcoord[i]] = list()

		if ycoord[i] not in ydict:
			ydict[ycoord[i]] = list()

		xdict[xcoord[i]].append(label[i])
		ydict[ycoord[i]].append(label[i])

	for k, v in xdict.items():
		print('keys: ' + str(k))
		print('values: ' + str(len(v)))
		if len(v) == 1:
			pass
		else:
			for i in range(0, len(v)):
				for j in range(0, len(v)):
					if i == j:
						pass
					else:
						sGraph.add_edge(v[i], v[j])
	for k, v in ydict.items():
		if len(v) == 1:
			pass
		else:
			for i in range(0, len(v)):
				for j in range(0, len(v)):
					if i == j:
						pass
					else:
						sGraph.add_edge(v[i], v[j])




#g.add_edge('0', '1')
#g.add_edge('1', '2')
#g.add_edge('2', '3')
#g.add_edge('3', '0')



#randomly generate n (= 20) (super connected) nodes in a 20 x 20 graph
"""def genNodes(sGraph, num_nodes, dimX, dimY):
	nodes  = []
	for i in range(0, num_nodes):
		x_rand = random.randint(0, dimX)
		y_rand = random.randint(0, dimY)
		sGraph.add_node(x_rand, y_rand, str(i))
		nodes.append(str(i))
		for j in nodes:
			if j == str(i):
				break
			print('this is j ' + j)
			conn = random.randint(0, int(j))
			while conn == str(i):
				conn = random.randint(0, int(j))
			print(conn)
			sGraph.add_edge(str(i), str(conn))"""


#randomly generate 10 cars with variable speeds 0 < s < 1 and super connected links
def genCars(sGraph, num_cars, num_nodes):
	for i in range(0, num_cars):
		rand_sta = random.randint(0, num_nodes - 1)
		rand_end = random.randint(0, num_nodes - 1)
		rand_spe = random.random()
		rand_rad = random.randint(3, 6) #rand radius between 0 and 10
		sGraph.add_car(Car(str(rand_sta), str(rand_end), str(i), g, rand_spe, rand_rad))

#randomly generate 10 cars with variable speeds 0 < s < 1 and selectively connected links
#links are connected to the n + 1 & n + 2, & also all links within nodal radius nr



numIter = 50 #number of driving iterations

images = []
with imageio.get_writer("movie.gif", 'GIF', mode='I', duration=.2,) as writer:
  plt.hold(True)
  genEdge(g)
  #genNodes(g, 5, 20, 20)
  genCars(g, 30, len(g._nodes))

  for i in range(numIter):
    print("Generating frame {}".format(i))
    drawRoads(g)
    node_x = []
    node_y = []
    node_label = []
    for n in g.get_nodes():
      x, y = n.position()
      node_x.append(x)
      node_y.append(y)
      node_label.append(n.label())
      plt.plot(node_x, node_y, 'go')

    for i in range(len(node_label)):
      plt.text(node_x[i], node_y[i], node_label[i]) 

    g_size = max(max(node_x) + 1, max(node_y) + 1)
    ticks = range(0, g_size + 1)
    plt.grid(b = True)
    plt.xticks(ticks)
    plt.yticks(ticks)
    plt.xlim(0, g_size)
    plt.ylim(0, g_size)

    xlist = []
    ylist = []

    drawNodes(g)

    for c in g._cars:
      x, y = c.position()
      xlist.append(x)
      ylist.append(y)
      plt.plot(x, y, 'bo')
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







