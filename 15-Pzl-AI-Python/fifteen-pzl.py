import sys
from math import sqrt as sr

##########################################################################

class ChuPriorityQueue(object):

    def __init__(self):

        self.elements = []
        self.num = 0

	#########################################################################
	##########################################################################

    def dequeue(self):

        self.num -= 1
        return self.elements.pop()

	##########################################################################
	##########################################################################

    def enqueue(self, element):

        if self.num == 0:

            self.elements.append(element)

        else:

            idx = 0

            for el in self.elements:

                if element.priority > el.priority:

                    self.elements.insert(idx, element)
                    break

                idx += 1

                if idx == self.num:

                    self.elements.append(element)
                    break

        self.num += 1

    ##########################################################################
	##########################################################################

    def isEmpty(self):
        return self.elements == []

    ##########################################################################
	##########################################################################

    def size(self):
        return len(self.elements)

##########################################################################
##########################################################################
#------------------------------------------------------------------------#
##########################################################################
##########################################################################

class ChuStack(object):

    def __init__(self):
        self.elements = []
        self.num = 0

    def length(self):
        return len(self.elements)

    def push(self, item):
        self.elements.append(item)
        self.num += 1

    def look(self):
    	return self.elements[len(self.elements) - 1]

    def pop(self):
        self.num -= 1
        return self.elements.pop()

    def isEmpty(self):
    	return self.elements == []

##########################################################################
##########################################################################
#------------------------------------------------------------------------#
##########################################################################
##########################################################################

class ChuQueue(object):

    def __init__(self):

        self.elements = []
        self.num = 0

    def isEmpty(self):

        return self.elements == []

    def enqueue(self, item):

        self.elements.insert(0, item)
        self.num += 1

    def dequeue(self):

        self.num -= 1
        return self.elements.pop()

    def size(self):
        return len(self.elements)

##########################################################################
##########################################################################
#------------------------------------------------------------------------#
##########################################################################
##########################################################################
#tried comparing my theData structures to the ones that came with python
from sets import Set 
from collections import deque
from heapq import heappush, heappop

class ChuNode():

    def __init__(self, aValue):

    	self.theLevel = 0
        self.theHeuristic = 0
        self.theParent = None
        self.theData = aValue
        self.theGoodPositions = [None] * glbl_branch_factor
        self.theBoard = None
        self.alternateRep()
        
    ##########################################################################
	##########################################################################

    def __repr__(self):

        return self.theData

    ##########################################################################
	##########################################################################

    def changePlaces(self, numberToSwap):

        emptyIdx = self.theData.index(' ')
        numbIndex = self.theData.index(str(numberToSwap))
        newtheData = list(self.theData)
        newtheData[emptyIdx], newtheData[numbIndex] = newtheData[numbIndex], newtheData[emptyIdx]
        newtheData = "".join(newtheData)
        return newtheData

    ##########################################################################
	##########################################################################

    def incrementPlace(self, ChuNode, heuristic = None):

        count = 0

        for pos in self.theGoodPositions:

            if(pos == None):

                self.theGoodPositions[count] = ChuNode
                self.theGoodPositions[count].theParent = self
                self.theGoodPositions[count].theLevel = self.theLevel + 1
                
                if(heuristic != None):

                    self.theGoodPositions[count].theHeuristic = heuristic(self.theGoodPositions[count].theData)
                
                break

            if(pos == None and count == 4):

                print("Error!!!! The size is too large :(")

            count += 1

    ##########################################################################
	##########################################################################
	


    def movingForward(self, heuristic = None):

        
        emptyIdx = self.theData.index(' ')
        emptyColumn = emptyIdx // glbl_S
        emptyRow = emptyIdx % glbl_S
        nodesMade = 0

        if (emptyColumn + 1 < glbl_S):

            newChuNode = ChuNode(self.changePlaces(self.theBoard[emptyRow][emptyColumn + 1]))
            
            if (newChuNode.theData not in visited):
            	
                nodesMade += 1
                self.incrementPlace(newChuNode, heuristic)
                visited.add(newChuNode.theData)
				
        if (emptyRow + 1 < glbl_S):

            newChuNode = ChuNode(self.changePlaces(self.theBoard[emptyRow + 1][emptyColumn]))
            
            if (newChuNode.theData not in visited):

                nodesMade += 1
                self.incrementPlace(newChuNode, heuristic)
                visited.add(newChuNode.theData)

        if (emptyColumn - 1 >= 0):

            newChuNode = ChuNode(self.changePlaces(self.theBoard[emptyRow][emptyColumn - 1]))
            
            if (newChuNode.theData not in visited):

                nodesMade += 1
                self.incrementPlace(newChuNode, heuristic)
                visited.add(newChuNode.theData)

        if (emptyRow - 1 >= 0):

            newChuNode = ChuNode(self.changePlaces(self.theBoard[emptyRow - 1][emptyColumn]))
            
            if (newChuNode.theData not in visited):

                nodesMade += 1
                self.incrementPlace(newChuNode, heuristic)
                visited.add(newChuNode.theData)

        return nodesMade

    ##########################################################################
	##########################################################################

    def alternateRep(self):

        global glbl_S
        posX = 0
        posY = 0
        theLength = len(self.theData)
        glbl_S = int(sr(theLength))

        self.theBoard = [[0 for x in range(glbl_S)] for y in range(glbl_S)]

        for el in self.theData:

            aNewLetter = None

            if(el != ' '):

                aNewLetter = el

            else:

                newLet = 0

            self.theBoard[posX][posY] = aNewLetter

            if posX < glbl_S - 1:

                posX += 1

            else:

                posY += 1
                posX = 0



    ##########################################################################
	##########################################################################

    def printChuNodes(self):

        for ChuNode in self.theGoodPositions:

            if(ChuNode != None):

                print ChuNode.theData

