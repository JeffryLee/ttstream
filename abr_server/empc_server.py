#!/usr/bin/env python

import base64
import urllib
import sys
import os
import json
import time


import numpy as np
import time
import itertools
from itertools import permutations


stime = time.time()
bufferstatus = [[2, 3], [0, 3], [0, 3], [0, 3], [0, 3]]

# 1000 kbps
throughput = 1000

bitrate = [170 * 5.4, 321 * 5.4, 487 * 5.4, 970 * 5.4, 1630 * 5.4]
bitraterewards = [1, 2, 3, 12, 15]

chunklength = 5.4
fcnt = [0]

bufferlist = []
playlist = []

prob = 1.0

for i in range(1, 4):
    pratioi = 3

    prob = prob / pratioi
    for j in range(1, min(3, 5-i) + 1):
        
        pratioj = min(3, 5-i)

        prob = prob / pratioj
        
        if 5-i-j == 0:
            playlist.append([i, j, 0, 0, 0, prob])

        
        
        for p in range(1, min(5-i-j, 3) + 1):
            pratiop = min(3, 5-i-j)

            prob = prob / pratiop

            if 5-i-j-p == 0:
                playlist.append([i, j, p, 0, 0, prob])
            
            for q in range(1, min(5-i-j-p, 3) + 1):
                pratioq = min(3, 5-i-j-p)

                prob = prob / pratioq

                if 5-i-j-p-q == 0:
                    playlist.append([i, j, p, q, 0, prob])

                for k in range(1, min(5-i-j-p-q, 3) + 1):
                    if 5-i-j-p-q-k == 0:
                        playlist.append([i, j, p, q, k, prob])
                prob = prob * pratioq

            prob = prob * pratiop

        prob = prob * pratioj
    prob = prob * pratioi

block2ProbMap = {}
for i in range(len(playlist)):
    for j in range(5):
        for k in range(playlist[i][j]):
            if (j,k) not in block2ProbMap.keys():
                block2ProbMap[(j, k)]  = playlist[i][-1]
            else:
                block2ProbMap[(j, k)]  += playlist[i][-1]


problist = []
for key in block2ProbMap.keys():
    if key != (0, 0) and key != (0, 1):
        problist.append(block2ProbMap[key])


problist = sorted(problist, reverse=True)

def computeRewardUpperbond_bitrate(combo):
    combo_sorted = sorted(combo, reverse=True)

    reward_est = block2ProbMap[(0, 0)] * bitraterewards[2] + block2ProbMap[(0, 1)] * bitraterewards[2]
    
    for i in range(len(problist)):
        if i < 5:
            reward_est += problist[i] * bitraterewards[combo_sorted[i]]
        
        else:
            reward_est += problist[i] * (bitraterewards[0] - 4 * bitrate[0] / throughput)
            
    return reward_est

def computeRewardUpperbond(bufferseqence):
    buffertableidx = [2, 0, 0, 0, 0]

    block2rewardMap = {}
    for key in block2ProbMap.keys():
        block2rewardMap[key] = -1

    block2rewardMap[(0, 0)] = bitraterewards[2]
    block2rewardMap[(0, 1)] = bitraterewards[2]
    
    trace = []


    for i in range(5):
        block2rewardMap[(bufferseqence[i], buffertableidx[bufferseqence[i]])] = 0

        trace.append((bufferseqence[i], buffertableidx[bufferseqence[i]]))
        buffertableidx[bufferseqence[i]] += 1

    reward_est = 0
    for key in block2ProbMap.keys():
        if block2rewardMap[key] == -1:
            cur_reward = bitraterewards[0] - 4 * bitrate[0] / throughput
            reward_est += cur_reward * block2ProbMap[key]
        else:
            reward_est += block2rewardMap[key] * block2ProbMap[key]
    
    return reward_est, trace
    

    
