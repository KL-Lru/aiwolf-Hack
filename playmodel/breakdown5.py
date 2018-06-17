#!/usr/bin/env python
import numpy as np
import pandas as pd

class Breakdown(object):
  def __init__(self):
    self.p2n = 6
    self.p3n = 5
    self.score_l = np.ones((6,4))
    self.param_3 = np.zeros((6, 6, self.p3n))
    self.param_2 = np.zeros((6, self.p2n))
    self.mat = np.zeros((60, 6), dtype = 'float32')
    idx = 0
    for wolf in range(1, 6):
      for seer in range(1, 6):
        for poss in range(1, 6):
          if poss == wolf or \
             seer == wolf or \
             seer == poss:
            continue
          self.mat[idx, poss] = 1
          self.mat[idx, wolf] = 2
          self.mat[idx, seer] = 3
          self.mat[idx, 0] = 1 # score
          idx += 1
    # print("breakdown: " + str(idx))
    
  def updateDeterministic(self, idx, role):
    rm = []
    for l in range(self.mat.shape[0]):
      if self.mat[l, idx] != role:
        rm.append(l)
    self.mat = np.delete(self.mat, rm, 0)
    # print("remains " + str(self.mat.shape[0]))

  def updateAttacked(self, idx):
    rm = []
    for l in range(self.mat.shape[0]):
      if self.mat[l, idx] == 2:
        rm.append(l)
    self.mat = np.delete(self.mat, rm, 0)
    # print("remains " + str(self.mat.shape[0])) 
    # for i in np.where(self.mat[:,idx] == 2)[0]:
    #   self.mat[i, 0] = 0      
    # print("remains " + str(len(np.where(self.mat[:,0] != 0)[0])))

  def updateExecuted(self, idx):
    self.param_2[idx, 0] = 1

  def updateCo(self, idx, role):
    if role == "SEER":
      self.param_2[idx, 1] = 1
    elif role == "POSSESSED":
      self.param_2[idx, 4] = 1    
    elif role == "WEREWOLF":
      self.param_2[idx, 5] = 1    

  def updateVote(self, src, dst):
    self.param_3[src, dst, 0] += 1
    self.score_l[dst, 0] *= 0.95
    self.score_l[dst, 1] *= 1.0
    self.score_l[dst, 2] *= 1.05
    self.score_l[dst, 3] *= 0.95
    # nonzero = np.where(self.mat[:,0] != 0)[0]
    # dstwolf = np.where(self.mat[:,dst] == 2)[0]
    # for i in [x for x in nonzero if x in dstwolf]:
    #   self.mat[i,0] *= 1.05

  def updateDivined(self, src, dst, species):
    if species == "HUMAN":
      self.param_3[src, dst, 1] += 1
      self.score_l[dst, 0] *= 1.1
      self.score_l[dst, 1] *= 1.1
      self.score_l[dst, 2] *= 0.9
      self.score_l[dst, 3] *= 0.95

    elif species == "WEREWOLF":
      self.param_3[src, dst, 2] += 1
      self.score_l[dst, 0] *= 0.9
      self.score_l[dst, 1] *= 0.9
      self.score_l[dst, 2] *= 1.1
      self.score_l[dst, 3] *= 0.95

  def update(self):
    for l in range(self.mat.shape[0]):
      # for prm in range(self.p3n):
      # 集約
      # core_3[int(self.mat[l, i]),int(self.mat[l, j]), prm] += self.param_3[i, j, prm]
      score = 0 
      for i in range(1,6):
        score += self.score_l[i, int(self.mat[l, i])]
      self.mat[l, 0] = score

  def printTop(self):
    mx = self.mat[:,0].max()  
    l = np.where(self.mat[:,0] == mx)[0]
    if len(l) <= 5:
      for i in l:
        print(self.mat[i])
    else:
      print("Top "+ str(len(l)))

  def getTop(self):
    if self.mat.shape[0] != 0:    
      mx = self.mat[:,0].max()
      l = np.where(self.mat[:,0] == mx)[0]
      wolfs = np.where(self.mat[l[0],1:] == 2)[0] + 1
      poss = np.where(self.mat[l[0],1:] == 1)[0] + 1
      seer = np.where(self.mat[l[0],1:] == 3)[0] + 1
      # print([poss, wolfs, seer])
      return [poss, wolfs, seer, self.score_l]
    return [[0],[0],[0],[0]]

  def compress(self):
    # print(self.mat.shape)
    # print("compressing...")
    rm = []
    for l in range(self.mat.shape[0]):
      core_2 = np.zeros((4,self.p2n))
      for i in range(1, 6):
        for prm in range(self.p2n):
          # 集約
          core_2[int(self.mat[l, i]), prm] += self.param_2[i, prm]
      # ありえん奴除く(人狼すでに死亡)
      if core_2[2, 0] >= 1 or \
         core_2[0, 1] >= 2 or \
         core_2[0, 2] >= 2:
        rm.append(l)
        continue
    self.mat = np.delete(self.mat, rm, 0)
    print(self.mat.shape)


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
  i : 1 : Possessed
  i : 2 : Wolf
  i : 3 : Seer

  core_3 i, j, k
  k : param_3
  i,j : 0 : Human
  i,j : 1 : Possessed
  i,j : 2 : Wolf
  i,j : 3 : Seer
  """
  """
  def norm(self):
    mx = self.mat[:,0].max()/10
    for i in np.where(self.mat[:,0] != 0)[0]:
      self.mat[i,0] /= mx
    
  def updateScore(self, wolf, poss):
    for i in np.where(self.mat[:,0] != 0)[0]:
      score = 0
      for j in range(1,15):
        score += (poss[j] if self.mat[i,j]==1 else wolf[j]/2) * self.mat[i,j]
      self.mat[i, 0] *= score/4
  """