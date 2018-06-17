#!/usr/bin/env python
import aiwolfpy.contentbuilder as cb
from playmodel.role.common15 import Common
from lib.talknode import Node

class Bodyguard(Common):
  def __init__(self, game_info, game_setting):
    super().__init__(game_info, game_setting)
    self.comingout_role = ''
    self.comingout = False
    self.reported = False
    self.ability_result = ''
    self.guardtar = 1 if self.idx != 1 else 2
    self.guard_say = False
  # end def init

  def update(self, game_info, history, request, breakdown):
    super().update(game_info, history, request, breakdown)
    if request == 'DAILY_INITIALIZE':
      for i in range(history.shape[0]):
        if history['type'][i] == 'guard':
          self.reported = False
          self.ability_result = history['text'][i]
          print("ab: " + self.ability_result)
      if self.ability_result != '':
        self.talkQueue.push(Node(100, self.ability_result))
        self.comingout = True
    poss, wolfs, scores= breakdown.getTop()
    wolfs = sorted([x for x in wolfs if x not in self.deadlist], key=lambda x: scores[int(x), 1])
    human = [x for x in range(1,16) if x not in wolfs and x not in self.deadlist]
    human.sort(key = lambda x: scores[int(x), 0])
    self.tar = wolfs[-1]
    self.hold = wolfs[0]
    self.guardtar = human[-1]
    if game_info['day'] != 0:
      if scores[wolfs[-1], 1] > 1.15 and not self.voted and self.skcnt < 2:
        self.talkQueue.push(Node(10 * scores[wolfs[-1], 1] ,cb.vote(self.tar)))    
        self.voted = True
      if self.comingout and not self.guard_say and self.skcnt < 2:
        self.talkQueue.push(Node(10 * scores[human[-1], 0] ,cb.guard(self.guardtar)))
        self.guard_say = True
#    else: 
#      for i in range(history.shape[0]):
#        if history['type']
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
    
  def guard(self):
    return self.guardtar
  # end def guard  
#end def Bodyguard