import json, queue, math
with open("Distance.json","r") as distance :
    dis =json.load(distance)
with open("Graph.json","r") as g :
    graph = json.load(g)
with open("Cost.json","r") as cost :
    budget = json.load(cost)
with open("Coordinate.json","r") as coor :
    coordinate = json.load(coor)

def uniform_cost_search_part1( start, goal):
   
    frontier = queue.PriorityQueue()    # FIFO Queue for Frontier

    # initialization
    frontier.put((0,start))         # Add the start node to frontier
    explored = {}               # Dict of explored nodes {node : parentNode}
    explored[start] = None      # start node has no parent node
    pathcost = {}               # Dict of path distane {node : distance}
    pathcost[start]=0           # start node has no distance
    processed = 0               # Count of total nodes processed
    
    while not frontier.empty():
        # get next node from frontier
        
        currentNode = frontier.get()[1]
        processed += 1
        
        # stop when goal is reached
        
        if currentNode == goal:
            break
        
        # explore every single neighbour of current node
        for nextNode in graph[str(currentNode)]:

            # compute the new distance for the node based on the current node
            weight = dis[str(currentNode)+','+str(nextNode)]
            newcost = pathcost[currentNode] + weight

            # ignore if it has already been explored and new path distance is larger than old path distance
            if (nextNode not in explored) or (newcost < pathcost[nextNode]):

                # set priority as newcost 
                priority = newcost
                
                # put new node in frontier with priority
                frontier.put((priority, nextNode))
                
                # assign current node as parent
                explored[nextNode] = currentNode
                
                # keep track of the updated path cost
                pathcost[nextNode] = newcost
    
    return explored, pathcost, processed

def uniform_cost_search_part2( start, goal):
    
    frontier = queue.PriorityQueue()    # FIFO Queue for Frontier
    
    # initialization
    frontier.put((0,start))         # Add the start node to frontier
    explored = {}               # Dict of explored nodes {node : parentNode}
    explored[start] = None      # start node has no parent node
    pathbudget = {}             # Dict of path energy cost {node : cost}
    pathbudget[start] = 0       # start node has no cost
    pathcost = {}               # Dict of path distane {node : distance}
    pathcost[start]=0           # start node has no distance
    processed = 0               # Count of total nodes processed
    
    while not frontier.empty():
        # get next node from frontier
        
        currentNode = frontier.get()[1]
        processed += 1
        
        # stop when goal is reached
        if currentNode == goal:
            break
        
        # explore every single neighbour of current node
        for nextNode in graph[str(currentNode)]:

            # compute the new energy cost for the node based on the current node
            energycost = budget[str(currentNode)+','+str(nextNode)]
            newbudget = pathbudget[currentNode]+energycost

            # compute the new distance for the node based on the current node
            weight = dis[str(currentNode)+','+str(nextNode)]
            newcost = pathcost[currentNode] + weight

            # ignore if it has already been explored and new path distance is larger than old path distance and energy cost exceed the limit 
            if ((nextNode not in explored) or (newcost < pathcost[currentNode])) and (newbudget<=287932) :
                
                # set priority as newcost 
                priority = newcost
                
                # put new node in frontier with priority
                frontier.put((priority, nextNode))
                
                # keep track of the updated path budget
                pathbudget[nextNode] = newbudget
                
                # assign current node as parent
                explored[nextNode] = currentNode
                
                # keep track of the updated path cost
                pathcost[nextNode] = newcost
    
    return explored, pathcost, processed

def heuristic(nodeA, nodeB):
    (xA, yA) = coordinate[nodeA]
    (xB, yB) = coordinate[nodeB]
    
    return math.sqrt((xA-xB)*(xA-xB)+(yA-yB)*(yA-yB))

