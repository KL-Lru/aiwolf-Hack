#!/usr/bin/env python
import aiwolfpy.contentbuilder as cb
from playmodel.role.common15 import Common
from lib.talknode import Node

class Medium(Common):
  def __init__(self, game_info, game_setting):
    super().__init__(game_info, game_setting)
    self.comingout_role = ''
    self.reported = False
    self.ability_result = ''
    self.talkQueue.push(Node(100, cb.comingout(self.idx, "MEDIUM")))
  # end def init

  def update(self, game_info, history, request, breakdown):
    super().update(game_info, history, request, breakdown)
    if request == 'DAILY_INITIALIZE':
      for i in range(history.shape[0]):
        if history['type'][i] == 'identify':
          self.reported = False
          self.ability_result = history['text'][i]
          print("ab: " + self.ability_result)
          text = history['text'][i].split()
          dst = self.getAgentIdx(text[1])
          species = text[2]
          if species == "WEREWOLF":
            breakdown.updateDeterministic(dst, 1)
          else:
            breakdown.updateAttacked(dst)
      if self.ability_result != '':
        self.talkQueue.push(Node(100, self.ability_result))    
    poss, wolfs, scores= breakdown.getTop()
    if poss[0] != 0:
      wolfs = sorted(wolfs, key=lambda x: scores[int(x), 1])
      self.tar = wolfs[-1]
      self.hold = wolfs[0]
      if game_info['day'] != 0:
        if scores[wolfs[-1], 1] > 1.15 and not self.voted and self.skcnt < 2:
          self.talkQueue.push(Node(10 * scores[wolfs[-1], 1] ,cb.vote(self.tar)))    
          self.voted = True
        if scores[wolfs[-1], 1] > 1.1 and not self.requested and self.skcnt < 2:
          self.talkQueue.push(Node(20 * scores[wolfs[0], 1],cb.request(cb.request_div(self.hold))))
          self.requested = True
        if scores[wolfs[-1], 1] > 1.0 and not self.estimated and self.skcnt < 2:
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
#end def Medium