#!/usr/bin/env python
from playmodel.role.villager15  import Villager
from playmodel.role.seer15      import Seer
from playmodel.role.werewolf15  import Werewolf
from playmodel.role.possessed15 import Possessed
from playmodel.role.medium15    import Medium
from playmodel.role.bodyguard15 import Bodyguard
from playmodel.breakdown15 import Breakdown

# 作ったけどいらないクラスである説(Roleクラスを後で統合すると思う)

class prot15(object):
  def __init__(self):
    print('')
  #end def init

  def initialize(self, game_info, game_setting):
    self.role = game_info['myRole']
    self.idx = game_info['agentIdx']
    self.breakdown = Breakdown()
    # print(game_info)
    # print(type(self.idx))
    if self.role == 'VILLAGER':
      self.rolemodel = Villager(game_info, game_setting)
      self.breakdown.updateDeterministic(self.idx, 0)
    if self.role == 'SEER':
      self.rolemodel = Seer(game_info, game_setting)
      self.breakdown.updateDeterministic(self.idx, 0)
    if self.role == 'MEDIUM':
      self.rolemodel = Medium(game_info, game_setting)      
      self.breakdown.updateDeterministic(self.idx, 0)
    if self.role == 'BODYGUARD':
      self.rolemodel = Bodyguard(game_info, game_setting)
      self.breakdown.updateDeterministic(self.idx, 0)
    if self.role == 'WEREWOLF':
      self.rolemodel = Werewolf(game_info, game_setting)
      self.breakdown.updateDeterministic(self.idx, 2)
      for i in game_info['roleMap']:
        self.breakdown.updateDeterministic(int(i), 2)      
    if self.role == 'POSSESSED':
      self.rolemodel = Possessed(game_info, game_setting)
      self.breakdown.updateDeterministic(self.idx, 1)
  #end def initialize

  def update(self, game_info, history, request):
    print(history)
    self.rolemodel.update(game_info, history, request, self.breakdown)
  #end def update

  def dayStart(self):
    self.rolemodel.dayStart(self.breakdown)
  #end def dayStart

  def talk(self):
    return self.rolemodel.talk()
  # end def talk
  
  def whisper(self):
    return self.rolemodel.whisper()
  # end def whisper
      
  def vote(self):
    return self.rolemodel.vote()
  # end def vote
  
  def attack(self):
    return self.rolemodel.attack()
  # end def attack
  
  def divine(self):
    return self.rolemodel.divine()
  # end def divine
  
  def guard(self):
    return self.rolemodel.guard()
  # end def guard
  
  def finish(self):
    return self.rolemodel.finish()
  # end def finish

# end def prot15