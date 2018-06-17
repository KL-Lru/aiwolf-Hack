#!/usr/bin/env python
import aiwolfpy.contentbuilder as cb
from playmodel.role.common5 import Common
from lib.talknode import Node

class Possessed(Common):
  def __init__(self, game_info, game_setting):
    super().__init__(game_info, game_setting)
    self.comingout_role = ''
    self.reported = False
    self.ability_result = ''
    self.talkQueue.push(Node(100, cb.comingout(self.idx, "SEER")))
  # end def init

  def update(self, game_info, history, request,breakdown):
    super().update(game_info, history, request, breakdown)
    if game_info['day'] != 2:
      if request == 'DAILY_INITIALIZE' and game_info['day'] != 0:
        self.reported = False
        self.ability_result = cb.divined(self.tar, "HUMAN")
      poss, wolf, seer, scores= breakdown.getTop()
      human = [x for x in range(1, 6) if x not in wolf and x not in self.deadlist and x != self.idx]
      human.sort(key = lambda x: scores[int(x), 0])
      self.tar = human[-1]
      self.hold = human[0]
      if game_info['day'] != 0:
        if not self.reported:
          self.talkQueue.push(Node(100, self.ability_result))
          self.reported = True
        if scores[human[0], 0] < 1.05 and not self.voted and self.skcnt < 2:
          self.talkQueue.push(Node(10 * scores[human[0], 2] ,cb.vote(self.hold)))    
          self.voted = True
        if scores[human[-1], 2] > 1.1 and not self.requested and len(human) >= 2 and self.skcnt < 2:
          self.talkQueue.push(Node(20 * scores[human[1], 2],cb.divine(human[1])))
          self.requested = True
        if scores[human[-1], 2] > 1.0 and not self.estimated and self.skcnt < 2:
          self.talkQueue.push(Node(30,cb.estimate(human[0], "WEREWOLF")))
          self.estimated = True
    else :
      self.talkQueue.push(Node(100, cb.comingout(self.idx, "POSSESSED")))
      poss, wolf, seer, scores= breakdown.getTop()
      self.tar = [x for x in range(1, 6) if x not in wolf and x not in self.deadlist][0]
      self.talkQueue.push(Node(100, cb.vote(self.tar)))
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
# end def Possessed