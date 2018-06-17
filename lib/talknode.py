class Node(object):
  def __init__(self, score, text):
    self.score = score
    self.text = text
  
  def __str__(self):
    return "%l: %s" % (self.score, self.text)
  
  def __lt__(self, other):
    return self.score > other.score

