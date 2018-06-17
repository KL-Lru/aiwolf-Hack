#!/usr/bin/env python
import aiwolfpy
import aiwolfpy.contentbuilder as cb

import playmodel as pm

myname = 'Lru'

class Agent(object):
  def __init__(self, agent_name):
    # myname
    self.myname = agent_name

    self.playmodelProt5 = pm.prot5()
    self.playmodelProt15 = pm.prot15()
  # end def init
      
  def getName(self):
    return self.myname
  # end def getName
  
  def initialize(self, base_info, diff_data, game_setting):
    # print(base_info)
    # print(diff_data)
    self.role = base_info['myRole']
    self.idx = base_info['agentIdx']
    self.playernum = game_setting['playerNum']

    # ゲームごとの初期化
    if self.playernum == 15 :
      self.playmodelProt15.initialize(base_info, game_setting)
    elif self.playernum == 5:
      self.playmodelProt5.initialize(base_info, game_setting)
  # end def initialize

  def update(self, base_info, diff_data, request):
    # print(base_info)
    # print(diff_data)
    # print(request)
    if self.playernum == 15 :
      self.playmodelProt15.update(base_info, diff_data, request)
    elif self.playernum == 5:
      self.playmodelProt5.update(base_info, diff_data, request)
  # end def update

  def dayStart(self):
    if self.playernum == 15 :
      self.playmodelProt15.dayStart()
    elif self.playernum == 5:
      self.playmodelProt5.dayStart()
    return None
  # end def dayStart

  def talk(self):
    if self.playernum == 15 :
      return self.playmodelProt15.talk()
    elif self.playernum == 5:
      return self.playmodelProt5.talk()
  
  def whisper(self):
    if self.playernum == 15 :
      return self.playmodelProt15.whisper()
    elif self.playernum == 5:
      return self.playmodelProt5.whisper()
      
  def vote(self):
    if self.playernum == 15 :
      return self.playmodelProt15.vote()
    elif self.playernum == 5:
      return self.playmodelProt5.vote()
  
  def attack(self):
    if self.playernum == 15 :
      return self.playmodelProt15.attack()
    elif self.playernum == 5:
      return self.playmodelProt5.attack()
  
  def divine(self):
    if self.playernum == 15 :
      return self.playmodelProt15.divine()
    elif self.playernum == 5:
      return self.playmodelProt5.divine()
  
  def guard(self):
    if self.playernum == 15 :
      return self.playmodelProt15.guard()
    elif self.playernum == 5:
      return self.playmodelProt5.guard()
  
  def finish(self):
    if self.playernum == 15 :
      return self.playmodelProt15.finish()
    elif self.playernum == 5:
      return self.playmodelProt5.finish()
    
agent = Agent(myname)
    
# run
if __name__ == '__main__':
  aiwolfpy.connect_parse(agent)
    