#!/usr/bin/env python
import aiwolfpy.contentbuilder as cb
from playmodel.role.common5 import Common
from lib.talknode import Node

class Seer(Common):
  def __init__(self, game_info, game_setting):
    super().__init__(game_info, game_setting)
    self.reported = False
    self.ability_result = ''
    self.talkQueue.push(Node(150, cb.comingout(self.idx, "SEER")))
  #end def init

  def update(self, game_info, history, request, breakdown):
    super().update(game_info, history, request, breakdown)
    if request == 'DAILY_INITIALIZE':
      for i in range(history.shape[0]):
        if history['type'][i] == 'divine':
          self.reported = False
          self.ability_result = history['text'][i]
          print("ab: "+self.ability_result)
          text = history['text'][i].split()
          dst = self.getAgentIdx(text[1])
          species = text[2]
          if species == "WEREWOLF":
            breakdown.updateDeterministic(dst, 2)
          else:
            breakdown.updateAttacked(dst)
      if self.ability_result != '':
        self.talkQueue.push(Node(100, self.ability_result))
    if game_info['day'] != 0:
      poss, wolf, seer, scores= breakdown.getTop()
      if poss[0] != 0:
        wolf = wolf[0]
        seer = seer[0]
        poss = poss[0]
        if scores[wolf, 2] > 1.05 and not self.voted and self.skcnt < 2:
          self.talkQueue.push(Node(10 * scores[wolf, 2] ,cb.vote(self.tar)))    
          self.voted = True
        if scores[wolf, 2] > 1.02 and not self.estimated and self.skcnt < 2:
          self.talkQueue.push(Node(30,cb.estimate(wolf, "WEREWOLF")))
          self.estimated = True
  #end def update

  def dayStart(self):
    super().dayStart()
  #end def dayStart

  def talk(self):
    return super().talk()
  # end def talk

  def vote(self):
    return self.tar
  # end def vote
  
  def divine(self):
    return self.hold
  # end def divine
# end def Seer