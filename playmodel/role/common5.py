#!/usr/bin/env python
import aiwolfpy.contentbuilder as cb
import re
from lib.priority_queue import PriorityQueue
from lib.talknode import Node


class Common(object):
  def __init__(self, game_info, game_setting):
    self.game_info = game_info
    self.idx = game_info["agentIdx"]
    self.game_setting = game_setting
    self.voted = False
    self.requested = False
    self.estimated = False
    self.tar = 1 if self.idx != 1 else 2
    self.hold = 1 if self.idx != 1 else 2
    self.skcnt = 0
    self.talk_cnt = 0
    self.talkQueue = PriorityQueue()
    self.talkQueue.push(Node(0,cb.skip()))
    self.talkQueue.push(Node(0,cb.skip()))
    self.deadlist = []
  # end def init

  def getAgentIdx(self, text):
    return int(re.sub(".*\[([0-9]+)\].*","\\1",text))

  def update(self, game_info, history, request, breakdown):
    self.game_info = game_info
    print(request)
    if request == "DAILY_INITIALIZE":
      self.talkQueue.push(Node(0,cb.skip()))
      self.talkQueue.push(Node(0,cb.skip()))
      self.voted = False
      self.estimated = False
      self.requested = False
      self.talk_cnt = 0
      self.skcnt=0
      # print("reset flags")      
    for i in range(history.shape[0]):
      if history.type[i] == "talk":
        text = history.text[i].split()
        if text[0] == "COMINGOUT":
          # Coming out時の処理
          idx = self.getAgentIdx(text[1])
          role = text[2]
          breakdown.updateCo(idx, role)
          print("co " + str(idx) + " " + text[2])

        elif text[0] == "DIVINED":
          # 占い結果の処理
          src = int(history.agent[i])
          dst = self.getAgentIdx(text[1])
          species = text[2]
          breakdown.updateDivined(src, dst, species)
          print("divine " + str(src) + " " + text[2] + " " + str(dst))

        elif text[0] == "ESTIMATE":
          # 推測時の処理
          src = int(history.agent[i])
          dst = self.getAgentIdx(text[1])
          species = text[2]
          print("estimate " + str(src) + " " + text[2] + " " + str(dst))

        elif text[0] == "VOTE":
          # 投票宣言の処理
          src = int(history.agent[i])
          dst = self.getAgentIdx(text[1])
          print("vote " + str(src) + " -> " + str(dst))

        elif re.match("REQUEST",text[0]):
          # リクエストの処理
          print("request...")

      elif history.type[i]  == "vote":
        # 投票時の処理
        src = int(history.idx[i])
        dst = int(history.agent[i])
        print("agent " + str(src) + " voted agent " + str(dst))
        breakdown.updateVote(src, dst)

      elif history.type[i]  == "execute":
        # 処刑時の処理
        idx = int(history.agent[i])
        breakdown.updateExecuted(idx)
        print("agent " + str(idx) + " executed")
        self.deadlist.append(idx)

      elif history.type[i]  == "dead":
        # 人狼襲撃時の処理
        idx = int(history.agent[i])
        print("agent " + str(idx) + " attacked")
        self.deadlist.append(idx)
        breakdown.updateAttacked(idx)

    if request != "DAILY_INITIALIZE":
      breakdown.compress()
      breakdown.update()
  # end def update

  def dayStart(self):
    self.voted = False
    self.estimated = False
    self.requested = False
    self.talk_cnt = 0
    self.skcnt=0
    # print("reset flags")
  #end def dayStart

  def talk(self):
    if len(self.talkQueue) == 0:
      # print("queue is empty")
      self.skcnt+=1
      return cb.skip()
    txt = self.talkQueue.pop().text
    self.skcnt = 0
    print("txt: " + txt)
    return txt
  # end def talk
  
  def whisper(self):
    return cb.over()
  # end def whisper
      
  def vote(self):
    return self.tar
  # end def vote
  
  def attack(self):
    return self.idx
  # end def attack
  
  def divine(self):
    return self.idx
  # end def divine
  
  def guard(self):
    return self.idx
  # end def guard
  
  def finish(self):
    return None
  # end def finish
#end def Common