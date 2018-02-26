import copy
import numpy as np
from random import shuffle

'''
	self.__board[0] gives...
			[['.' '.' '.']
			 ['.' '.' '.']
			 ['.' '.' '.']]
	
	self.__board[0][0] gives...
			 ['.' '.' '.']

	self.__board[0][0][0] give...
			  '.'
'''

'''
Summary: This class represents and entire Pentago borad. This PentagoBoard has 4 smaller boards
		 within (top left's index is 0, top right's index index 1, bottom left's index is 2, 
		 bottom right's index index 3).
		 +---+---+
		 | 0 | 1 |
		 +---+---+
		 | 2 | 3 |
		 +---+---+
'''

class PentagoBoard(object):
	
	__LEFT = 0 #THE GLOBAL VARIABLE DENOTING A LEFT TURN.
	__RIGHT = 1 #THE GLOBAL VARIABLE DENOTING A RIGHT TURN.

	'''
	Summary: The constructor for PentagoBoard.

	Parameters: 
	  initialBoard(optional): Users have an option to pass a numpy.ndarray into initialBoard
	     					in order to initialize their own version of a pentago board.
	'''
	def __init__(self, initialBoard = np.array([['.', '.', '.'],['.', '.', '.'],['.', '.', '.']])):

		initialBoard = np.copy(initialBoard)

		#Initializes the board
		self.__board = np.array([initialBoard,initialBoard,initialBoard,initialBoard])

		#Variables to calculate the heuristic
		#Each array has 4 elements denoting each length of possible consecutive pieces in a row
		#Index 0 denotes a single piece, while index 1 denotes two in a row, etc.
		self.__bCountArr = [ 0, 0, 0, 0 ] #for the black piece
		self.__wCountArr = [ 0, 0, 0, 0 ] #for the white piece

		#Denotes wheter this board is a copy or not
		self.__isCopy = False

		#Spaces available on the board
		self.__spaceAvail = 36

		#The coordinates of the avialable spaces on the board.
		self.__availCoord = []

		#move: The coordinates of where the move is going to be made along with what board to turn
	  	#		and in what direction (left or right).
  		for b in range(0, 4): #each board
  			for r in range(0, 3): #each row
  				for c in range(0, 3): #each column
  					for tB in range (0, 4): #index of which board to turn.
						#turn left
						self.__availCoord.append([b, r, c, PentagoBoard.__LEFT, tB]) #represents an element
						#turn right
						self.__availCoord.append([b, r, c, PentagoBoard.__RIGHT, tB]) #represents an element
		#print(len(self.availCoord))
		
		#shuffles the possibile moves
		shuffle(self.__availCoord)

		'''
		All the possibile diagnols where you can get 5 in a row
		I KNOW THIS IS REALLY UGLY, BUT I INITIALLY THOUGHT THERE WERE ONLY TWO DIAGONLS
				>.<		>.<		>.<		>.<		>.<		>.<		>.<		>.<
		'''
		self.__slashes = []
		self.__slashes.append(    [  [0, 0, 0], [0, 1, 1], [0, 2, 2],
							  [3, 0, 0], [3, 1, 1], [3, 2, 2]  ]  )
		self.__slashes.append(    [   [1, 0, 2], [1, 1, 1], [1, 2, 0],
						      [2, 0, 2], [2, 1, 1], [2, 2, 0]  ]  )
		self.__slashes.append(    [  [0, 1, 0], [0, 2, 1], [2, 0, 2],
							  [3, 1, 0], [3, 2, 1] ] )
		self.__slashes.append(    [   [0, 0, 1], [0, 1, 2], [1, 2, 0],
						      [3, 0, 1], [3, 1, 2] ] )
		self.__slashes.append(    [  [1, 0, 1], [1, 1, 0], [0, 2, 2],
							  [2, 0, 1], [2, 1, 0] ] )
		self.__slashes.append(    [   [1, 1, 2], [1, 2, 1], [3, 0, 0],
						      [2, 1, 2], [2, 2, 1] ] )


	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	###########################################################################
	###########################################################################
				    		#Utility Methods Start

    	'''
    Summary: Gives you a copy of the numpy version of the board (a copy).

	Return: a numpy array that represents the board (a copy).
	'''
	def getNumpyBoard(self):

		return np.copy(self.__board)

	'''
	Summary: Checks how many spaces are available on the board.

	Return: an integer representing how many spaces are avialable.
	'''
	def spacesAvailable(self):

		return self.__spaceAvail

	

	'''
	Summary: Checks if this PentagoBoard is a copy or a original.

	Return: A boolean denoting if this board is a copy.
	'''
	def isCopy(self):

		return self.__isCopy

	'''
	Summary: Prints the matrix.
	'''
	def printMatrix(self):
		line = "#-------+-------#\n"
		pBString = line
		for bN in range(0, 4, 2):
		    for r in range(0, 3):
		        leftBoardRow = '| ' + str(self.__board[bN][r][0]) + ' ' + str(self.__board[bN][r][1]) + ' ' + str(self.__board[bN][r][2])
		        rightBoardRow = str(self.__board[bN + 1][r][0]) + ' ' + str(self.__board[bN + 1][r][1]) + ' ' + str(self.__board[bN + 1][r][2])
		        pBString += leftBoardRow + ' | ' + rightBoardRow + ' |\n'
		    pBString += line
		print(pBString)	

	'''
	Summary: Gets the list of coordinates that are available.

	Return: a list of coordinates that have all the availalbe coordinates.
	'''
	def getAvailableCoords(self):

		return copy.copy(self.__availCoord)

	'''
	Summary: Makes a deep copy of the board (so any modifications to the copy won't affect original).

	Return: a PentagoBoard (a deep copy of the original).
	'''
	def makeCopy(self):
		acopy = PentagoBoard()
		acopy.__board = np.copy(self.__board)

		acopy.__bCountArr = copy.copy(self.__bCountArr)
		acopy.__wCountArr = copy.copy(self.__wCountArr)

		acopy.__isCopy = self.__isCopy
		acopy.__spaceAvail = self.__spaceAvail

		acopy.__availCoord = copy.copy(self.__availCoord)

		return acopy

	'''
	Summary: Checks if the game is over.

	Return: a boolean of whether the game is over or not.
	'''
	def isGameOver(self):

		return len(self.__availCoord) == 0

	'''
	Summary: Checks if a space if taken.

	Parameters: 
	  boardIdx: an integer from 0-3 that represents which of the 4 boards we use.
	  rowIdx: an integer from 0-3 that represents the index of the row.
	  colIdx: an integer from 0-3 that represents the index of the column.

	Return: return a boolean indicating whether the space is taken.
	'''
	def isTaken(self, boardIdx, rowIdx, colIdx):
		return (self.__board[boardIdx][rowIdx][colIdx] == 'w' or self.__board[boardIdx][rowIdx][colIdx] == 'b')

	'''
	Summary: Calculates a heuristic.

	Parameters:
	  piece: a character (either 'b' or 'w') that represents which piece.

	Return: returns am integer (0 or greater) if a valid piece is given, or -1
	         if piece is invalid.
	'''
	def getHeuristic(self, piece):
		if(piece != 'w' and piece != 'b'): 
			print("Invalid piece")
			return -1
		elif(piece == 'b'):
			return self.__bCountArr[0] + 2 ** self.__bCountArr[1] + 3 ** self.__bCountArr[2] + 4 ** self.__bCountArr[3]
		else:
			return self.__wCountArr[0] + 2 ** self.__wCountArr[1] + 3 ** self.__wCountArr[2] + 4 ** self.__wCountArr[3]


							#Utility Methods End
	###########################################################################
    ###########################################################################

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	###########################################################################
	###########################################################################
						#Input Methods Start

	'''
	Summary: A simplified version of input.

	Parameters:
		move: the move being made, where each element of the array represents a metric of the move.
		piece: the piece that is to be placed on the board.
	'''
	def move(self, move, piece):
		self.input(move[0], move[1], move[2], move[3], move[4], piece)

	'''
	Summary: Takes valid inputs (indeces and a piece), puts it on the board, and check if
			 5 identical consecutive pieces were found.

	Parameters: 
	  boardIdx: an integer from 0-3 that represents which of the 4 boards we use.
	  rowIdx: an integer from 0-3 that represents the index of the row.
	  colIdx: an integer from 0-3 that represents the index of the column.
	  turnDir: a string that says 'left' or 'right' which denotes which direction to turn.
	  boardTurnIdx: the index of the board I want to turn.
	  piece: a character (either 'b' or 'w') that represents which piece.

	Return: return a boolean indicating whether the inputs were valid & 5.
			identical consecutive pieces were found
	'''
	def input(self, boardIdx, rowIdx, colIdx, turnDir, boardTurnIdx, piece):

		#CHECKS FOR VALID INPUTS
		if(piece != 'w' and piece != 'b'): 
			print("Invalid piece")
			return False
		if(boardIdx > 3 or boardIdx < 0 or rowIdx > 3 or rowIdx < 0 or colIdx > 3 or colIdx < 0):
			print("One or more indeces are invalid")
			return False

		#DOUBLE CHECK IF THAT SPACE IS TAKEN
		taken = self.isTaken(boardIdx, rowIdx, colIdx) #checks if the move is valid

		#ONLY INPUTS THE PIECE IF AND ONLY IF A SPACE IS A AVAILALBE AND ALL PARAMETERS ARE VALID
		if(taken == False):
			#Puts the piece in the respective part of the board
			self.__board[boardIdx][rowIdx][colIdx] = piece

			#SINCE THIS MOVE IS DONE, WE REMOVE IT SO YOU CANNOT USE THIS MOVE AGAIN
			self.__availCoord.remove([boardIdx, rowIdx, colIdx, turnDir, boardTurnIdx])

			#THE ROTATION OF A BOARD
			if(turnDir == PentagoBoard.__LEFT):
				self.__rotateLeft(boardTurnIdx) #TURN LEFT OR...
			elif(turnDir == PentagoBoard.__RIGHT):
				self.__rotateRight(boardTurnIdx) #TURN RIGHT

			self.__spaceAvail -= 1 #one less space available

			#HAVE TO MODIFY THE MOVE LIST CAUSE OF THE TURN
			self.modifyCoordinates(boardIdx, rowIdx, colIdx, turnDir, boardTurnIdx)

			#CHECK TO SEE IF YOU HAVE 5 IN A ROW IN THIS RETURN STATEMENT
			return self.checkColumn(boardIdx, colIdx) or self.checkRow(boardIdx, rowIdx) or self.checkDiagonal()
		else:

			#GOING HERE MEANS YOU MADE AN ILLEGAL MOVE (self.isTaken should prevent getting here)
			print("TAKEN")
			return False

	'''
	Summary: An abridged version of the testInput to expedite the process.

	Parameters: 
	  move: The coordinates of where the move is going to be made along with what board to turn
	  		and in what direction (left or right).
	  piece: a character (either 'b' or 'w') that represents which piece.

	Return: a PentagoBoard representing the board with test input.
	'''
	def testInputAbrid(self, move, piece):

		return self.testInput(move[0], move[1], move[2], move[3], move[4], piece)
	
	'''
	Summary: Tests valid inputs (indeces and a piece), puts it on a copy of the board, and calculaes
			 a heuristic.

	Parameters: 
	  boardIdx: an integer from 0-3 that represents which of the 4 boards we use.
	  rowIdx: an integer from 0-3 that represents the index of the row.
	  colIdx: an integer from 0-3 that represents the index of the column.
	  turnDir: a string that says 'left' or 'right' which denotes which direction to turn.
	  boardTurnIdx: the index of the board I want to turn.
	  piece: a character (either 'b' or 'w') that represents which piece.

	Return: a PentagoBoard representing the board with test input.
	'''
	def testInput(self, boardIdx, rowIdx, colIdx, turnDir, boardTurnIdx, piece):

		#CHECKS FOR VALID INPUTS
		if(piece != 'w' and piece != 'b'): 
			print("Invalid piece")
			return False
		if(boardIdx > 3 or boardIdx < 0 or rowIdx > 3 or rowIdx < 0 or colIdx > 3 or colIdx < 0):
			print("One or more indeces are invalid")
			print(boardIdx, rowIdx, colIdx, turnDir, boardTurnIdx)
			return False

		copy = self.makeCopy() #makes a copy
		copy.__isCopy = True #lets me know what the true board is

		#do an input operation on that copy
		copy.input(boardIdx, rowIdx, colIdx, turnDir, boardTurnIdx, piece)
	

		#copy.board[boardIdx][rowIdx][colIdx] = piece
		#copy.checkColumn(boardIdx, colIdx)
		#copy.checkRow(boardIdx, rowIdx)
		#copy.checkDiagonal()

		#print(copy)

		return copy #RETURNS a copy of the board with the test move executed

							#Input Methods End
	###########################################################################
	###########################################################################

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	###########################################################################
	###########################################################################
						#Rotation Related Methods Start

	'''
	Summary: Modifies the Coordinates after you rotate.

	Parameters:
		boardIdx: an integer from 0-3 that represents which of the 4 boards we use.
	  	rowIdx: an integer from 0-3 that represents the index of the row.
	  	colIdx: an integer from 0-3 that represents the index of the column.
	  	turnDir: a string that says 'left' or 'right' which denotes which direction to turn.
	  	boardTurnIdx: the index of the board I want to turn.
	'''
	def modifyCoordinates(self, boardIdx, rowIdx, colIdx, turnDir, boardTurnIdx):

		self.__availCoord = []

		#move: The coordinates of where the move is going to be made along with what board to turn
	  	#		and in what direction (left or right).
  		for b in range(0, 4): #each board
  			for r in range(0, 3): #each row
  				for c in range(0, 3): #each column

					if(self.__board[b][r][c] == '.'):
						for tB in range (0, 4): #index of which board to turn.

							coorL = [b, r, c, PentagoBoard.__LEFT, tB]
							coorR = [b, r, c, PentagoBoard.__RIGHT, tB]

							#turn left
							self.__availCoord.append(coorL) #represents an element
							#turn right
							self.__availCoord.append(coorR) #represents an element

		'''
		theRotatedBoard = self.__board[boardTurnIdx]

		#self.__availCoord

		#Removes all coordinates with on the rotated board
		for row in range(0, 3):
			for col in range(0,3):
				for rotation in range(0, 2):
					for bTI in range (0, 4):

						move = [boardTurnIdx, row, col, rotation, bTI]

						if move in self.__availCoord:
							self.__availCoord.remove(move)


		#Adds the new available elements to the available coords
		for row in range(0, 3):
			for col in range(0,3):
				element = theRotatedBoard[row][col]
				if(element == '.'):
					for rotation in range(0, 2):
						for bTI in range (0, 4):
							move = [boardTurnIdx, row, col, rotation, bTI]
							self.__availCoord.append(move)

		'''



	'''
	Summary: Rotates one of the 4 boards in the PentagoBoard to the right.

	Parameters:
	  boardIdx: an integer (0 - 3) that represents which board the user wants
				to rotate; the integer represent an index on an array of size 4.
	'''
	def __rotateRight(self, boardIdx):
		self.__board[boardIdx] = np.rot90(self.__board[boardIdx], k = 3)

	'''
	Summary: Rotates one of the 4 boards in the PentagoBoard to the left.

	Parameters: 
	  boardIdx: an integer (0 - 3) that represents which board the user wants
				to rotate; the integer represent an index on an array of size 4.
	'''
	def __rotateLeft(self, boardIdx):
		self.__board[boardIdx] = np.rot90(self.__board[boardIdx], k = 1)


						#Rotation Related Methods End
	###########################################################################
	###########################################################################

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	###########################################################################
	###########################################################################
							#Checking Chaining Start

	
	'''
	Summary: Checks if a column has 5 identical consecutive pieces.

	Parameters: 
	  boardIdx: an integer from 0-3 that represents which of the 4 boards we use.
	  colIdx: an integer from 0-3 that represents the index of the column.

	Return: return a boolean indicating whether there is 5 in a column.
	'''
	def checkColumn(self, boardIdx, colIdx):
		#ONLY FOR TESTING#########
		#boardIdx = 0            #
		#colIdx = 1              #
		##########################

		topi = 0 #index of the top board
		bottomi = 0 #index of the bottom board

		if(boardIdx == 0 or boardIdx == 2):
			topi = 0
			bottomi = 2
		else:
			topi = 1
			bottomi = 3

		coor = []

		#Adds the coordinates for the top board
		for row in range(0, 3): #3 is the height of any 1 of the 4 pentago boards
			coor.append([topi, row, colIdx])

		#Adds the coordinates for the top board
		for row in range(0, 3): #3 is the height of any 1 of the 4 pentago boards
			coor.append([bottomi, row, colIdx])

		'''TESTING ROWS 
		a = 0
		for idx in coor:
			if(a == 0 or a == 1 or a == 2 or a == 3 or a == 4):
				self.__board[idx[0]][idx[1]][idx[2]] = 'b'
			else:
				self.__board[idx[0]][idx[1]][idx[2]] = 'w'
			a += 1
		print(self)
		############################TESTING END
		'''

		return self.__chainCheck(coor)

	'''
	Summary: Checks if a row has 5 identical consecutive pieces.

	Parameters: 
	  boardIdx: an integer from 0-3 that represents which of the 4 boards we use.
	  rowIdx: an integer from 0-3 that represents the index of the row.

	Return: return a boolean indicating whether or not 5 in a row was found.
	'''
	def checkRow(self, boardIdx, rowIdx):

		#ONLY FOR TESTING#########
		boardIdx = 0            #
		rowIdx = 2              #
		##########################

		lefti = 0 #index of the left board
		righti = 0 #index of the right board

		if(boardIdx < 2):
			lefti = 0
			righti = 1
		else:
			lefti = 2
			righti = 3

		coor = []

		#Adds the coordinates for the left board
		for col in range(0, 3): #3 is the width of any 1 of the 4 pentago boards
			coor.append([lefti, rowIdx, col])

		#Adds the coordinates for the right board
		for col in range(0, 3): #3 is the width of any 1 of the 4 pentago boards
			coor.append([righti, rowIdx, col])
		#The coordinates

		'''TESTING ROWS
		a = 0
		for idx in coor:
			if(a == 0 or a == 1 or a == 2 or a == 3 or a == 4):
				self.__board[idx[0]][idx[1]][idx[2]] = 'b'
			else:
				self.__board[idx[0]][idx[1]][idx[2]] = 'w'
			a += 1

		print(self)
		############################TESTING END
		'''

		return self.__chainCheck(coor)

	'''
	Summary: Checks if any of the two diagonals have 5 identical consecutive pieces.

	Return: return a boolean indicating whether or not 5 in a row was found.
	'''
	def checkDiagonal(self):
		''' TESTING DIAGONALS
		a = 0
		for idx in self.__forSlash:
			if(a == 0 or a == 1 or a == 2 or a == 3 or a == 4):
				self.__board[idx[0]][idx[1]][idx[2]] = 'w'
			else:
				self.__board[idx[0]][idx[1]][idx[2]] = 'b'
			a += 1
		print(self)
		'''
		hasWon = False

		for slash in self.__slashes:
			hasWon = hasWon or self.__chainCheck(slash)

		return hasWon

	'''
	Summary: Given a list of consecutive coordinates, checks to see if 5 
			 identical consecutive pieces exist.

	Parameters:
	  coor: the list of coordinates on the PentagoBoard (assumes they're consecutive).

	Return: return a boolean indicating whether or not 5 in a row was found.
	'''
	def __chainCheck(self, coor):

		#the 2 possible chains of black pieces
		bchain1 = 0
		bchain2 = 0

		#the 2 possible chains of white pieces
		wchain1 = 0
		wchain2 = 0

		#the loop counter
		count = 1

		#Looks for 5 in a row in that row
		for idx in coor:
			value = self.__board[idx[0]][idx[1]][idx[2]]
			if(value == 'b'):
				if(count == 1):
					bchain1 += 1
				elif(count == 6):
					bchain2 += 1
				else:
					bchain1 += 1
					bchain2 += 1
			elif(value == 'w'):
				if(count == 1):
					wchain1 += 1
				elif(count == 6):
					wchain2 += 1
				else:
					wchain1 += 1
					wchain2 += 1
			count += 1

		
		#IF THIS EXECUTES, SOMEONE HAS WON THE GAME
		if((bchain1 == 5 or bchain2 == 5) and self.__isCopy == False):
			print("BLACK WINS PENTAGO!!!")
			return True
		elif((wchain1 == 5 or wchain2 == 5) and self.__isCopy == False):
			print("WHITE WINS PENTAGO!!!")
			return True

		
		#UPDATE THE HEURISITC!!!!!!!!!!!!!!!!!!!!HEURISTIC!!!!!!!!!!!!!!!!!!!!HEURISTIC!!!!!!!!!!!!!!!!!!!!!!!!!!!!HEURISTIC!!!!!
		#self.__bCountArr = [ 0, 0, 0, 0 ] #for the black piece
		#self.__wCountArr = [ 0, 0, 0, 0 ] #for the white piece
		if(bchain1 > 0 and bchain1 < 5):
			self.__bCountArr[bchain1 - 1] += 1
		if(bchain2 > 0 and bchain2 < 5):
			self.__bCountArr[bchain2 - 1] += 1
		if(wchain1 > 0 and wchain1 < 5):
			self.__wCountArr[wchain1 - 1] += 1
		if(wchain2 > 0 and wchain2 < 5):
			self.__wCountArr[wchain2 - 1] += 1


		#No 5 in a row was found
		return False


					#Checking Chains End
	###########################################################################
	###########################################################################

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	###########################################################################
	###########################################################################
						#Sort Possibile Moves Start

	'''
	Summary: Reorders a singe breadth layer of so the best options are on the left.
			 (the depth you do this should be half of the depth for the entire tree).

	Parameters: 
		breadthList: the list of elements that represent a breadth layer
					 (assumes the list given isn't encapsulated).
		 minOrMax: a string that represents if this node is a min node or a max node.
	'''
	def reorderMoves(self, piece, minOrMax):

		#Makes the heuristic breadth layer for this board as a list of heuristic values
		heurBreadthLayer = self.__breadthLayer(piece)

		#Reorder the moves array so the best moves are to the left
		if(minOrMax == 'min'):
			self.sortLeastToGreatest(heurBreadthLayer)
		else:
			self.sortGreatestToLeast(heurBreadthLayer)

	'''
	Summary: Creates a breadth heuristic layer based all the possibile moves from the board's current state.

	Return: a list of integers representing the heurisitc of each respective move in self.__availCoord
	'''
	def __breadthLayer(self, piece):

		heuristicList = []

		#Iterating through all the possible moves
		for m in self.__availCoord:

			board = self.testInputAbrid(m, piece)

			heuristicList.append(board.getHeuristic(piece))

		return heuristicList

	###################
	#GREATEST TO LEAST

	'''
	Summary: sorts the self.__availCoord from greatest to least based on heurisitc value of each (MOR MAX NODE).

	Parameters: 
		heurBreadthLayer: the layer representing the heurisitc value of each respective move in self.__availCoord
	'''
	def sortGreatestToLeast(self, heurBreadthLayer):
		
		self.__availCoord = [x for _, x in sorted(zip(heurBreadthLayer,self.__availCoord), 
							 key = lambda pair: pair[0], reverse = True)]
   		
	
	###################
	#LEAST TO GREATEST

	'''
	Summary: sorts the self.__availCoord from least to greatest based on heurisitc value of each (FOR MIN NODE).
			
	Parameters: 
		heurBreadthLayer: the layer representing the heurisitc value of each respective move in self.__availCoord
	'''
	def sortLeastToGreatest(self, heurBreadthLayer):

   		self.__availCoord = [x for _, x in sorted(zip(heurBreadthLayer, self.__availCoord), 
   							 key = lambda pair: pair[0])]  

						#Sort Possibile Moves End
	###########################################################################
	###########################################################################

	'''
	Removes a move.
	'''
	def removeMove(self, move):
		#self.__availCoord.remove([boardIdx, rowIdx, colIdx, turnDir, boardTurnIdx])
		#self.testInput(, move[1], move[2], move[3], move[4], piece)
		self.__availCoord.remove(move)

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
					    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
