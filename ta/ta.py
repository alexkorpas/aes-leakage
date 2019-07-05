# manualTemplate.py
# A script to perform a template attack
# Will attack one subkey of AES-128

import numpy as np
from scipy.stats import multivariate_normal
import matplotlib.pyplot as plt
from helpers import *
from metrics import guessing_entropy


class TAAttacker:
    def __init__(self, numPOIs, pooled=False):
        # 0: Init convariance and mean matrices
        self.numPOIs = numPOIs
        self.POIspacing = 5
        self.POIs = [[] for _ in range(16)]
        self.meanMatrix = np.zeros((16, 9, self.numPOIs))
        self.covMatrix = np.zeros((16, 9, self.numPOIs, self.numPOIs))
        self.pooled = pooled
        self.bestguess = [0] * 16

    def find_traces_HW(self, bnum, traces, ptext, key):
        # 2: Find HW(sbox) to go with each input
        # Note - we're only working with the first byte here
        tempSbox = [sbox[ptext[i][bnum] ^ key[i][bnum]]
                    for i in range(len(ptext))]
        tempHW = [hw[s] for s in tempSbox]

        # 2.5: Sort traces by HW
        # Make 9 blank lists - one for each Hamming weight
        tempTracesHW = [[] for _ in range(9)]

        # Fill them up
        for i in range(len(ptext)):
            HW = tempHW[i]
            tempTracesHW[HW].append(traces[i])

        # Switch to numpy arrays
        tempTracesHW = [np.array(tempTracesHW[HW]) for HW in range(9)]
        return tempTracesHW

    def find_diffs(self, traces_HW, trace_size):
        # 3: Find averages
        tempMeans = np.zeros((9, trace_size))
        for i in range(9):
            tempMeans[i] = np.average(traces_HW[i], 0)

        # 4: Find sum of differences
        tempSumDiff = np.zeros(trace_size)
        for i in range(9):
            for j in range(i):
                tempSumDiff += np.abs(tempMeans[i] - tempMeans[j])

        return (tempMeans, tempSumDiff)

    def find_max_POIs(self, diffs, bnum):
        # 5: Find POIs
        for i in range(self.numPOIs):
            # Find the max
            nextPOI = diffs.argmax()
            self.POIs[bnum].append(nextPOI)

            # Make sure we don't pick a nearby value
            poiMin = max(0, nextPOI - self.POIspacing)
            poiMax = min(nextPOI + self.POIspacing, len(diffs))
            for j in range(poiMin, poiMax):
                diffs[j] = 0

    def fill_matrices(self, means, tempTracesHW, bnum):
        # 6: Fill up mean and covariance matrix for each HW
        for HW in range(9):
            for i in range(self.numPOIs):
                # Fill in mean
                self.meanMatrix[bnum, HW, i] = means[HW][self.POIs[bnum][i]]
                for j in range(self.numPOIs):
                    x = tempTracesHW[HW][:, self.POIs[bnum][i]]
                    y = tempTracesHW[HW][:, self.POIs[bnum][j]]
                    self.covMatrix[bnum, HW, i, j] = cov(x, y)

    def profile(self, traces, ptexts, keys):

        for bnum in range(16):
            tempTracesHW = self.find_traces_HW(bnum, traces, ptexts, keys)
            (tempMeans, tempSumDiff) = self.find_diffs(
                tempTracesHW, len(traces[0]))    
            self.find_max_POIs(tempSumDiff, bnum)
            self.fill_matrices(tempMeans, tempTracesHW, bnum)

    def get_multivariate_normal(self, bnum, HW):
        if self.pooled:
            return multivariate_normal(self.meanMatrix[bnum, HW],
                                       self.covMatrix[bnum].mean(axis=0))
        else:
            return multivariate_normal(self.meanMatrix[bnum, HW],
                                       self.covMatrix[bnum, HW])

    def attack(self, traces, ptexts):
        # 2: Attack
        # Running total of log P_k
        refs = [0] * 16
        for bnum in range(16):
            P_k = np.zeros(256)
            for j in range(len(traces)):
                # Grab key points and put them in a small matrix
                a = [traces[j][self.POIs[bnum][i]]
                     for i in range(len(self.POIs[bnum]))]

                # Test each key
                for k in range(256):
                    # Find HW coming out of sbox
                    HW = hw[sbox[ptexts[j][bnum] ^ k]]
                    # Find p_{k,j}
                    rv = self.get_multivariate_normal(bnum, HW)
                    p_kj = rv.pdf(a)

                    # Add it to running total
                    P_k[k] += np.log(p_kj)

            self.bestguess[bnum] = np.argmax(P_k)
            refs[bnum] = P_k.argsort()[::-1]

        return refs


if __name__ == "__main__":
    temp_size = 4000
    atk_size = 1000
    tempTraces = np.load('data/ta_traces.npy')[:temp_size]
    tempPText = np.load('data/ta_plaintexts.npy')[:temp_size]
    tempKey = np.load('data/ta_keylist.npy')[:temp_size]
    atkTraces = np.load('data/traces.npy')[:atk_size]
    atkPText = np.load('data/plain.npy')[:atk_size]
    atkKey = np.load('data/key.npy')[:atk_size]
    # Start calculating template

    ta = TAAttacker(5, pooled=False)
    ta.profile(tempTraces, tempPText, tempKey)

    # Template is ready!
    print(atkKey[0])
    refs = ta.attack(atkTraces, atkPText)
    ge = guessing_entropy(atkKey[0], refs)
    print(ta.bestguess)
    print(ge)
