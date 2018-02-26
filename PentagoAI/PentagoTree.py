import ChuStructrues
import PentagoBoard as pb
import Node as nd

import copy
import numpy as np
import sys

'''
Summary: The tree representation of the the PentagoBoard
'''
class PentagoTree(object):

	'''
	Summary: The constructor of the tree. 
	
	Parameters: 
		maxORmin: a string representing if the root node should be.
		          Originally set to max because we are assuming that computer is 
		          looking at his or her turn.
	'''
	def __init__(self, pentagoBoard = pb.PentagoBoard(), maxOrmin = 'max'):

		#The root node that has the final value
		self.root = nd.Node(pentagoBoard.makeCopy(), maxOrmin)

		self.__boardsDone = []

		self.num = 1

	'''
	Summary: Adds a hash of a board to the movesDone list.
	'''
	def __recordHash(self, board):

		boardHash = self.__getHash(board)

		self.__boardsDone.append( boardHash )

	'''
	Summary: Checks if a board has been done before.

	Return: a boolean indicating if this board exists.
	'''
	def __alreadyDone(self, board):

		boardHash = self.__getHash(board)

		if boardHash in self.__boardsDone:
			return True
		else:
			return False

	'''
	Summary: Gets a has of a board.

	Return: an int hash
	'''
	def __getHash(self, board):

		boardStr = np.array2string(board.getNumpyBoard())

		boardHash = hash(boardStr)

		return boardHash


	'''
	Summary: Sets up the AI to choose a move to do.
	
	Parameters:
		depth: an integer denoting the depth of the tree we should populate.
		node: The Node class (object below PentagoTree) we are looking starting from.
		piece: a character 'w' or 'b' that denotes which person's turn it is.
		doPrune: a boolean value that represents whether or not I will perform alpha-beta pruning.

	Return: the best move.
	'''
	def setup(self, depth, node, piece, doPrune):

		if(depth < 0):
			print("Invalid Depth!!!")
			return
		elif(piece is not 'w' and piece is not 'b'):
			print("Invalid Piece!!!")
			return

		rootDepth = 0

		#The stack nodes that represents iterating the tree
		nStack = ChuStructrues.ChuStack()

		node.getBoard().reorderMoves(piece, node.getMinOrMax()) 

		#This will be the root node
		nStack.push(node)

		#Go down to the the depth
		self.__goToDepth(nStack, rootDepth, piece, doPrune, depth)

		#Currently at the node on the bottome left (if a visual version of tree is seen)

		currDepth = nStack.look().getDepth()
		self.__dfs(nStack, piece, doPrune, depth, currDepth)

		#Here we extract the root node to see what the best move is
		rootNode = nStack.pop()

		bestMove = rootNode.getBestMove()

		return bestMove

	'''
	Summary: Actually traverses the tree in a dfs fashion (Assuming we start at the bottom left node).
	'''
	def __dfs(self, nStack, piece, doPrune, treeDepth, currDepth):

		#Base case, we are back at root
		if(currDepth == 0 or nStack.size == 1):
			return

		##################################################################
		#CHILD NODE

		#The current child node
		currNode = nStack.look()

		#Get the values to pass up to the parent node
		value = currNode.getValue()
		bestMove = currNode.getBestMove()
		
		#Now pass it to the parent node
		nStack.pop()

		##################################################################
		#PARENT NODE
		parentNode = nStack.look()
		

		#That child's parent (parentNode)
		shouldPrune = parentNode.propogateUp(value, bestMove, doPrune)

		movesLeft = len(parentNode.getMoves())

		##################################################################
		#AM I DONE WITH THIS NODE?

		#IF ALL THE MOVES HAVE BEEN LOOKED AT OR...IF I AM PRUNING, IS shouldPruen True (beta <= alpha) 11111111111111111111111111111111
		
		if(movesLeft != 0 or shouldPrune == True):

			#switching
			if(piece == 'w'):
				piece = 'b'
			else:
				piece = 'w'

			parentDepth = parentNode.getDepth()
			#Go to the depth of the tree
			self.__goToDepth(nStack, parentDepth, piece, doPrune, treeDepth)

			#SWITCH BACK
			if(piece == 'w'):
				piece = 'b'
			else:
				piece = 'w'

			self.__dfs(nStack, piece, doPrune, treeDepth, currDepth)

		else:

			#Get the values to pass up to the grandparent node
			pValue = parentNode.getValue()
			pBestMove = parentNode.getBestMove()
			
			#Now pass it to the grandparent node
			nStack.pop()

			##################################################################
			#Grandparent NODE
			grandNode = nStack.look()
			grandDepth = nStack.look().getDepth()
		
			shouldPrune = grandNode.propogateUp(pValue, pBestMove, doPrune)

			#Go down to the the depth
			self.__goToDepth(nStack, grandDepth, piece, doPrune, treeDepth)

			#Currently at the node on the bottome left (if a visual version of tree is seen)
			#######################################################################################
			self.__dfs(nStack, piece, doPrune, treeDepth, grandDepth)

			'''
			#switching
			if(piece == 'w'):
				piece = 'b'
			else:
				piece = 'w'

			print(" \nB's next MOVE BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB\n ")

			self.__dfs(nStack, piece, doPrune, treeDepth, currDepth - 1)
			'''
			

	'''
	Summary: Gets the next node and pushes it onto the stack.

	Return: a boolean indicating whether or not the move was already performed
	'''
	def __getNode(self, nStack, currNode, move, piece, currDepth, treeDepth): #d = currDepth

		#Get the board for the next turn
		nextBoard = currNode.testInput(move, piece) #this should remove the same move from the board list
		currNode.removeMove(move) #this was necessary

		#__alreadyDone(self, board):
		#__recordHash(self, board):
		if(self.__alreadyDone(nextBoard)):
			return True

		#Establishes if the child node of the most recent node will be min or max (based on the previous)
		#if the parent is max then the child is min and vice versa
		minOrMax = 'max'
		if(currNode.getMinOrMax() == 'max'):
			minOrMax = 'min'

		nextNode = nd.Node(nextBoard, minOrMax, depth = currDepth + 1)

		#Changes the piece cause that would be the next person's turn
		if(piece == 'w'):
			piece = 'b'
		else:
			piece = 'w'

		#If I build the breadth of my current choice and then reorder the moves up to half the total depht
		#the big O is still O( sqrt(b^d) )  <--- THIS ASSUMES I AM PRUNING
		if(currDepth <= (treeDepth / 2) ):
			nextNode.getBoard().reorderMoves(piece, minOrMax) #reorders the moves 

		nStack.push(nextNode)

		return False



	def __goToDepth(self, nStack, currDepth, piece, doPrune, treeDepth):

		#THIS FOR LOOP COULD BE THE TREE TRAVERSAL
		#This loop looks down the tree if a dfs fashion till a certain depth (to get first move)
		for d in range(currDepth, treeDepth):

			#The node on the top of the stack is the parent node
			currNode = nStack.look()

			if(len(currNode.getMoves()) == 0):
				break

			#If the moves were reordered, this should be the best move
			#If not reordered this is just the first move
			move = currNode.getMoves()[0]
			
			#Pushes the next node noto the stack
			moveAlreadyDone = self.__getNode(nStack, currNode, move, piece, d, treeDepth)

			
			while(len(currNode.getMoves()) != 0 and moveAlreadyDone == True): #change back to true

				move = currNode.getMoves()[0]
				moveAlreadyDone = self.__getNode(nStack, currNode, move, piece, d, treeDepth)

			#Switch pieces
			if(piece == 'w'):
				piece = 'b'
			else:
				piece = 'w'

		#Check the leaves on that tree
		self.__checkLeaves(nStack, piece, doPrune)

	'''
	Summary: Checks the leaves of the node on th top of the stack.
	
	Parameters:
		nStack: the stack representing the tree iteration.
		depth: current depth.
		piece: the character ('b' or 'w') that represents what piece is being used.
		doPrune: a boolean value that represents whether or not I will perform alpha-beta pruning.
	
	'''
	def __checkLeaves(self, nStack, piece, doPrune):

		currNode = nStack.look()

		moves = currNode.getMoves()

		#Looks through all possibile moves given the current game state
		for m in moves:

			#CAN CHECK FOR REPEATS HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1

			currBoard = currNode.testInput(m, piece)

			if(self.__alreadyDone(currBoard) == False):

				mValue = currBoard.getHeuristic(piece) #gets the heurisitic value for that move
				
				prune = currNode.minMaxMove(mValue, m, doPrune) #performs the min max operation

				#THIS CHECKS IF I PRUNE, BUT WITH THE MAY minMaxMove IS SETUP,
				#IF doPrune IS FALSE, IT WILL ALWAYS RETURN FALSE
				#ONLY WHEN doPrune IS SET TO TRUE WILL THERE BE A POSSIBILITY TO RETURN TRUE.
				if(prune == True and doPrune == True):
					break

		#This means we are
		#if(nStack.size == 1)
		'''!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		#See how many moves are left here
		movesLeft = len(currNode.getMoves())

		if(movesLeft == 0):
			print(movesLeft)
			self.__checkLeaves(nStack, currDepth - 1, piece, doPrune, treeDepth)
		else:
			#__getNode(self, nStack, currNode, move, piece, currDepth, treeDepth): #d = currDepth
			nextMove = currNode.getMoves()[0]

			nextNodeDepth = currNode.getDepth()
			self.__getNode(nStack, currNode, nextMove, piece, currDepth, treeDepth)

			self.__checkLeaves(nStack, currDepth, piece, doPrune, treeDepth)
		'''

