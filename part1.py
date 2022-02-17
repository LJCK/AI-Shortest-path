#Question: You will need to solve a relaxed version of the NYC instance where we do not have the energy constraint. You can use any algorithm we discussed in the lectures. Note that this is equivalent to solving the shortest path problem. The starting and ending nodes are set to be ‘1’ and ‘50’.

import json,queue
import numpy as np


#load Graph.json
with open('Graph.json','r') as f :
  graph = json.load(f)

def uniform_cost_search(graph, start, goal):
    ''' Function to perform BFS to find path in a graph
        Input  : Graph with the start and goal vertices
        Output : Dict of explored vertices in the graph
    '''
    frontier = queue.PriorityQueue()    # FIFO priority Queue for Frontier
    
    # initialization
    frontier.put(start)         # Add the start node to frontier
    explored = {}               # Dict of explored nodes {node : parentNode}
    explored[start] = None      # start node has no parent node
    processed = 0               # Count of total nodes processed
    
    while not frontier.empty():
        # get next node from frontier
        currentNode = frontier.get()
        processed += 1
        
        # stop when goal is reached
        if currentNode == goal:
            break
        
        # explore every single neighbor of current node
        for nextNode in graph[str(currentNode)]:
           
            # ignore if it has already been explored
            if nextNode not in explored:
                
                # put new node in frontier
                frontier.put(nextNode)
                
                # assign current node as parent
                explored[nextNode] = currentNode
    
    return explored, processed


# Reconstruct the path from the Dict of explored nodes {node : parentNode}
# Intuition : Backtrack from the goal node by checking successive parents

def reconstruct_path(explored, start, goal):
    currentNode = goal             # start at the goal node
    path = []                      # initiate the blank path

    # stop when backtrack reaches start node
    while currentNode != start:
        # grow the path backwards and backtrack
        path.append(currentNode)
        currentNode = explored[str(currentNode)]

    path.append(start)             # append start node for completeness
    path.reverse()                 # reverse the path from start to goal

    return path

start =1
goal =50
nodesExplored, nodesProcessed = uniform_cost_search(graph=graph,start=start,goal=goal)
path = reconstruct_path(nodesExplored,start=start,goal=goal)

print("Total nodes in graph: ",len(graph))
print("total nodes visited: ", nodesProcessed," | ", np.round(100*(nodesProcessed/len(graph),2),"%"))
print("Path through the graph: ",path)