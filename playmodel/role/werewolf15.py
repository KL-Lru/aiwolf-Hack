#!/usr/bin/env python
import aiwolfpy.contentbuilder as cb
from playmodel.role.common15 import Common
from lib.talknode import Node
class Werewolf(Common):
  def __init__(self, game_info, game_setting):
    super().__init__(game_info, game_setting)
    self.comingout_role = ''
    self.reported = False
    self.ability_result = ''
    self.attar = 1 if self.idx != 1 else 2
    self.tar = 1 if self.idx != 1 else 2
  # end def init

  def update(self, game_info, history, request, breakdown):
    super().update(game_info, history, request, breakdown)
    poss, wolfs, scores= breakdown.getTop()
    if poss[0] != 0:
      human = [x for x in range(1,16) if x not in wolfs and x not in self.deadlist]
      human.sort(key = lambda x: scores[x][0])
      self.tar = human[-1]
      self.hold = human[0]
      if game_info['day'] != 0:
        if scores[human[0], 1] > 1.2 and not self.voted and self.skcnt < 2:
          self.talkQueue.push(Node(10 * scores[human[0], 1] ,cb.vote(self.hold)))
          self.voted = True
        if len(human) >= 2 and scores[human[1], 1] > 1.1 and not self.requested and self.skcnt < 2:
          self.talkQueue.push(Node(20 * scores[human[1], 1], cb.request(cb.request_div(human[1]))))
          self.requested = True
        if scores[human[0], 1] > 1.0 and not self.estimated and self.skcnt < 2:
          self.talkQueue.push(Node(30,cb.estimate(human[0], "WEREWOLF")))
          self.estimated = True
  # end def update

  def dayStart(self,breakdown):
    super().dayStart(breakdown)
  #end def dayStart

  def talk(self):
    return super().talk()
  # end def talk
  
  def whisper(self):
    # not whispe
    return cb.over()
  # end def whisper
      
  def vote(self):
    return self.hold
  # end def vote
  
  def attack(self):
    return self.tar
  # end def attack
# end def Werewolf