def astar_search_part3(start, goal):
    ''' Function to perform A*S to find path in a graph
        Input  : Graph with the start and goal vertices
        Output : Dict of explored vertices in the graph
    '''
    frontier = queue.PriorityQueue()      # Priority Queue for Frontier
    
    # initialization
    frontier.put((0, start))    # Add the start node to frontier with priority 0
    explored = {}               # Dict of explored nodes {node : parentNode}
    explored[start] = None      # start node has no parent node
    pathbudget = {}             # Dict of path energy cost {node : cost}
    pathbudget[start] = 0       # start node has no cost
    pathcost = {}               # Dict of path distane {node : distance}
    pathcost[start] = 0         # start node has no distance
    processed = 0               # Count of total nodes processed
    
    while not frontier.empty():
        # get next node from frontier
        currentNode = frontier.get()[1]
        processed += 1
        
        # stop when goal is reached
        if currentNode == goal:
            break
        
        # explore every single neighbour of current node
        for nextNode in graph[str(currentNode)]:
            
            # compute the new energy cost for the node based on the current node
            energycost = budget[str(currentNode)+','+str(nextNode)]
            newbudget = pathbudget[currentNode]+energycost
            
            # compute the new distance for the node based on the current node
            weight = dis[str(currentNode)+','+str(nextNode)]
            newcost = pathcost[currentNode] + weight
            
            # ignore if it has already been explored and new path distance is larger than old path distance
            if ((nextNode not in explored) or (newcost < pathcost[nextNode])) and (newbudget<=287932):
        
                # set priority as newcost 
                priority = newcost + heuristic(nextNode, goal)
                
                # put new node in frontier with priority
                frontier.put((priority, nextNode))
                
                pathbudget[nextNode] = newbudget
                
                # assign current node as parent
                explored[nextNode] = currentNode
                
                # keep track of the updated path cost
                pathcost[nextNode] = newcost
        
    return explored, pathcost, processed

def reconstruct_path(explored, start, goal, question):
    currentNode = goal             # start at the goal node
    path = []                      # initiate the blank path
    energycost = 0
    # stop when backtrack reaches start node
    while currentNode != start:
        # grow the path backwards and backtrack
        path.append(currentNode)
        energycost = energycost + budget[str(currentNode)+','+explored[str(currentNode)]]
        currentNode = explored[str(currentNode)]

    path.append(start)             # append start node for completeness
    path.reverse()                 # reverse the path from start to goal

    return path, energycost

start =("1")
goal =("50")

# Task 1
nodesExplored_part1, pathsExplored_part1, nodesProcessed_part1 = uniform_cost_search_part1(start = start, goal = goal)
path_part1,energycost_part1 = reconstruct_path(nodesExplored_part1, start = start, goal = goal, question=1)

print("Task 1:")
# print("Total nodes in graph: ",len(graph))
# print("total nodes visited: ", nodesProcessed_part1)
# print("Path through the graph: ",path_part1)
print("Shortest Path: ",end='')
print(*path_part1,sep="->")
# print("Number of nodes traversed: ", len(path_part1))
print("Shortest distance: ", pathsExplored_part1[path_part1[-1]])
print("\n\n")

# Task 2
nodesExplored_part2, pathsExplored_part2, nodesProcessed_part2 = uniform_cost_search_part2(start = start, goal = goal)
path_part2, energycost_part2 = reconstruct_path(nodesExplored_part2, start = start, goal = goal,question=2)

print("Task 2:")
# print("Total nodes in graph: ",len(graph))
# print("total nodes visited: ", nodesProcessed_part2)
# print("Path through the graph: ",path_part2)
print("Shortest Path: ",end='')
print(*path_part2,sep="->")
# print("Number of nodes traversed: ", len(path_part2))
print("Shortest distance: ", pathsExplored_part2[path_part2[-1]])
print("Total energy cost: ", energycost_part2)
print("\n\n")

# Task 3
nodesExplored_part3, pathsExplored_part3, nodesProcessed_part3 = astar_search_part3(start = start, goal = goal)
path_part3, energycost_part3 = reconstruct_path(nodesExplored_part3, start = start, goal = goal,question=3)

print("Task 3:")
# print("Total nodes in graph: ",len(graph))
# print("total nodes visited: ", nodesProcessed_part3)
# print("Path through the graph: ",path_part3)
print("Shortest Path: ",end='')
print(*path_part3,sep="->")
# print("Number of nodes traversed: ", len(path_part3))
print("Shortest distance: ", pathsExplored_part3[path_part3[-1]])
print("Total energy cost: ", energycost_part3)