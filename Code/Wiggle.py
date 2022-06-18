# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 17:15:01 2022

@author: Patrick Steiner
"""
import SwitchSides
import SlidingToken
import sys

def Get_Bipartite_Sets(Edges):
    #could add check here to see if graph is bipartite, leaving it out since
    #in main script, it will be tested before arriving here. This was very complicated
    A = []
    B = []
    EdgeTuples = SlidingToken.Get_Edges(Edges)
    for e in EdgeTuples:
        if not e[0] in A and not e[0] in B and not e[1] in A and not e[1] in B:
            A.append(e[0])
            B.append(e[1])
        elif e[0] in A and not e[0] in B and not e[1] in A and not e[1] in B:
            B.append(e[1])
        elif not e[0] in A and e[0] in B and not e[1] in A and not e[1] in B:
            A.append(e[1])
        elif not e[0] in A and not e[0] in B and e[1] in A and not e[1] in B:
            B.append(e[0])
        elif not e[0] in A and not e[0] in B and not e[1] in A and e[1] in B:
            A.append(e[0])                             
    return A, B


#Input: BPG Graph AUB E, Independent set I0    
#output: possibly all independent sets possible on graph G starting from IS I0
def Wiggle(Edges ,A,B,I):
    l1 = SwitchSides.SwitchSides(Edges,A,B,I)
    l2 = SwitchSides.SwitchSides(Edges,B,A,I)
    resultList = l1 + l2
    return resultList


#Legacy code, used to test Wiggle.py and SwitchSides.py
def main():
    with open(sys.argv[1]) as gtxt:
        graph = gtxt.readlines()
    with open(sys.argv[2]) as itxt:
        independentSet = itxt.readlines()
    true, A, B = Get_Bipartite_Sets(graph)
    print(A)
    print(B)
    indSet = []
    #need to strip all
    for i in range(len(independentSet)):
        independentSet[i] = independentSet[i].strip()
    #independentSet[0] = independentSet[0].strip()
    indSet.append(independentSet)
    result = Wiggle(graph, A, B, indSet)
    print("The following independent sets were reached:")
    print(result)

if __name__ == "__main__":
    main()