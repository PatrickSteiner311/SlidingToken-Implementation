# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 19:11:46 2022

@author: Patrick Steiner
"""
import SlidingToken


#Input: Graph edges G, start vertex, end vertex
#Output: shortes path in graph between the vertices
#this code bit has been taken from https://onestepcode.com/graph-shortest-path-python/?utm_source=rss&utm_medium=rss&utm_campaign=graph-shortest-path-python
def Breadth_First_Search(Edges, StartVertex, EndVertex):
    if StartVertex == EndVertex:
        return [StartVertex]
    explored = []
    queue = [[StartVertex]]
    
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node not in explored:
            neighbours = SlidingToken.Vertex_Neighbours(Edges, node)
            
            for n in neighbours:
                newPath = list(path)
                newPath.append(n)
                queue.append(newPath)
                
                if n == EndVertex:
                    return newPath
            explored.append(node)
            
    return[]


#Input: Graph edges G, independent sets I and J, rigid tokens R, connected components CC
#Output: Independent set reconfiguration sequence as list reconfigurationSequence
def reconfiguration_Search(Edges, I, J, RigidTokens, CC):
    IC = I.copy()
    JC = J.copy()
    I0 = I + RigidTokens
    I0 = [int(i) for i in I0]
    I0.sort()
    I0 = [str(i) for i in I0]
    reconfigurationSequence = [I0]
    routes = []
    routeCounter = 0
    for component in CC:
        for i in range(len(I)):
            IBuff = str(IC[i]) 
            JBuff = str(JC[i])
            if IBuff in component and JBuff in component:
                #find route between, add to sets etc.
                routes.append(Breadth_First_Search(Edges, IBuff, JBuff))
        for route in routes:
            start = route[0]
            route.remove(start)
            #if the current paths tokens does not have any neighbours that are neighbours for any other paths tokens, we can simply move our tokens directly. 
            #Else we must take precautions as to not create a step that is not an independent set.
            if not any(item in SlidingToken.Vertex_Neighbours(Edges, [item for item in route]) for item in [item for item in SlidingToken.Vertex_Neighbours(Edges,[item for item in routes])]):
                newStep = reconfigurationSequence[routeCounter].copy()
                newStep.remove(start)
                for token in route:
                    newStep.append(token)
                    newStep = [int(i) for i in newStep]
                    newStep.sort()
                    addedStep = newStep.copy()
                    addedStep = [str(i) for i in addedStep]
                    reconfigurationSequence.append(addedStep)
                    newStep = [str(i) for i in newStep]
                    if not token == route[-1]:
                        newStep.remove(token)     
                routeCounter += 1
            else:
                newStep = reconfigurationSequence[routeCounter].copy()
                newStep.remove(start)
                for token in route:
                    #if any neighbours for this specific token are neighbours with tokens from other paths, we put this path on hold.
                    if any(item in SlidingToken.Vertex_Neighbours(Edges, token) for item in [item for item in SlidingToken.Vertex_Neighbours(Edges,[item for item in routes])]):
                        break
                    else:
                        newStep.append(token)
                        newStep = [int(i) for i in newStep]
                        newStep.sort()
                        addedStep = newStep.copy()
                        addedStep = [str(i) for i in addedStep]
                        reconfigurationSequence.append(addedStep)
                        newStep = [str(i) for i in newStep]
                        if not token == route[-1]:
                            newStep.remove(token)     
                    routeCounter += 1
                    
    return reconfigurationSequence
