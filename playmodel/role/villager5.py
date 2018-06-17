#!/usr/bin/env python
import aiwolfpy.contentbuilder as cb
from playmodel.role.common5 import Common
from lib.talknode import Node

class Villager(Common):
  def __init__(self, game_info, game_setting):
    super().__init__(game_info, game_setting)
  # end def init

  def update(self, game_info, history, request, breakdown):
    super().update(game_info, history, request, breakdown)
    poss, wolf, seer, scores= breakdown.getTop()
    wolf = wolf[0]
    seer = seer[0]
    poss = poss[0]
    self.tar = wolf
    self.hold = poss
    if game_info['day'] != 0:
      if scores[wolf, 2] > 1.02 and not self.voted and self.skcnt < 2:
        self.talkQueue.push(Node(10 * scores[wolf, 2] ,cb.vote(self.tar)))
        self.voted = True
      if scores[wolf, 2] > 1.01 and not self.requested and self.skcnt < 2:
        self.talkQueue.push(Node(20 * scores[wolf, 2],cb.request(cb.request_div(self.hold))))
        self.requested = True
      if scores[wolf, 2] > 1.0 and not self.estimated and self.skcnt < 2:
        self.talkQueue.push(Node(30,cb.estimate(wolf, "WEREWOLF")))
        self.estimated = True
  # end def update

  def dayStart(self):
    super().dayStart()
  #end def dayStart

  def talk(self):
    return super().talk()
  # end def talk
      
  def vote(self):
    return self.tar
  # end def vote
# end def Villager