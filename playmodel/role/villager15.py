#!/usr/bin/env python
import aiwolfpy.contentbuilder as cb
import re
from lib.talknode import Node
from playmodel.role.common15 import Common

class Villager(Common):
  def __init__(self, game_info, game_setting):
    super().__init__(game_info, game_setting)
  # end def init

  def getAgentIdx(self, text):
    return super().getAgentIdx(text)

  def update(self, game_info, history, request, breakdown):
    super().update(game_info, history, request, breakdown)
    poss, wolfs, scores= breakdown.getTop()
    wolfs = sorted([x for x in wolfs if x not in self.deadlist], key=lambda x: scores[int(x), 1])
    
    self.tar = wolfs[-1]
    self.hold = wolfs[0]
    if game_info['day'] != 0:
      if scores[wolfs[-1], 1] > 1.15 and not self.voted and self.skcnt < 2:
        self.talkQueue.push(Node(10 * scores[wolfs[-1], 1] ,cb.vote(self.tar)))    
        self.voted = True
      if self.tar != self.hold and self.skcnt < 2:
        if scores[wolfs[-1], 1] > 1.1 and not self.requested:
          self.talkQueue.push(Node(20 * scores[wolfs[0], 1],cb.request(cb.request_div(self.hold))))
          self.requested = True
        if scores[wolfs[-1], 1] > 1.0 and not self.estimated:
          self.talkQueue.push(Node(30,cb.estimate(wolfs[1], "WEREWOLF")))
          self.estimated = True
  # end def update

  def dayStart(self,breakdown):
    super().dayStart(breakdown)
  #end def dayStart

  def talk(self):
    return super().talk()
  # end def talk
  
  def vote(self):
    return self.tar
  # end def vote
#end def Villager