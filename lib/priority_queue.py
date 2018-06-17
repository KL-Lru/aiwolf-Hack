from heapq import heappush, heappop

class PriorityQueue(object):
  def __init__(self):
    self.queue = []
  
  def __len__(self):
    return len(self.queue)

  def push(self, node):
    heappush(self.queue, node)
  
  def pop(self):
    return heappop(self.queue)

  def clear(self):
    self.queue = []
  