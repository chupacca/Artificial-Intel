import ChuStructrues

import copy
import sys

'''
Summary: The nodes that the PentagoTree uses
'''
class Node(object):

	'''
	Summary: The construcor for making a node in a min or max tree.
	
	Parameters: 
		board: The PentgoBoard itself (from the PentagoClass).
		minOrMax:  string representing if this is a MIN or MAX node.
		depth: the DEPTH this node is at.

		value: The value of the node.
		alpha: the alpha value (in terms of alpha-beta pruning).
		beta:  the alpha value (in terms of alpha-beta pruning).

	'''
	def __init__(self, board, minOrMax, value = None, depth = 0):
		
		self.__board = board #make a copy for encapsulation
		self.__minOrMax = minOrMax
		self.__depth = depth

		self.__bestMove = self.getMoves()[0] #What is the move that I'm actually going to make
									  #(it's an array of [boardIdx, rowIdx, colIdx, 
									  #turnDirection, and index of board to turn]).

		self.__value = value
		self.__alpha = -sys.maxint - 1
		self.__beta = sys.maxint

	'''
	Summary: Gets a copy of the list of board.

	Return: a list of possibile moves.
	'''
	def getBoard(self):

		return self.__board

	def minMaxMove(self, value, move, checkPrune):

		if(self.__minOrMax == 'min'):
			self.__min(value, move, checkPrune)
		else:
			self.__max(value, move, checkPrune)

	'''
	Summary: This method checks an inputValue to see if it's less that value and beta.
	
	Parameters: 
		testValue (The value that is being checked in it will become the new value; should be an integer representing the heuristic).
		whichMove: the move that is being checked.
		checkPrune (a boolean indicating if I shold perform alpha-beta pruning).
	
	Returns: a boolean representing whether or not pruning should be done.
			 (if you don't want to check for alpha-beta pruning just don't utilize the return value).
	'''
	def __min(self, testValue, whichMove, checkPrune):
		if(self.__minOrMax != 'min'): #this method won't execute in this node is a min node
			print("Invalid Min Operation")
			return

		#VALUE OPERATION
		if(self.__value is None): #If self.__value is None, then just set self.__value to testValue
			self.__value = testValue
			self.__bestMove = whichMove #and denotes the best move from that node

		elif(testValue < self.__value): #Set self.__value to testValue if testValue is smaller
			self.__value = testValue
			self.__bestMove = whichMove #and denotes the best move from that node

		#PRUNING OPERATION (if executed)
		if(checkPrune == True): #Only executes if we're doing alpha-beta pruning
			if(testValue < self.__beta): #self.__beta is only replaced if testValue is smaller
				self.__beta = testValue
			return self.shouldPrune()

		return False #always return false unless you're checking for alpha-beta pruning

	'''
	Summary: his method checks an inputValue to see if it's greater that value and alpha.
	
	Parameters: 
		testValue (The value that is being checked in it will become the new value).
		whichMove: the move that is being checked.
		checkPrune (a boolean indicating if I shold perform alpha-beta pruning).
	
	Returns: a boolean representing whether or not pruning should be done.
			 (if you don't want to check for alpha-beta pruning just don't utilize the return value; should be an integer representing the heuristic).
	'''
	def __max(self, testValue, whichMove, checkPrune):
		if(self.__minOrMax != 'max'): #this method won't execute in this node is a max node
			print("Invalid Max Operation")
			return

		#VALUE OPERATION
		if(self.__value is None): #If self.__value is None, then just set self.__value to testValue
			self.__value = testValue
			self.__bestMove = whichMove #and denotes the best move from that node

		elif(testValue > self.__value): #Set self.__value to testValue if testValue is greater
			self.__value = testValue
			self.__bestMove = whichMove #and denotes the best move from that node

		#PRUNING OPERATION (if executed)
		if(checkPrune == True): #Only executes if we're doing alpha-beta pruning
			if(testValue > self.__alpha): #self.__alpha is only replaced if testValue is greater
				self.__alpha = testValue
			return self.shouldPrune()

		return False #always return false unless you're checking for alpha-beta pruning

	'''
	Summary: a method that determines if pruning should be done.
	Return: a boolean indicating if pruning should be done.
	'''
	def shouldPrune(self):
		return (self.__beta <= self.__alpha)

	'''
	Summary: Compares metrics determined by the child and this node's and swaps if necessary.

	Return: a boolean indicating if pruning should be done (if do Prune is false will always return false)
	'''
	def propogateUp(self, value, move, doPrune):

		#If this is a min node
		if(self.__minOrMax == 'min'):
			
			#Check if the value is smaller
			if(value < self.__value or self.__value == None):
				self.__value = value
				self.__bestMove = move

			#Update beta if allowed
			if(self.__value < self.__beta):
				self.__beta = self.__value


		#IF this is a max node
		else:
			
			#Check if the value is smaller
			if(value > self.__value or self.__value == None):
				self.__value = value
				self.__bestMove = move

			#Update beta if allowed
			if(self.__value > self.__alpha):
				self.__alpha = self.__value

				
		#shoud we prune?
		if(doPrune == False):
			return False

		return self.shouldPrune() #boolean if we should actually prune or not


	'''
    Summary: Does a test input on the board.

    Parameters:
    	move: the move that's being made.
    	piece: the piece the move is being done on.

	Return: a board that represents that board with this test input implemented.
    '''
	def testInput(self, move, piece):

		return self.__board.testInputAbrid(move, piece)

   	##################################
	############GETTERS###############
	##################################

	'''
	Removes a move
	'''
	def removeMove(self, move):
		self.__board.removeMove(move)

	'''
	Summary: Gets the depth of that this node is on.

	Return: an integer that represents the depth.
	'''
	def getDepth(self):

		return self.__depth

	'''
	Summary: Gets the string minOrMax.

	Return: a string that represents if this node is a min node or a max node.
	'''
	def getMinOrMax(self):

		return self.__minOrMax

	'''
	Summary: Gets a copy of the list of moves.

	Return: a list of possibile moves.
	'''
	def getMoves(self):

		return self.__board.getAvailableCoords()

	'''
	Summary: Gives you the value of this node (should be the heurisitc of the best move).

	Return: an integer representing the value.
	'''
	def getValue(self):

		return self.__value

	'''
	Summary: Gives you the best move of this node.

	Return: an array where the array's values represent the move being made representing the value.
	'''
	def getBestMove(self):

		return self.__bestMove

	'''
	Summary: Gives you the alpha value.

	Return: an integer representing the alpha.
	'''
	def getAlpha(self):

		return self.__alpha

	'''
	Summary: Gives you the beta value.

	Return: an integer representing the beta.
	'''
	def getBeta(self):

		return self.__beta

	##################################
	############SETTERS###############
	##################################

	'''
	Summary: Sets the string minOrMax.

	Parameters: 
		minOrMax: a string that represents if this node is a min node or a max node.
	'''
	def setMinOrMax(self, minOrMax):

		self.__minOrMax = minOrMax


	'''
	Summary: Changes the alpha value.

	Parameters:
		alpha: the int value to set as alpha
	'''
	def setAlpha(self, alpha):

		self.__alpha = alpha

	'''
	Summary: Changes the beta value.

	Parameters:
		beta: the int value to set as beta
	'''
	def setBeta(self, beta):

		self.__beta = beta

	'''
	Summary: Changes the node's value.

	Parameters:
		value: the int that will be the node's new value.
	'''
	def setValue(self, value):

		self.__value = value

	'''
	Summary: Changes the best move of this node.

	Parameters:
		move: an array of integers where the elements represent what move is chosen.
	'''
	def setBestMove(self, move):

		self.__bestMove = move