###############################################################################################
############THE MAIN METHOD THAT EXECUTES AFTER THE COMMAND LINE IS INPUTTED###################
###############################################################################################
if __name__ == '__main__':

	t = PentagoTree()

	am_I_Pruning = True

	print("WELCOME TO PENTAGO!!!!!!!!!\n\n")
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	
	t.setup(2, t.root,'b', am_I_Pruning)
	
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	print("\n_________________\n")


'''
	print(len(t.root.children))
	print(len(t.root.children[0].children))
	print(len(t.root.children[0].children[0].children))
	print(len(t.root.children[0].children[0].children[0].children))
	
	#second move
	cnode1 = t.currNode.children[0] #one of the children
	print(len(cnode1.children))
	t.setup(1, cnode1, 'b')
	print(len(cnode1.children))
	'''

'''
def recursion(self, depth, currDepth, node, piece):

		if(depth == currDepth):
			return

		#The moves that are possible
		moves = node.board.getAvailableCoords() #doesn't affect original
		
		#Populates all the possible moves from that node
		#for d in range(0, depth):
		#	self.layer(node, piece, moves)
		

		nextDepth = currDepth + 1
		#Takes all the children
		children = node.children

		
		#And populates them all
		#for child in children:
		#	self.recursion(depth, nextDepth, child, piece)
		

	

	def __addTurns(self, node, boardIdx, rowIdx, colIdx, piece, boTurnIdx):
		#Gets the board while turning left
		lboard = self.currNode.board.testInput(
			boardIdx, rowIdx, colIdx, piece, tLeft = True, bTurnIdx = boTurnIdx)

		#Gets the board while turning right
		rboard = self.currNode.board.testInput(
			boardIdx, rowIdx, colIdx, piece, tRight = True, bTurnIdx = boTurnIdx)


		#Appends the boards into the list of children
		lnode = Node(rboard, children = [])
		rnode = Node(rboard, children = [])
		node.children.append(lnode)
		node.children.append(rnode)

'''