##########################################################################
##########################################################################
#------------------------------------------------------------------------#
##########################################################################
##########################################################################

def getHeuristic(table):

    cost = 0

    for square in table:

        if (goalState.index(square) != table.index(square)):
            cost += 1

    return cost

##########################################################################
##########################################################################

def getHeuristicAStar(table):
	
    return getHeuristic(table) + getHeuristicDistance(table)

##########################################################################
##########################################################################

def floorDivision(a, b):

	return a // b

##########################################################################
##########################################################################

def modularCalc (a, b):

	return a % b

##########################################################################
##########################################################################

def getHeuristicDistance(boardtheData):

    global glbl_S
    heuristicDist = 0

    for square in boardtheData:

        if (square != ' '):

            bdrIdx = boardtheData.index(square)
            brdColumn = floorDivision(bdrIdx, glbl_S)#bdrIdx // glbl_S
            brdRow = modularCalc(bdrIdx, glbl_S) #bdrIdx % glbl_S

            cIdx = goalState.index(square)
            cC = floorDivision(cIdx, glbl_S) # cIdx // glbl_S
            cR = modularCalc(cIdx, glbl_S)  # cIdx % glbl_S

            heuristicDist += abs(brdColumn - cC) + abs(brdRow - cR)

    return heuristicDist

##########################################################################
##########################################################################
#------------------------------------------------------------------------#
##########################################################################
##########################################################################

