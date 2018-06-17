#!/usr/bin/env python
import aiwolfpy.contentbuilder as cb
from playmodel.role.common5 import Common
from lib.talknode import Node

class Werewolf(Common):
  def __init__(self, game_info, game_setting):
    super().__init__(game_info, game_setting)
    self.comingout_role = ''
    self.reported = False
    self.ability_result = ''
  # end def init

  def update(self, game_info, history, request, breakdown):
    super().update(game_info,history, request, breakdown)
    if game_info['day'] != 2:
      if request == 'DAILY_INITIALIZE':
        self.reported = False
        self.ability_result = ''
      poss, wolf, seer, scores= breakdown.getTop()
      wolf = wolf[0]
      seer = seer[0]
      poss = poss[0]
      human = [x for x in range(1,6) if x != wolf]
      human.sort(key = lambda x: scores[int(x), 0])
      self.tar = human[-1]
      self.hold = human[0]
      if game_info['day'] != 0:
        if scores[human[0], 2] > 1.02 and not self.voted and self.skcnt < 2:
          self.talkQueue.push(Node(10 * scores[human[0], 2] ,cb.vote(self.hold)))
          self.voted = True
        if scores[human[1], 2] > 1.01 and not self.requested and self.skcnt < 2:
          self.talkQueue.push(Node(20 * scores[human[1], 2], cb.request(cb.request_div(human[1]))))
          self.requested = True
        if scores[human[0], 2] > 1.0 and not self.estimated and self.skcnt < 2:
          self.talkQueue.push(Node(30,cb.estimate(human[0], "WEREWOLF")))
          self.estimated = True
    else:
      for i in range(history.shape[0]):
        if history.type[i] == "talk":
          txt = history.text[i].split()
          if txt[0] == "COMINGOUT" and txt[2] == "POSSESSED":
            self.hold = self.getAgentIdx(txt[1])
            self.tar = self.getAgentIdx(txt[1])

  # end def update

  def dayStart(self):
    super().dayStart()
  #end def dayStart

  def talk(self):
    return super().talk()
  # end def talk
  
  def whisper(self):
    return cb.over()
  # end def whisper
       
  def vote(self):
    return self.hold
  # end def vote
  
  def attack(self):
    return self.tar
  # end def attack
#end def Werewolf