# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 11:01:01 2022

@author: Patrick Steiner
"""
import sys
import os
import time
import Wiggle
import SwitchSides
import GraphCheck
import ComponentPrepping
import IPlus
import Reconfiguration

#Main file. Containing instructions and helping functions needed across all other files

#Input: Graph Edges, vertex 
#Output: Neighbours of v including v.
def Vertex_Neighbours(Edges, vertex):
    NeighbourList = [vertex]
    EdgeTuples = Get_Edges(Edges)
    for edge in EdgeTuples:
       if vertex in edge:
           if vertex == edge[0]:
               NeighbourList.append(edge[1])
           else:
               NeighbourList.append(edge[0])         
    return NeighbourList


# Input: Graph Edges
# Output: List of vertices in G.
def Get_Vertices(Edges):
    Vertices = []
    for edge in Edges:
        e = edge.split()
        for vertex in e:
            if not vertex in Vertices:
                Vertices.append(vertex)
    return Vertices


# Input: Graph Edges
# Output: List of edges as tuples in G. Example: [<1,2>, <2,3>]
def Get_Edges(Edges):
    EdgeList = []
    for edge in Edges:
        vertex = edge.split()
        e = tuple((vertex[0], vertex[1]))
        EdgeList.append(e)
    return EdgeList


# Input: Graph Edges, Independent Set I
# Output: True, if I is independet Set for G, else False
def Check_IS(Edges, I):
    # check if the sets Tokens are all contained in G
    Vertices = Get_Vertices(Edges)
    if not all(item in Vertices for item in I):
        return False
    # second check: any element of I can not share an edge with another element of I
    for i in I:
        for j in I:
            if i+" " + j in Edges:
                return False
    return True


# Input: Graph G, independet set I
# Output: Rigid tokens for I under G
def Rigid_tokens(Edges, I):
    #A, B = Wiggle.Get_Bipartite_Sets(Edges)
    boolean, A, B = GraphCheck.Check_Bipartite(Edges)
    wiggleResult = Wiggle.Wiggle(Edges, A, B, I)
    # resulting lists intersections equal rigid tokens.
    l1 = []
    lBuffer = wiggleResult.pop()
    while not len(wiggleResult) == 0:
        l1 = wiggleResult.pop()
        lBuffer = SwitchSides.List_Intersection(lBuffer, l1)
    return lBuffer


# Input: Rigid tokens of independent sets I and J
# Output: True if rigid tokens of independent sets I and J the same, else False
def Check_Shared_Rigid(RigidTokensI, RigidTokensJ):
    # idea: just compare the lists
    RigidTokensI.sort()
    RigidTokensJ.sort()
    return RigidTokensI == RigidTokensJ


# Input: Independent set I, lower limit LL, upper limit UL
#Output: I^{LI,UI}
def Apply_Limitations(Input, LowerLimit, UpperLimit):
    I = Input.copy()
    for token in Input:
        if int(token) < LowerLimit:
            I.remove(token)
        elif int(token) > int(UpperLimit):
            I.remove(token)
    return I


# Input: Graph GJ (G without J or its neighbours), Independent set T[j], independent set index j, maximal vertex index n
# Output: rigid tokens under graph GJ, Independent set T[j]^{j+1,n}
def Rigid_GJ(EdgesGJ, T, ISIndexJ, MaxVertexIndexN):
    # remove vertices that break rules set by T[j]^{j+1,n}
    # does this fix hold every time?
    if T == [] or EdgesGJ == []:
        return []
    T = Apply_Limitations(T, int(ISIndexJ)+1, MaxVertexIndexN)
    # identify rigid tokens
    RT = Rigid_tokens(EdgesGJ, [T])
    return RT


#Input: Vertices of G, edges of G,

def Build_GJ(Vertices, Edges, j, i):
    GBuffer = [item for item in Vertices if item not in Vertex_Neighbours(
        Edges, str(j))]
    GBuffer = [item for item in GBuffer if not int(item) < int(j)]
    return GBuffer


# Function to compare I'+ with J'+. If they are equal, then we can say that there
# exists an Independent set reconfiguration sequence from I to J under G following the proof of Theorem 1.
# Input: Independent Sets I'+ and J'+
# Output: True if I'+ is identical to J'+, else False
def Compare_IJPlus(IP, JP):
    IP.sort()
    JP.sort()
    return IP == JP


#If no rigid tokens are part of the Independent sets, i.e. sets are already unlocked.
#skip to IPlus algorithm
#Input:independent sets I,J, graph G (vertices and edges)
#Output: result of IPlus algorithm.
def skip_to_IPlus(I, J, Vertices, Edges, start):
    print("Expand I' and J' to I'+ and J'+.")
    IP = IPlus.Find_IJPlus(I, Vertices, Edges)
    print("I'+:", IP)
    JP = IPlus.Find_IJPlus(J, Vertices, Edges)
    print("J'+:", JP)

    print("Compare I'+ with J'+.")
    if Compare_IJPlus(IP, JP):
        print("An independent set reconfiguration sequence exists between I and J under G!")
        ReconfigurationSequence = Reconfiguration.reconfiguration_Search(Edges, I, J, [], ComponentPrepping.Find_Connected_Components(Vertices, Edges))
        print("A possible reconfiguration sequence from I to J:")
        for item in ReconfigurationSequence:
            print(item)
        end = time.time()
        print("Runtime:", end -start)
    else:
        print("There can not be an independent set reconfiguration sequence between I and J under G!")
        end = time.time()
        print("Runtime:", end -start)
        return


def main():
    start = time.time()
    
    #First section: Validate input data.
    if not len(sys.argv) > 1:
        print("Not enough arguments, this code needs a graph G and two Independent sets I and J as text files to work.")
        end = time.time()
        print("Runtime:", end -start)
        return
    # get Graph G and independent sets I and J from specified folder
    folder = sys.argv[1]
    files = os.listdir(folder)
    with open(folder+ "/" + files[0]) as gtxt:
        Edges = gtxt.readlines()
    with open(folder +"/" + files[1]) as itxt:
        I = itxt.readlines()
    with open(folder +"/" + files[2]) as jtxt:
        J = jtxt.readlines()
    # striping "\n" from all the inputs
    for i in range(len(Edges)):
        Edges[i] = Edges[i].strip()
    for i in range(len(I)):
        I[i] = I[i].strip()
    for i in range(len(J)):
        J[i] = J[i].strip()
    CCVariant = False
    if len(sys.argv) == 3: 
        if sys.argv[2] == "CC":
            print("here")
            CCVariant = True
    
    print("Graph G and independent sets I and J from input.")
    print("Edges of G:", Edges)
    print("Independent set I:", I)
    print("Independent set J:", J)
    
    #Start of GraphCheck.
    print("Check if Graph G is BPG.")
    if not GraphCheck.Check_BPG(Edges):
        print("G is not BPG!")
        end = time.time()
        print("Runtime:", end -start)
        return
    print("Check if I and J are Independent sets for G.")
    if not Check_IS(Edges, I):
        print("I is not independent set for G!")
        end = time.time()
        print("Runtime:", end -start)
        return
    if not Check_IS(Edges, J):
        print("J is not independent set for G!")
        end = time.time()
        print("Runtime:", end -start)
        return
    print("I and J are independent sets for G.")
    
    #Second Section: Find rigid tokens and remove them including neighbours, if present.
    print("Find rigid tokens of I and J.")
    IList = []
    IList.append(I)
    JList = []
    JList.append(J)
    RigidTokensI = Rigid_tokens(Edges, IList)
    RigidTokensJ = Rigid_tokens(Edges, JList)
    #If there are no rigid tokens, skip to IPlus/ CC check.
    if len(RigidTokensI) == 0:
        print( "There are no rigid tokens, the sets are unlocked.")
        if CCVariant:
            print("Linear approach using Token Distribution on Connected Components.")
            CI, CJ = ComponentPrepping.CC_Check(Get_Vertices(Edges), Edges, I, J)
            if CI == CJ:
                print("An independent set reconfiguration sequence exists between I and J under G!")
                ReconfigurationSequence = Reconfiguration.reconfiguration_Search(Edges, I, J, RigidTokensI, ComponentPrepping.Find_Connected_Components(Get_Vertices(Edges),Edges))
                print("A possible reconfiguration sequence from I to J:")
                for item in ReconfigurationSequence:
                    print(item)
                end = time.time()
                print("Runtime:", end -start)
                return
            else:
                print("There can not be an independent set reconfiguration sequence between I and J under G!")
                end = time.time()
                print("Runtime:", end -start)
                return
        skip_to_IPlus(I, J, Get_Vertices(Edges), Edges, start)
        return
    print("There are rigid tokens, continue normally.")
    print("Rigid tokens for I:", RigidTokensI)
    print("Rigid tokens for J:", RigidTokensJ)

    if not Check_Shared_Rigid(RigidTokensI, RigidTokensJ):
        print("Rigid tokens are different!")
        end = time.time()
        print("Runtime:", end -start)
        return
    print("I and J share the same rigid tokens.")   

    #Third section: prepare data for further manipulation
    print("Find the neighbours of the rigid tokens in I.")
    NeighboursRigidI = []
    buff = []
    for i in RigidTokensI:
        buff.append(Vertex_Neighbours(Edges, i))
        for j in buff:
            for k in j:
                if not k in NeighboursRigidI:
                    NeighboursRigidI.append(k)
    print("Rigid tokens including neighbours:", NeighboursRigidI)

    #Start of ComponentPrepping.
    print("Form a new graph G' which is G without the rigid tokens and their neighbours.")
    NewVertices = ComponentPrepping.Form_GNew(Edges, NeighboursRigidI)
    print("New Vertices:", NewVertices)
    # for I+, should have updated graph including edges
    NewEdges = ComponentPrepping.Update_G(Edges, NewVertices)
    print("G' Edges", NewEdges)
    print("Find intersection of components of G' with I and J, forming I' and J'.")
    NewComponentsI = ComponentPrepping.Find_IJC(I, NewVertices)
    print("Intersection with I:", NewComponentsI)
    NewComponentsJ = ComponentPrepping.Find_IJC(J, NewVertices)
    print("Intersection with J:", NewComponentsJ)
    if CCVariant:
        print("Find connected components of the new Graph, compare token distribution between I and J.")
        CI, CJ = ComponentPrepping.CC_Check(NewVertices, NewEdges, NewComponentsI, NewComponentsJ)
        if CI == CJ:
            print("An independent set reconfiguration sequence exists between I and J under G!")
            ReconfigurationSequence = Reconfiguration.reconfiguration_Search(NewEdges, NewComponentsI, NewComponentsJ, RigidTokensI, ComponentPrepping.Find_Connected_Components(NewVertices, NewEdges))
            print("A possible reconfiguration sequence from I to J:")
            for item in ReconfigurationSequence:
                print(item)
            end = time.time()
            print("Runtime:", end -start)
            return
        else:
            print("There can not be an independent set reconfiguration sequence between I and J under G!")
            end = time.time()
            print("Runtime:", end -start)
            return
      
    #Fourth section: IPlus algorithm to determine if there are Possible reconfiguration sequences
    print("Expand I' and J' to I'+ and J'+.")
    IPlusResult = IPlus.Find_IJPlus(NewComponentsI, NewVertices, NewEdges)
    print("I'+:", IPlusResult)
    JPlusResult = IPlus.Find_IJPlus(NewComponentsJ, NewVertices, NewEdges)
    print("J'+:", JPlusResult)

    print("Compare I'+ with J'+.")
    
    #Fifth section: Evaluate result, return sequence if positive.
    if Compare_IJPlus(IPlusResult, JPlusResult):
        print("An independent set reconfiguration sequence exists between I and J under G!")
        print("Find reconfiguration sequence using search algorithm.")

        ReconfigurationSequence = Reconfiguration.reconfiguration_Search(NewEdges, NewComponentsI, NewComponentsJ, RigidTokensI, ComponentPrepping.Find_Connected_Components(NewVertices, NewEdges))
        print("A possible reconfiguration sequence from I to J:")
        for item in ReconfigurationSequence:
            print(item)
        end = time.time()
        print("Runtime:", end -start)
        return
    else:
        print("There can not be an independent set reconfiguration sequence between I and J under G!")
        end = time.time()
        print("Runtime:", end -start)
        return

if __name__ == "__main__":
    main()
