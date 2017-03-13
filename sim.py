from heapq import heappop, heappush
import copy
import math
import matplotlib.pyplot as plt

#########################################################################################

class NoEventError(Exception):
  pass


class Environment(object):
  """Parent environment used to run Discrete Event Simulations"""
  def __init__(self):
    self.time_elapsed = 0
    self.event_queue = []
    
  def add_event(self, eventfunc, time, message="some"):
    # Events are just functions. When the function is executed, the event is done
    # Time is relative- an event with time=5 added at time_elapsed=2 will occur at time_elapsed=7
    heappush(self.event_queue, (time, eventfunc, message))
    
  def add_fixed_event(self, eventfunc, time, message="some"):
    # Adds an event at an absolute time - not relative
    self.add_event(eventfunc, time-self.time_elapsed, message)
    
  def do_next_event(self):
    # Pop the soonest event off the heap and run it
    # Decrease the time of all the other events
    try:
      time, eventfunc, message = heappop(self.event_queue)
      assert time > 0
      self.time_elapsed += time
      print("Executing {} event at time {}".format(message, self.time_elapsed))
      eventfunc()
      self.event_queue = [(t-time, e, m) for t,e,m in self.event_queue]
    except IndexError:
      print("No events left in queue")
      raise NoEventError()
      
  def run(self):
    # Run events until there are no more in the queue
    while True:
      try:
        self.do_next_event()
      except NoEventError:
        break

  def run_till_time(self, time):
    # Run till total time elapsed is greater than TIME
    while self.time_elapsed < time:
      self.do_next_event()

#########################################################################################


class Car(object):
  """web enabled car"""
  def __init__(self, source, destination, label, sg, speed):
    self._source = source
    self._destination = destination
    self._label = label
    # Parent street graph this car cruises on
    self._sg = sg
    self._speed = speed
    self._calculate_route()

  def set_speed(self, speed):
    self._speed = speed

  def _calculate_route(self):
    route = self._sg.shortest_path(self._source, self._destination)
    route.pop(0)
    self._route = route
    self._update_next_dest()

  def _update_next_dest(self):
    self._next_dest = self._route.pop(0)

  def drive(self):
    return null
    
#########################################################################################

class Node(object):
  """Simple node in a graph containing a label, x + y coordinates for drawing, and a neighbors map"""
  def __init__(self, x, y, label):
    self._x = x
    self._y = y
    self._label = label
    self._neighbors = {}
    
  def __repr__(self):
    return self._label

  def add_neighbor(self, other, dist = 1):
    assert isinstance(other, Node)
    assert other not in self._neighbors
    self._neighbors[other] = dist

  def neighbors(self):
    return self._neighbors.items()


class EuclideanNode(Node):
  """Node in a graph representing a single street intersection. Calculates Euclidian distance between other's x and y"""
  def __init__(self, *args):
    super(self).__init__(*args)

  def add_neighbor(self, other):
    assert isinstance(other, Node)
    assert other not in self.neighbors
    self._neighbors[other] = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)


class ManhattanNode(Node):
  """Node in a graph representing a single street intersection. Calculates Manhattan distance between other's x and y"""
  def __init__(self, *args):
    super(self).__init__(*args)

  def add_neighbor(self, other):
    assert isinstance(other, Node)
    assert other not in self.neighbors
    self._neighbors[other] = math.abs(self.x - other.x) + math.abs(self.y - other.y)


class StreetGraph(object):
  """Graph class containing information and methods related to roadways"""
  def __init__(self, nodeCls = Node, carCls = Car):
    self._nodes = set()
    self._cars = set()
    self._nodeCls = nodeCls
    self._carCls = carCls

  def add_car(self, origin, destination, label, speed = 1):
    delorian = self._carCls(origin, destination, label, self, speed)
    self._cars.add(delorian)
    return delorian

  def add_node(self, x, y, label):
    node = self._nodeCls(x, y, label)
    self._nodes.add(node)

  def add_edge(self, label1, label2, distance):
    node1 = self._node_from_label(label1)
    node2 = self._node_from_label(label2)
    if not node1 or not node2:
      return
    node1.add_neighbor(node2)
    node2.add_neighbor(node1)

  def _node_from_label(self, label):
    for n in self._nodes:
      if n._label == label:
        return n
    return None

  def shortest_path(self, label1, label2):
    # Returns a list of labels corresponding to the shortest path from label1 to label2 and the total distance
    s = self._node_from_label(label1)
    t = self._node_from_label(label2)
    if not s or not t:
      return

    dist = {}
    prev = {}

    for n in self._nodes:
      dist[n] = math.inf
      prev[n] = None

    dist[s] = 0

    Q = copy.copy(self._nodes)
    while Q:
      # O(n^2) time because I'm a piece of human garbage
      _, smallest = min([ (dist[n], n) for n in Q ], key = lambda x: x[0])
      Q.remove(smallest)
      for neighbor, ndist in smallest.neighbors():
        newdist = dist[smallest] + ndist
        if newdist < dist[neighbor]:
          dist[neighbor] = newdist
          prev[neighbor] = smallest

    path = []
    bt = t
    while bt:
      path.insert(0, bt._label)
      bt = prev[bt]
      
    print(dist)
    print(prev)

    return path, dist[t]
      
#########################################################################################


g = StreetGraph()
g.add_node(0, 0, 'A')
g.add_node(0, 1, 'B')
g.add_node(1, 1, 'C')
g.add_edge('A', 'B', 1)
g.add_edge('B', 'C', 1)
print(g.shortest_path('A', 'C'))

"""Vehicle Simulations"""
#car1 = Car((0,0),(5,5),'car1',g,3)

GRAPHSIZE = 10
ticks = range(0, GRAPHSIZE + 1)
x = [1,6,8,1,0,3,6,3,5]
y = [1,3,5,6,2,7,0,3,1]
plt.hold(True)


def checkEuc(i, xlist, ylist, r):
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

plt.plot(x, y, 'bo')
plt.grid(b = True)
plt.xticks(ticks)
plt.yticks(ticks)
plt.xlim(0, GRAPHSIZE)
plt.ylim(0, GRAPHSIZE)
checkEuc(4, x, y, 6)
plt.show()


