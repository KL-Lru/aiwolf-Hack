#!/usr/bin/env python
import numpy as np
import pandas as pd
import csv 
from random import random

class Breakdown(object):
  def __init__(self):
    self.p2n = 6
    # self.p3n = 5
    self.score_l = np.ones((16,2))
    # self.param_3 = np.zeros((16, 16, self.p3n))
    self.param_2 = np.zeros((16, self.p2n))
    self.mat_wolf = np.zeros((455, 16), dtype = 'float32') # wolf or not wolf
    self.fdata = [[0.95, 1.05], [1.1, 0.9], [0.9, 1.1], [1.05, 0.95], [0.95, 1.05], [1.1, 0.9], [1.01, 0.99], [0.99, 1.01]]
    # self.fdata = [[round(0.5+random(),2), round(0.5+random(),2)], [round(0.5+random(),2), round(0.5+random(),2)], [round(0.5+random(),2), round(0.5+random(),2)], [round(0.5+random(),2), round(0.5+random(),2)], [round(0.5+random(),2),round(0.5+random(),2)], [round(0.5+random(),2), round(0.5+random(),2)], [round(0.5+random(),2), round(0.5+random(),2)], [round(0.5+random(),2), round(0.5+random(),2)]]
    self.first = True
    idx = 0
    for wolf1 in range(1, 16 - 2):
      for wolf2 in range(wolf1 + 1, 16 - 1):
        for wolf3 in range(wolf2 + 1, 16):
          self.mat_wolf[idx, [wolf1, wolf2, wolf3]] = 1
          self.mat_wolf[idx, 0] = 1 # score
          idx += 1
    # print("breakdown: " + str(idx))
    
  def updateDeterministic(self, idx, role):
    rm = []
    for l in range(self.mat_wolf.shape[0]):
      if self.mat_wolf[l, idx] != role:
        rm.append(l)
    self.mat_wolf = np.delete(self.mat_wolf, rm, 0)
    print("remains " + str(self.mat_wolf.shape[0]))

  def updateAttacked(self, idx):
    rm = []
    for l in range(self.mat_wolf.shape[0]):
      if self.mat_wolf[l, idx] == 1:
        rm.append(l)
    self.mat_wolf = np.delete(self.mat_wolf, rm, 0)
    print("remains " + str(self.mat_wolf.shape[0])) 
    # for i in np.where(self.mat_wolf[:,idx] == 2)[0]:
    #   self.mat_wolf[i, 0] = 0      
    # print("remains " + str(len(np.where(self.mat_wolf[:,0] != 0)[0])))

  def updateExecuted(self, idx):
    self.param_2[idx, 0] = 1

  def updateCo(self, idx, role):
    if role == "SEER":
      self.param_2[idx, 1] = 1
    elif role == "MEDIUM":
      self.param_2[idx, 2] = 1
    elif role == "BODYGUARD":
      self.param_2[idx, 3] = 1    
    elif role == "POSSESSED":
      self.param_2[idx, 4] = 1    
    elif role == "WEREWOLF":
      self.param_2[idx, 5] = 1    

  def updateVote(self, src, dst):
    # self.param_3[src, dst, 0] += 1
    self.score_l[dst, 0] *= self.fdata[0][0]
    self.score_l[dst, 1] *= self.fdata[0][1]
    # nonzero = np.where(self.mat_wolf[:,0] != 0)[0]
    # dstwolf = np.where(self.mat_wolf[:,dst] == 2)[0]
    # for i in [x for x in nonzero if x in dstwolf]:
    #   self.mat_wolf[i,0] *= 1.05

  def updateDivined(self, src, dst, species):
    if species == "HUMAN":
      # self.param_3[src, dst, 1] += 1
      self.score_l[dst, 0] *= self.fdata[1][0]
      self.score_l[dst, 1] *= self.fdata[1][1]

    elif species == "WEREWOLF":
      # self.param_3[src, dst, 2] += 1
      self.score_l[dst, 0] *= self.fdata[2][0]
      self.score_l[dst, 1] *= self.fdata[2][1]

  def updateIdentified(self, src, dst, species):
    if species == "HUMAN":
      # self.param_3[src, dst, 3] += 1
      self.score_l[dst, 0] *= self.fdata[3][0]
      self.score_l[dst, 1] *= self.fdata[3][1]
    elif species == "WEREWOLF":
      # self.param_3[src, dst, 4] += 1
      self.score_l[dst, 0] *= self.fdata[4][0]
      self.score_l[dst, 1] *= self.fdata[4][1]

  def updateGuarded(self, src, dst):
      self.score_l[dst, 0] *= self.fdata[5][0]
      self.score_l[dst, 1] *= self.fdata[5][1]

  def updateEstimate(self, src, dst, role):
    if role in ["HUMAN", "SEER", "MEDIUM", "VILLAGER", "POSSESSED"]:
      self.score_l[dst, 0] *= self.fdata[6][0]
      self.score_l[dst, 1] *= self.fdata[6][1]
    else:
      self.score_l[dst, 0] *= self.fdata[7][0]
      self.score_l[dst, 1] *= self.fdata[7][1]
      
  def printTop(self):
    mx = self.mat_wolf[:,0].max()  
    l = np.where(self.mat_wolf[:,0] == mx)[0]
    if len(l) <= 5:
      for i in l:
        print(self.mat_wolf[i])
    else:
      print("Top "+ str(len(l)))

  def getTop(self):
    if self.mat_wolf.shape[0] != 0:
      mx = self.mat_wolf[:,0].max()
      l = np.where(self.mat_wolf[:,0] == mx)[0]
      wolfs = np.where(self.mat_wolf[l[0],1:] == 1)[0] + 1
      poss = [1] # np.where(self.mat_wolf[l[0],1:] == 1)[0] + 1
      # print([poss, wolfs])
      return [poss, wolfs, self.score_l]
    return [[0],[0],[0]]

  def compress(self):
    # print(self.mat_wolf.shape)
    # print("compressing...")
    rm = []
    for l in range(self.mat_wolf.shape[0]):
      core_2 = np.zeros((2,self.p2n))
      for i in range(1, 16):
        for prm in range(self.p2n):
          # 集約
          core_2[int(self.mat_wolf[l, i]), prm] += self.param_2[i, prm]
      # ありえん奴除く(人狼すでに3人死亡)
      if core_2[1, 0] >= 3 or \
         core_2[0, 1] >= 3 or \
         core_2[0, 2] >= 3 or \
         core_2[0, 3] >= 3:
        rm.append(l)
        continue
    self.mat_wolf = np.delete(self.mat_wolf, rm, 0)
    # print(self.mat_wolf.shape)

  def update(self):
    for l in range(0,self.mat_wolf.shape[0]):
      # for prm in range(self.p3n):
      # 集約
      # core_3[int(self.mat_wolf[l, i]),int(self.mat_wolf[l, j]), prm] += self.param_3[i, j, prm]
      score = 0 
      for i in range(1,16):
        score += self.score_l[i, int(self.mat_wolf[l, i])]
      self.mat_wolf[l, 0] = score

  def writelog(self, role):
    f = csv.writer(open("./data/"+role+".log","a+"),lineterminator='\n')
    if self.first:
      f.writerow([y for x in self.fdata for y in x])
    self.first = False
    poss, wolfs, scores = self.getTop()
    if poss[0] != 0:
      f.writerow(wolfs)
  
  """
  param_3
  [i, j, 0] : エージェント i が j に投票
  [i, j, 1] : エージェント i が j を占って人間と宣言
  [i, j, 2] : エージェント i が j を占って人狼と宣言
  [i, j, 3] : エージェント i が j の霊能結果が人間と宣言
  [i, j, 4] : エージェント i が j の霊能結果が人狼と宣言

  param_2
  [i, 0] : エージェント i が処刑された
  [i, 1] : エージェント i が占いCOした
  [i, 2] : エージェント i が霊能COした
  [i, 3] : エージェント i が騎士COした
  [i, 4] : エージェント i が狂人COした
  [i, 5] : エージェント i が人狼COした
  """
  """
  core_2 i, j
  j : param_2
  i : 0 : Human
  i : 1 : Wolf

  core_3 i, j, k
  k : param_3
  i,j : 0 : Human
  i,j : 1 : Possessed
  i,j : 2 : Wolf
  """
  """
  def norm(self):
    mx = self.mat_wolf[:,0].max()/10
    for i in np.where(self.mat_wolf[:,0] != 0)[0]:
      self.mat_wolf[i,0] /= mx
    
  def updateScore(self, wolf, poss):
    for i in np.where(self.mat_wolf[:,0] != 0)[0]:
      score = 0
      for j in range(1,15):
        score += (poss[j] if self.mat_wolf[i,j]==1 else wolf[j]/2) * self.mat_wolf[i,j]
      self.mat_wolf[i, 0] *= score/4
  """