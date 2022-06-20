# -*- coding: utf-8 -*-
"""
Created on Tue May 24 00:52:50 2022

@author: Patrick Steiner
"""
# Here are all the necessary methods to prepare for the I+ algorithm.
import SlidingToken

# Input: Graph Edges, Neighbours of Rigid Tokens of Independent Set I under G.
# Output: G'. G' = G\N[R(G, I)]
def Form_GNew(Edges, NeighboursRigidI):
    # remove every element that G shares with NRI
    Vertices = SlidingToken.Get_Vertices(Edges)
    for n in NeighboursRigidI:
        Vertices.remove(n)
    return Vertices


# Input: Orignal graph G, component graph G'
# Output: Edges of graph G' (used for neighbours in I+)
def Update_G(Edges, NewVertices):
    GNE = []
    for edge in Edges:
        e = edge.split()
        if e[0] in NewVertices and e[1] in NewVertices:
            GNE.append(edge)
    return GNE


# Input: Independent set I, components Graph G'
# Output: I' = I cut with C
def Find_IJC(I, Vertices):
    # cut, only the elements that appear in both lists
    INew = []
    for i in I:
        if i in Vertices:
            INew.append(i)
    return INew


#input: temporary list, vertice vi, visited truth list, edges E
#output: recursively, connected components.
#this code bit has been taken from https://www.geeksforgeeks.org/connected-components-in-an-undirected-graph/ after disussing it and approval received from supervisor
def Depth_First_Search(temp, vertex, visited, E):
    visited[int(vertex)] = True
    v = str(vertex)
    temp.append(v)
    for n in SlidingToken.Vertex_Neighbours(E, v):
        if not n == v and visited[int(n)] == False:
            temp = Depth_First_Search(temp,n, visited, E) 
    return temp
    
    
#input: Edges E of graph G
#output: List of edges that are connected to eachother, i.e. connected components
def Find_Connected_Components(Vertices, Edges):
    #using dfs, Skeleton code from geeksforgeeks.org
    visited = []
    CC = []
    for i in range(int(Vertices[-1])+1):
        visited.append(False)
    for v in range(int(Vertices[-1])):
        if visited[v] == False and str(v) in Vertices:
            temp = []
            CC.append(Depth_First_Search(temp, v, visited, Edges))
    return CC


#Input: Vertices, Edges, independent sets I and J
#Output: Dictionaries containting tokens per connected component information.
def CC_Check(Vertices, Edges, I, J):
    cc = Find_Connected_Components(Vertices, Edges)
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
            if i in c:
                cVal = list(CDict.keys())[list(CDict.values()).index(c)]
                ICount[cVal] += 1
                IDict[cVal] = ICount[cVal]
    JCount = []
    for count in range(len(CDict)):
        JCount.append(0)
    JDict = {}
    for j in J:
        for c in cc:
            if j in c:
                cVal = list(CDict.keys())[list(CDict.values()).index(c)]
                JCount[cVal] += 1
                JDict[cVal] = JCount[cVal]
                
    print("I and J, tokens per component:", IDict, JDict)
    return IDict, JDict