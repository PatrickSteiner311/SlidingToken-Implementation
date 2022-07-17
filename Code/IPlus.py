# -*- coding: utf-8 -*-
"""
Created on Tue May 24 00:59:24 2022

@author: Patrick Steiner
"""
import SlidingToken
import ComponentPrepping

#Here are all the necessary methods to calculate I+

# Input: Vertices v, edges E, lower index li, upper index ui, size of the unlocked independent set
# Output: Independent set J
def Build_J(Vertices, Edges, LowerIndex, UpperIndex, ISLength, I):
    
    J = []
    BL = []
    cc = ComponentPrepping.Find_Connected_Components(Vertices, Edges)
    li = int(LowerIndex)
    ui = int(UpperIndex)
    J.append(UpperIndex)
    
    #identify which tokens belong to which connected components(should make this a method, used 3 times)
    CDict = {}
    CCount = 0
    for c in cc:
        CDict[CCount] = c
        CCount += 1
    ICount = []
    for count in range(len(CDict)):
        ICount.append(0)
    IDict = {}
    for i in I:
        for c in cc:
            cVal = list(CDict.keys())[list(CDict.values()).index(c)]
            if i in c:
                ICount[cVal] += 1
                IDict[cVal] = ICount[cVal]   
                
    #initialize J in token dict
    for c in cc:
        if J[0] in c:
            cVal = list(CDict.keys())[list(CDict.values()).index(c)]
            if not ICount[cVal] == 0:
                ICount[cVal] -= 1
                IDict[cVal] = ICount[cVal]    
            else:
                return []
            
    #make int list of str Vertices, reverse order for easier handling
    intList = []
    for v in Vertices:
        intList.append(int(v))
    for i in sorted(intList, reverse=True):
        if not i < li and not i > ui:
            BL.append(i)   
            
    #creating J. Only tokens that are not neighbours and can be placed in a connected component are allowed to be added to J
    for v in BL:
        if len(J) == ISLength:
            return J
        for c in cc:
            cVal2 = list(CDict.keys())[list(CDict.values()).index(c)]
            if str(v) in c and not ICount[cVal2] == 0:
                if not any(str(item) in SlidingToken.Vertex_Neighbours(Edges, str(v)) for item in J):
                    ICount[cVal2] -= 1
                    J.append(str(v))

                IDict[cVal2] = ICount[cVal2]
    if not len(J) == ISLength:
        return []
    return J


# Input: Independent set I', vertices and edges of G'
# Output: Dynamic programming table T
def Build_T(I, Vertices, Edges):
    T = {}
    T[0] = I
    for i in Vertices:
        T[i] = Build_J(Vertices, Edges, 0, i, len(I), I)
    return T


# Input: graph G' including edges, table of IS T, min value of N minN, number of independent sets k
# Output: Dynamic programming table W
def Build_W(Vertices, Edges, T, MinN, n, k):

    # preparing W
    W = []
    maxValDict = list(T)[k-1]
    for w in range(int(n)+1):
        W.append([])
        for v in range(int(maxValDict)+1):
            W[w].append([])

    # Filling W
    for i in range(int(MinN), int(n)+1):
        for j in T:

            GJ = SlidingToken.Build_GJ(Vertices, Edges, j, i)
            if not j == 0:
                if str(i) in T[j]:
                    W[i][int(j)] = T[j]
    
                elif SlidingToken.Rigid_GJ( ComponentPrepping.Update_G(Edges, GJ), T[j], int(j)+1, n) == []:
                    T2 = [item for item in SlidingToken.Apply_Limitations(
                        T[j], int(j)+1, n) if item in GJ]
                    T2 = T2 + [str(i)]
                    T3 = SlidingToken.Apply_Limitations(T[j], 0, k)
                    
                    T4 = T3 + T2 
                    # This deletes duplicates form the list. these lists are supposed to be sets
                    T4 = list(dict.fromkeys(T4))
                    W[i][int(j)] = T4
                else:
                    W[i][int(j)] = ["invalid"]
    return W

#Input: minimun range minN, maximum range n, dynamic tables T and W, graph edges G, maximum upper limit k
#Output: the evaluation of dynamic talbe W
def Eval_W(MinN, n, T, W, Edges, k):
    WImax = {}
    for i in range(int(MinN), int(n)+1):
        WIBuffer = []
        for j in range(int(list(T)[k-1])+1):
            #somewhere here was a mix up considering i and j counters
            # it works when they switch places.
            if 0 <= j and j < i:
                if SlidingToken.Check_IS(Edges, W[i][j]) and not W[i][j] == ["invalid"]:
                    #print("w", W[i][j])
                    AppW = SlidingToken.Apply_Limitations(W[i][j], 0, i)
                    WIBuffer.append(AppW)
        if not len(WIBuffer) == 0:
            WImax[i] = max(WIBuffer, key=len)
    return WImax


# Input: Independent Set I', graph G', (edges of G')
# Output: Independent Set I'+.
def Find_IJPlus(I, Vertices, Edges):
    T = Build_T(I, Vertices, Edges)
    MinN = Vertices[0]
    n = Vertices[-1]
    k = len(T)
    # building W
    W = Build_W(Vertices, Edges, T, MinN, n, k)

    W2 = Eval_W(MinN, n, T, W, Edges, k)

    IJPlus = []
    for i in W2.keys():
        if int(i) > 0:
            Ti = SlidingToken.Apply_Limitations(W2[i], 0, i)
            
            if len(IJPlus) == 0:
                IJPlus.append(Ti)
            if len(Ti) > len(IJPlus[0]):
                IJPlus = [Ti]
            elif len(Ti) == len(IJPlus[0]):
                IJPlus.append(Ti)
    finalList = [int(i) for i in IJPlus[0]]
    while not len(finalList) == len(I):
        if len(finalList) > 1:
            finalList.remove(max(finalList))
        else:
            return [str(i) for i in finalList]     
    finalList = [str(i) for i in finalList]        
    return finalList