def computeReward(bufferseqence, bitratesequence):
    fcnt[0] += 1
    rewardlist = [0 for i in range(len(playlist))]

    buffertable = [[[-1, 0] for i in range(3)] for j in range(5)]

    buffertable[0][0] = [0, 2]
    buffertable[0][1] = [0, 2]

    buffertableidx = [2, 0, 0, 0, 0]
    
    timestamp = 0
    for i in range(5):
        timestamp += bitrate[bitratesequence[i]] / throughput

        buffertable[bufferseqence[i]][buffertableidx[bufferseqence[i]]] = [timestamp, bitratesequence[i]]


        buffertableidx[bufferseqence[i]] += 1
        
        
    for i in range(len(playlist)):
        playsequence = []

        timestamp = 0
        for j in range(5):
            for k in range(playlist[i][j]):
                playsequence.append([j, k, timestamp])
                
                timestamp += 5.4
        
        rebufferingpenalty = 0
        abrreward = 0
        
        has_penality = [0 for i in range(5)]
        for j in range(5):
            abrreward += bitraterewards[buffertable[playsequence[j][0]][playsequence[j][1]][1]]
            
            if buffertable[playsequence[j][0]][playsequence[j][1]][0] == -1:
                if has_penality[playsequence[j][0]] == 0:
                    rebufferingpenalty += bitrate[0] / throughput
                    has_penality[playsequence[j][0]] = 1
            
            else:
                if buffertable[playsequence[j][0]][playsequence[j][1]][0] > playsequence[j][2]:
                    rebufferingpenalty += min(bitrate[0] / throughput, buffertable[playsequence[j][0]][playsequence[j][1]][0] - playsequence[j][2])

        rewardlist[i] = abrreward - 4 * rebufferingpenalty


    sumx = 0
    for i in range(len(playlist)):
        sumx += rewardlist[i] * playlist[i][-1]
        
    return sumx
    



for i in range(2):
    for j in range(min(5-i, 3) + 1):
        if j == 0 and 5-i > 0 and bufferstatus[1][0] == 0:
            continue
        for p in range(min(5-i-j, 3) + 1):
            if p == 0 and 5-i-j > 0 and bufferstatus[2][0] == 0:
                continue


            for q in range(min(5-i-j-p, 3) + 1):

                if q==0 and 5-i-j-p > 0 and bufferstatus[3][0] == 0:
                    continue

                k = 5-i-j-p-q

                if k > 3:
                    continue

                bufferlist.append((i, j, p, q, k))

bufferstrategy = []

for i in range(len(bufferlist)):
    tmp = []
    smap = {}
    for j in range(5):
        
        for k in range(bufferlist[i][j]):
            tmp.append(j)

    perm = permutations(tmp)

    perm = list(perm)
    
    for item in perm:
        bi = 0
        flag = False
        retstring = ""
        for k in range(5):
            retstring += str(item[k])
            if item[k] > bi + 1:
                flag = True
                break
            else:
                bi = max(item[k], bi)
        
        if flag == False:
            smap[retstring] = 0
        
    
    for key in smap.keys():
        bufferstrategy.append(key)


maxreward = 0

CHUNK_COMBO_OPTIONS = []
for combo in itertools.product([0,1,2,3,4], repeat=5):
    # combo = [0, 3, 3, 3, 3]
    # combo = [3, 3, 3, 3, 0]
    reward_est = computeRewardUpperbond_bitrate(combo)
    
    if reward_est > maxreward:
        CHUNK_COMBO_OPTIONS.append([combo, reward_est])




CHUNK_COMBO_OPTIONS.sort(key=lambda x: x[1], reverse=True)
maxbs = [0, 0, 0, 0, 0]
maxcombo = [0, 0, 0, 0, 0]
for bs_item in bufferstrategy:
    
    # print(bs_item)
    
    bs_info = (int(bs_item[0]), int(bs_item[1]), int(bs_item[2]), int(bs_item[3]), int(bs_item[4]))

    # block2ProbMap[(j, k)]

    reward_est, trace = computeRewardUpperbond(bs_info)
    
    for full_combo_pair in CHUNK_COMBO_OPTIONS:
        
        if maxreward >= full_combo_pair[1]:
            break

        full_combo = full_combo_pair[0]
        
        reward_upperbond = reward_est

        for rui in range(5):
            if trace[rui] in block2ProbMap.keys():
                reward_upperbond += bitraterewards[full_combo[rui]] * block2ProbMap[trace[rui]]
    
        if maxreward >= reward_upperbond:
            continue
        
        thisreward = computeReward(bs_info, full_combo)
        
        if thisreward > maxreward:
            maxreward = thisreward
            maxbs = list(bs_info)
            maxcombo = list(full_combo)


print(maxreward)
print(maxbs)
print(maxcombo)

etime = time.time()

print(etime - stime)
kk = 1

print(fcnt)