# -*- coding: utf-8 -*-
"""
Created on Tue May 24 00:49:35 2022

@author: Patrick Steiner
"""
import SlidingToken
import SwitchSides

#Here are all the necessary methods to check if a graph is a bipartite permutation graph

# Input: Graph Edges
# Output: True if G is bipartite permutation graph, else False.
# We check first for bipartite, because our check for permutation requires the bipartite sets.
def Check_BPG(Edges):
    BGCheck, A, B = Check_Bipartite(Edges)
    if not BGCheck:
        return False
    print("G is Bipartite.")
    print("Set A:", A)
    print("Set B:", B)
    if not Check_Permutation(Edges, A, B):
        return False
    return True


# Input: Graph Edges.
# Output: True if G is Bipartite Graph, else false.
def Check_Bipartite(Edges):
    A = []
    B = []
    EdgeList = SlidingToken.Get_Edges(Edges)
    for e in EdgeList:
        if e[0] in A and e[1] in B or e[1] in A and e[0] in B:
            continue
        elif not e[0] in A and not e[0] in B and not e[1] in A and not e[1] in B:
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
        else:
            print("Graph is not Bipartite!")
            return False, A, B
    return True, A, B


#Input: graph Edges, vertex, blocklist BList
#Output: list of blocks which contain at least one vertex in N(v)
def Adjacent_Blocks(Edges, vertex, BList):
    aBlocks = []
    for bl in BList:
        if type(bl) == type(1):
            bl = [bl]
        if any(item in bl for item in[int(i) for i in SlidingToken.Vertex_Neighbours(Edges, vertex)[1:]]):
            aBlocks.append(bl)
    return aBlocks


#Input: Graph Edges, vertex, set A, blocklist BL
#Output: list of blocks containting at least one vertex from N(v) and one from S-(N(v))
def Mix_Blocks(Edges, vertex, A, BList):
    mBlocks = []
    vN = [int(i) for i in SlidingToken.Vertex_Neighbours(Edges, vertex)[1:]]
    aNew = [item for item in[int(i) for i in A] if item not in vN]
    for bl in BList:
        if type(bl) == type(1):
            bl = [bl]
        if any(item in bl for item in vN) and any(item in bl for item in aNew):
            mBlocks.append(bl)
    return mBlocks


#Input: list mixBlocks, neighbours of b nb, Block list BList, new Block BNew, boolean if BNew was placed at the right end of the list.
#Output: Block List BList with proper placement of C (between BNew and the mixBlock element)
def place_C(MixBlocks, BNeighbours, BList, front):
    if len(MixBlocks) > 0:
        for mb in MixBlocks:
            C = [item for item in mb if item not in BNeighbours]
            if type(C) == type(1):
                C = [C]
            for i in range(len(BList)):
                if BList[i] == mb:
                    if front:
                        BList = BList[:i+1] + [C] + BList[i+1:]
                    else:
                        BList = BList[:i] + [C] + BList[i:]
    return BList


# Input: Graph Edges, bipartite sets A, B
# Output: True if G is Permutation Graph, else false
def Check_Permutation(Edges, A, B):
    #step 1: find element in B with minimal Neighbours.
    minBuffer = (len(SlidingToken.Vertex_Neighbours(Edges, B[0])[1:]),B[0])
    BList = []
    #we need to make a list of old and new vertices.
    newList = []
    for length in range (len(A)+len(B)+1):
        newList.append(True)
        
    for b in B:
        #due to the nature of the algorith, we need to remove the initial vertex as well, only leaving the
        #neighbours of b that are in bipartite set A, update these values in the newList
        if len(SlidingToken.Vertex_Neighbours(Edges, b)[1:]) < minBuffer[0]:
            minBuffer = (len(SlidingToken.Vertex_Neighbours(Edges, b)[1:]),b)

    BList.append([int(i) for i in SlidingToken.Vertex_Neighbours(Edges, minBuffer[1])[1:]])
    for n in BList[0]:
        newList[int(n)] = False

    for b in B:
        nB = [int(i) for i in SlidingToken.Vertex_Neighbours(Edges, b)[1:]]
        if any(newList[int(i)] for i in nB):
            BNew = SwitchSides.List_Intersection([j for j, x in enumerate(newList) if x], nB) 
            adjBlocks = Adjacent_Blocks(Edges, b, BList)
            mixBlocks = Mix_Blocks(Edges, b, A, BList)
            if not all(item in [j for j, x in enumerate(newList) if not x] for item in nB):
                if len(BList) == 1:
                    BList.append(BNew)
                    BList = place_C(mixBlocks, nB, BList, True)
                elif not BList[0] in adjBlocks or BList[0] in mixBlocks and BList[-1] in adjBlocks:
                    BList.append(BNew)
                    BList = place_C(mixBlocks, nB, BList, True)
                else:
                    BList = BNew + BList
                    BList = place_C(mixBlocks, nB, BList, False)
                for bnew in BNew:
                    newList[bnew] = False
            else:
                if len(BList) == 1:
                    #choice here arbitrary
                    BList.append(BNew)
                else:
                    #here forced to the right of BList
                    BList.append(BNew)
        #all vertices in nb are old        
        else:
            adjBlocks = Adjacent_Blocks(Edges, b, BList)
            mixBlocks = Mix_Blocks(Edges, b, A, BList)
            #the vertices appear in a single block (easier to check than if they appear in two different blocks in BList, meaning we switched succession up compared to paper)
            for bl in BList:
                if type(bl) == type(1):
                    bl = [bl]
                if all(item in nB for item in bl):
                    if all(item in bl for item in nB):
                        break
                    C = [item for item in nB if item not in nB]
                    if BList.index(bl) == len(BList)-1:
                        BList.append(C)
                    elif BList.index(bl) == 0:
                        BList = [C] + BList
                    else:
                        print("Graph is not permutation Graph!")
                        return False
                else:   
                    for mb in mixBlocks:
                        if not adjBlocks.index(mb) == 0 or adjBlocks.index(mb) == len(adjBlocks):
                            break
                        C = [item for item in mb if item not in nB]
                        mbIndex = BList.index(mb)
                        if BList[mbIndex+1] in adjBlocks:
                            BList = BList[:mbIndex+1] + [C] + BList[mbIndex+1:]
                        elif mbIndex > 1 and BList[mbIndex-1] in adjBlocks:
                            BList = BList[:mbIndex] + [C] + BList[mbIndex:]
    print("Graph is permutation Graph.")    
    return True