class ChuTree():

    def __init__(self, root):

        self.root = root
        self.visited = {root.theData}

	##########################################################################
	##########################################################################

    #continously increases depth of the search until a solution is found
    def IDS(self, rootNode):

        thetheLimit = 0
        isFound = -1

        while(isFound == -1):

            thetheLimit += 1
            isFound = self.DLS(rootNode, thetheLimit, True)

        print("IDS; Found here -> ", thetheLimit)

	##########################################################################
	##########################################################################

    def BFS(self, rootNode):

        nodesMade = 0
        nodesExp = 0
        ChuQueue = deque([rootNode])

        while (len(ChuQueue) > 0):

            presentNode = ChuQueue.popleft()
            nodesExp += 1

            if (presentNode.theData == goalState or presentNode.theData == goalStateTwo):
                break
            
            nodesMade += presentNode.movingForward()
            
            for ChuNode in presentNode.theGoodPositions:

                if (ChuNode != None):

                    ChuQueue.append(ChuNode)

        print('Depth: ' + str(presentNode.theLevel) + ', ' + 'Node Created: ' + str(nodesMade) + ', ' + 'Nodes Expanded: ' + str(nodesExp) 
        	+ ', ' + 'Fringe: ' + str(len(ChuQueue)))

	##########################################################################
	##########################################################################

    def DLS(self, rootNode, theLimit, quiet):

        solFound = False
        nodesMade = 0
        Chustack = deque([rootNode])
        nodesExp = 0

        while (len(Chustack) > 0):

            presentNode = Chustack.pop()
            nodesExp += 1

            if (presentNode.theData == goalState or presentNode.theData == goalStateTwo):
                
                solFound = True
                break

            nodesMade += presentNode.movingForward()

            for ChuNode in presentNode.theGoodPositions:

                if (ChuNode != None and ChuNode.theLevel < theLimit):

                    Chustack.append(ChuNode)

        if(solFound == True):

            print('Depth: ' + str(presentNode.theLevel) + ', ' + 'Node Created: ' + str(nodesMade) + ', ' + 'Nodes Expanded: ' + str(nodesExp) 
        	+ ', ' + 'Fringe: ' + str(len(Chustack)))

        else:

            if (quiet == False):

                print("Failed to find a solution to this problem ;(")

            return -1

	##########################################################################
	##########################################################################

    def DFS(self, rootNode):

    	nodesMade = 0
        nodesExp = 0
        Chustack = deque([rootNode])
        
        while (len(stack) > 0):

            presentNode = Chustack.pop()
            nodesExp += 1

            if (presentNode.theData == goalState or presentNode.theData == goalStateTwo):
                break

            nodesMade += presentNode.movingForward()

            for ChuNode in presentNode.theGoodPositions:

                if (ChuNode != None):

                    Chustack.append(ChuNode)

        
        print('Depth: ' + str(presentNode.theLevel) + ', ' + 'Node Created: ' + str(nodesMade) + ', ' + 'Nodes Expanded: ' + str(nodesExp) 
        	+ ', ' + 'Fringe: ' + str(len(ChuQueue)))

	##########################################################################
	##########################################################################

    def ASTAR(self, rootNode, heuristic):

        ChuQueue = [(0, rootNode)]
        nodesMade = 0
        nodesExp = 0

        while(len(ChuQueue) > 0):

            presentNode = heappop(ChuQueue)[1]
            nodesExp += 1

            if (presentNode.theData == goalState or presentNode.theData == goalStateTwo):
                break

            nodesMade += presentNode.movingForward(heuristic)
            presentNode.theHeuristic += presentNode.theLevel

            for ChuNode in presentNode.theGoodPositions:

                if (ChuNode != None):

                    heappush(ChuQueue, (ChuNode.theHeuristic, ChuNode))

        print('Depth: ' + str(presentNode.theLevel) + ', ' + 'Node Created: ' + str(nodesMade) + ', ' + 'Nodes Expanded: ' + str(nodesExp) 
        	+ ', ' + 'Fringe: ' + str(len(ChuQueue)))


	##########################################################################
	##########################################################################

    def algorithmGreedy(self, rootNode, heuristic):

        nodesExp = 0
        ChuQueue = [(0, rootNode)]
        nodesMade = 0

        while(len(ChuQueue) > 0):

            presentNode = heappop(ChuQueue)[1]
            nodesExp += 1

            if (presentNode.theData == goalState or presentNode.theData == goalStateTwo):
                break

            nodesMade += presentNode.movingForward(heuristic)

            for ChuNode in presentNode.theGoodPositions:

                if (ChuNode != None):

                    heappush(ChuQueue, (ChuNode.theHeuristic, ChuNode))

        print('Depth: ' + str(presentNode.theLevel) + ', ' + 'Node Created: ' + str(nodesMade) + ', ' + 'Nodes Expanded: ' + str(nodesExp) 
        	+ ', ' + 'Fringe: ' + str(len(ChuQueue)))

##########################################################################
##########################################################################
##########################MAIN__HERE######################################
##########################################################################
##########################################################################

#THE MAIN METHOD THAT EXECUTES AFTER THE COMMAND LINE IS INPUTTED
if __name__ == '__main__':

	#INITIALIZING VARIABLE NAMES HERE
	table = sys.argv[1]
	ChuTreeSearch = sys.argv[2]
	heuristic = None
	if (len(sys.argv) > 3):
	    heuristic = sys.argv[3]
	goalState = None
	goalStateTwo = '123456789abcdfe '
	glbl_S = 0
	glbl_branch_factor = 4
	visited = set()

	#CHOOSING BETWEEN 8 TABLE OR 15 TABLE
	if(len(table) == 16):	#15 puzzle
	    goalState = '123456789abcdef '
	if(len(table) == 9):	#8 puzzle
	    goalState = '12345678 '

	#INITIALIZING MORE VARIABLES
	rootChuNode = ChuNode(table)
	ChuTree = ChuTree(rootChuNode)


	#CHOOSING WHICH ChuTree SEARCH ALGORITHM
	if(ChuTreeSearch.lower() == 'dfs'):

	    ChuTree.DFS(rootChuNode)

	if(ChuTreeSearch.lower() == 'bfs'):

	    ChuTree.BFS(rootChuNode)

	if(ChuTreeSearch.lower() == 'ids'):

	    ChuTree.IDS(rootChuNode)

	if(ChuTreeSearch.lower() == 'gbfs'):

	    if(heuristic.lower() == 'h1'):

	        ChuTree.algorithmGreedy(rootChuNode, getHeuristic)

	    if(heuristic.lower() == 'h2'):

	        ChuTree.algorithmGreedy(rootChuNode, getHeuristicDistance)

	if(ChuTreeSearch.lower() == 'astar'):

	    if(heuristic.lower() == 'h1'):

	        ChuTree.ASTAR(rootChuNode, getHeuristic)

	    if(heuristic.lower() == 'h2'):

	        ChuTree.ASTAR(rootChuNode, getHeuristicDistance)


'''
END OF PROGRAM
'''