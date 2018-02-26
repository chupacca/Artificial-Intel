import PentagoBoard as pb 
import PentagoTree as pt 

import numpy as np
import random

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#THE STARTING VARIABLES

AIpiece = 'w'
myPiece = 'b'

print("AI's piece is 'w' and the player's piece is 'b'\n")

am_I_pruning = True

depth = 2

whoTurn = ""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def interpretMove(myMove):

	boardIdx = ord(myMove[0]) - 49

	rowIdx = ord(myMove[2]) - 49
	
	if(rowIdx < 4):
		rowIdx = 0
	elif(rowIdx < 7):
		rowIdx = 1
	else:
		rowIdx = 2

	colIdx = ord(myMove[2]) - 48
	if(colIdx == 1 or colIdx == 4 or colIdx == 7):
		colIdx = 0
	elif(colIdx == 2 or colIdx == 5 or colIdx == 8):
		colIdx = 1
	else:
		colIdx = 2

	rotateDir = myMove[5]
	if(rotateDir == 'R' or rotateDir == 'r'):
		rotateDir = 1
	elif(rotateDir == 'L' or rotateDir == 'l'):
		rotateDir = 0

	move = [ boardIdx, rowIdx, colIdx, rotateDir, ord(myMove[4]) - 49, myPiece]

	return move

def aiTurn(gameBoard):
	#Create the AI
	ai = pt.PentagoTree(pentagoBoard = gameBoard)
	print("AI's TURN")

	#Find the best move and then make it
	aiMove = ai.setup(depth, ai.root, AIpiece, am_I_pruning)
	gameBoard.move(aiMove, AIpiece)

	gameBoard.printMatrix()
	#print(len(gameBoard.getAvailableCoords()))

	whoTurn = "AI"

	#Check if game is over ##############################################
	stillPlaying = not(gameBoard.isGameOver())

	return stillPlaying

def playerTurn(gameBoard):
	#My Move########################################################
	valid = False

	#Obtain valid input from the user____________________________________________
	while(valid == False):

		inputMove = raw_input("Enter Move : \n")

		myMove = interpretMove(inputMove)

		if(len(inputMove) == 6 and len(myMove) == 6 and gameBoard.isTaken(myMove[0], myMove[1], myMove[2]) == False):

			valid = True

	#_________________________________________________________________________

	#Make the move
	gameBoard.move(myMove, myPiece)

	gameBoard.printMatrix()
	#print(len(gameBoard.getAvailableCoords()))

	whoTurn = "Human"

	stillPlaying = not(gameBoard.isGameOver())

	return stillPlaying

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

print("Welcome To Pentago!!!\n\nBoard Format:\n")

partboard = np.array([['1', '2', '3'],['4', '5', '6'],['7', '8', '9']])
formatBoard = pb.PentagoBoard(initialBoard = partboard)

print(" Game    Game ")
print(" Block    Block ")
print("    1       2")
formatBoard.printMatrix()
print(" Game    Game ")
print(" Block    Block ")
print("    3       4\n")

print("Move Examples:\n2/3 1R \n4/8 3L \n1/5 4R")
print("(GameBlock#)/(BlockIndex) (GameBlock#2)(L or R meaning left or right) ")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

stillPlaying = True
gameBoard = pb.PentagoBoard()

print("\nGame Start__________________________________\n\nStarting Board:")
gameBoard.printMatrix()

#Random Number Generator to determine who goes first
whoGoesFirst = random.randint(1, 100) % 2

if(whoGoesFirst == 0):
	print("AI goes first")
	stillPlaying = aiTurn(gameBoard)
	stillPlaying = playerTurn(gameBoard)
else:
	print("Player goes first")
	stillPlaying = playerTurn(gameBoard)

while(stillPlaying == True):

	#Check if game is over ##############################################
	stillPlaying = aiTurn(gameBoard)

	#Check if game is over ##############################################
	stillPlaying = playerTurn(gameBoard)

print("\n" + whoTurn + " WINS PENTAGO!!!")