###############################################################################################
#THE MAIN METHOD THAT EXECUTES AFTER THE COMMAND LINE IS INPUTTED##############################
###############################################################################################
if __name__ == '__main__':

	#PLAYER COMMANDS
	#ENTER YOUR MOVE: (the board#) (the row#) (the column#)
    # may need to subtract row & column number by one
	# cause they see it as 1-4, but it's indexed as 0-3
	
	#TESTING THE PENTAGO BOARD
	#pB = PentagoBoard(np.array([['a', 'b', 'c'],['d', 'e', 'f'],['g', 'h', 'i']]))s
	pB = PentagoBoard()
	
	#Checks if the available coordinates works
	#print(pB.getAvailableCoords())
	#pB.input(0,0,0, 'w')
	#pB.input(0,0,1, 'w')
	#print("----")
	#print(pB.getAvailableCoords())

	#a = pB.isTaken(1,1,1)
	#print(a)

	#print(pB)

	''' ROTATE TEST
	print(" ")
	pB.__rotateLeft(0)
	pB.__rotateRight(1)
	pB.__rotateLeft(2)
	pB.__rotateRight(3)
	print(pB)
	'''

	'''
	#TESTING INPUT METHOD -> input(self, boardIdx, rowIdx, colIdx, piece) 
	print(pB.input(0, 0, 2, 'w'))
	print(pB.input(0, 1, 2, 'w'))
	print(pB.input(0, 2, 2, 'w'))
	print(pB.input(2, 0, 2, 'w'))
	#print(pB.input(2, 1, 2, 'w'))
	print(pB)
	'''

	''' 
	#TESTING testInput(self, boardIdx, rowIdx, colIdx, piece)
	print("0")
	print(pB.testInput(0, 1, 2, 'w'))
	pB.input(0, 0, 2, 'w')
	
	print("\n____________\n1")
	print(pB.testInput(0, 1, 2, 'w'))
	pB.input(0, 1, 2, 'w')
	
	print("\n____________\n2")
	print(pB.testInput(0, 2, 2, 'w'))
	pB.input(0, 2, 2, 'w')
	
	print("\n____________\n3")
	print(pB.testInput(2, 0, 2, 'w'))
	pB.input(2, 0, 2, 'w')

	print("\n____________\n4")
	print(pB.testInput(2, 1, 2, 'w'))
	'''

	#pB = PentagoBoard()
	#print(pB)
	print("\nPentago Done!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
