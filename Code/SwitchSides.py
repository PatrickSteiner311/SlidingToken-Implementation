# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 18:46:43 2022

@author: Patrick Steiner
"""
import SlidingToken

#Important global tables
M = []
C = {}


#input: Two lists
#output: A list of the common items from the input lists.
def List_Intersection(List1,List2):
    List3 = [item for item in List1 if item in List2]
    return List3


#Input: Vertices V
#Output: Global Dictionary C initialized with empty lists as values
def Init_C(Vertices):
    for v in Vertices:
        C[v] = []
   
        
#Input: Bipartite graph G, split in parts A and B, initial independent set I0
#Output: Global variable M initialized.
def Init_M(Edges, A, B, I):
    global M
    for u in B:
        C[u] = List_Intersection(SlidingToken.Vertex_Neighbours(Edges, u), I[0])
        if len(C[u]) == 1:
            M = list(set(M) | set([u]))
  
    
#Input: Graph G, independent set I
#Output: Independent set I in same equivalence cass as input IS I
def Switch_Sides(Edges, I):
    global k
    global M
    k = 0
    while len(M) > 0:
        k += 1
        u = M.pop()#remove arbitrary element?
        v = C[u][0]
        C[u] = []
        Ik = I[0]
        #for some reason using append here copys the to be appended element into every list position
        # the same happened when using dictionaries. some pointer going haywire?
        Ik = Ik + [u]
        Ik.remove(v)
        I.append(Ik)
        for w in SlidingToken.Vertex_Neighbours(Edges, v):
            if v in C[w]:
                #ensuring that the remainder is at least an empty list, not none
                if len(C[w]) == 1:
                    C[w]==[]
                else: 
                    C[w].remove(v)
 
            if len(C[w])==1:
                #No append here either, need union.
                M = list(set(M) | set([w]))
    return I


#Input: Graph edges G, bipartite sets A,B, independent set I0
def SwitchSides(Edges, A, B, I):
    V = A+B
    V.sort()
    Init_C(V)
    Init_M(Edges, A, B, I)
    #print("Start switch sides.")
    ResultI = Switch_Sides(Edges, I)
    return ResultI