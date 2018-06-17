
"""
villager.update()
for i in range(history.shape[0]):
if history.type[i] == "talk":
  text = history.text[i].split()
  if text[0] == "COMINGOUT":
    # Coming out時の処理
    idx = self.getAgentIdx(text[1])
    role = text[2]
    print("co  " + str(idx) + " " + text[2])
    if role == "SEER":
      self.wolfscore[idx] *= 1.02
      self.possscore[idx] *= 1.04
    elif role == "MEDIUM":
      self.wolfscore[idx] *= 1.04
      self.possscore[idx] *= 1.02
    elif role == "BODYGUARD":
      self.wolfscore[idx] *= 0.98
      self.possscore[idx] *= 0.97
    elif role == "WEREWOLF":
      self.wolfscore[idx] *= 1.06
      self.possscore[idx] *= 0.1
    elif role == "POSSESSED":
      self.wolfscore[idx] *= 0.98
      self.possscore[idx] *= 1.2
  elif text[0] == "DIVINED":
    # 占い結果の処理
    Idx = self.getAgentIdx(text[1])
    pracIdx = int(history.agent[i])
    species = text[2]
    print("div " + str(pracIdx) + " " + text[2] + " " + str(Idx))
    if species == "WEREWOLF":
      self.wolfscore[Idx] *= 1.1
      self.possscore[Idx] *= 0.9
    elif species == "HUMAN":
      self.wolfscore[Idx] *= 0.9
      self.possscore[Idx] *= 1.1
  elif text[0] == "_IDENTIFIED":
    # 霊能結果の処理
    Idx = self.getAgentIdx(text[1])
    pracIdx = int(history.agent[i])
    species = text[2]
    print("ide " + str(pracIdx) + " " + text[2] + " " + str(Idx))
    if species == "WEREWOLF":
      self.wolfscore[Idx] *= 1.1
      self.possscore[Idx] *= 0.9
    elif species == "HUMAN":
      self.wolfscore[Idx] *= 0.9
      self.possscore[Idx] *= 1.1
  elif text[0] == "ESTIMATE":
    # 推測時の処理
    Idx = self.getAgentIdx(text[1])
    pracIdx = int(history.agent[i])
    species = text[2]
    print("est " + str(pracIdx) + " " + text[2] + " " + str(Idx))
    if species == "WEREWOLF":
      self.wolfscore[Idx] *= 1.01
      self.possscore[Idx] *= 0.99
    elif species == "HUMAN":
      self.wolfscore[Idx] *= 0.99
      self.possscore[Idx] *= 1.01
  elif text[0] == "VOTE":
    # 投票宣言の処理
    Idx = self.getAgentIdx(text[1])
    pracIdx = int(history.agent[i])
    print("vot " + str(pracIdx) + " -> " + str(Idx))
  elif re.match("REQUEST",text[0]):
    # リクエストの処理
    print("request")

elif history.type[i]  == "vote":
  pracIdx = int(history.idx[i])
  idx = int(history.agent[i])
  print("agent " + str(pracIdx) + " voted agent " + str(idx))
  breakdown.updateVote(pracIdx, idx)

elif history.type[i]  == "execute":
  idx = int(history.agent[i])
  print("agent " + str(idx) + " executed")

elif history.type[i]  == "dead":
  idx = int(history.agent[i])
  print("agent " + str(idx) + " attacked")
  self.wolfscore[idx] = 0
  breakdown.updateAttacked(idx)

# elif history.type[i] == "finish":
#   print("end of game")
"""