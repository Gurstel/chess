
#USE THIS ONE FOR FULL GAME

#I learned modes and importing/using images from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes
#In general, all knowledge of graphics, animations, and overall syntax for code came from https://www.cs.cmu.edu/~112/index.html
#(Look at schedule, then graphics/animations links)


#All sources, explanation, and comments for the actual implemenation of 
#code for playing as black or playing as white are in their respective files
#(white.py/black.py/whiteWithAI.py/blackWithAI.py)

#This is a culmination of a start screen and the game modes to 
#make a user friendly game that is able to switch modes without having to come back
#to the code

#You can play the specific games from their individual files.

#From https://www.cs.cmu.edu/~112/notes/notes-graphics.html
from cmu_112_graphics import *

import white
import black
import whiteWithAI
import blackWithAI


def appStarted(app):
    app.mode = 'startScreenMode'
    app.margin = 50
    app.rows = 8  #chess board dimensions
    app.cols = 8  #chess board dimensions
    app.boardColors = ['wheat2', 'LightSalmon4', 'IndianRed1']
    app.pieceValues = {'p' : -1, 'n' : -3, 'b' : -3, 'r' : -5, 'q' : -9, 'k' : -1000,
                       'P' : 1, 'N' : 3, 'B' : 3, 'R' : 5, 'Q' : 9, 'K' : 1000}
    app.whitesPieces = {'P', 'N', 'B', 'R', 'Q', 'K'}
    app.blacksPieces = {'p', 'n', 'b', 'r', 'q', 'k'}
    app.allPieces = {'P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k'}
    app.pieceImages = getPieceImages(app)
    app.whitesMove = True
    app.startRow, app.startCol = None, None
    app.gameOver = False
    app.pastMoves = []
    app.stalemate = False
    app.checkmate = False
    app.whiteCanCastleRightSide = True
    app.whiteCanCastleLeftSide = True
    app.blackCanCastleRightSide = True
    app.blackCanCastleLeftSide = True
    app.kingImage = app.loadImage('k.png')  #Got pieces from https://github.com/ornicar/lila/issues/3411
    app.blackKingImage = app.loadImage('bk.png')
    app.kingWidth = 400
    app.kingHeight = 400
    app.timerDelay = 1
    app.startGoingRight = False
    app.playerChooses = False
    app.goRight = 0
    app.goLeft = 0

#This is when the user presses back (we don't want to redo start animation)
def reset(app):
    app.mode = 'startScreenMode'
    app.whitesMove = True
    app.startRow, app.startCol = None, None
    app.gameOver = False
    app.pastMoves = []
    app.stalemate = False
    app.checkmate = False
    app.whiteCanCastleRightSide = True
    app.whiteCanCastleLeftSide = True
    app.blackCanCastleRightSide = True
    app.blackCanCastleLeftSide = True
    app.timerDelay = 1

#Returns a dictionary that maps each piece to an image representing that piece
#Got pieces from https://github.com/ornicar/lila/issues/3411
def getPieceImages(app):
    pieceToImage = {}
    gridWidth  = app.width/2 - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    for key in app.pieceValues:
        if key.islower():
            pieceToImage[key] = app.scaleImage(app.loadImage(f'b{key}.png'), 2/9)
        else:
            pieceToImage[key] =  app.scaleImage(app.loadImage(f'{key}.png'), 2/9)
    return pieceToImage


#Dependent on what the user wants to play as, the board will be different
def changeBoard(app):
    if app.mode == 'whiteMode' or app.mode == 'whiteWithAIMode':
        app.board = [
                        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                        ['_', '_', '_', '_', '_', '_', '_', '_'],
                        ['_', '_', '_', '_', '_', '_', '_', '_'],
                        ['_', '_', '_', '_', '_', '_', '_', '_'],
                        ['_', '_', '_', '_', '_', '_', '_', '_'],
                        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
                    ]
    elif app.mode == 'blackMode' or app.mode == 'blackWithAIMode':
        app.board = [
                        ['R', 'N', 'B', 'K', 'Q', 'B', 'N', 'R'],
                        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                        ['_', '_', '_', '_', '_', '_', '_', '_'],
                        ['_', '_', '_', '_', '_', '_', '_', '_'],
                        ['_', '_', '_', '_', '_', '_', '_', '_'],
                        ['_', '_', '_', '_', '_', '_', '_', '_'],
                        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                        ['r', 'n', 'b', 'k', 'q', 'b', 'n', 'r']
                    ]


#Changes screen dependent on which mode user clicks
def startScreenMode_mousePressed(app, event):
    if app.width/2 - 150 < event.x < app.width/2 +150 and app.height/2 - 25 < event.y < app.height/2 + 25:
            app.mode = 'whiteChoice'
    elif app.width/2 - 150 < event.x < app.width/2 +150 and 3*app.height/4 - 25 < event.y < 3*app.height/4 + 25:
            app.mode = 'blackChoice'



#Learned the resize function for tkinter from https://www.geeksforgeeks.org/how-to-resize-image-in-python-tkinter/
#This is for the animated pieces. At certain times, boolean flags turn.
def startScreenMode_timerFired(app):
    app.kingWidth -= 5
    app.kingHeight -= 5
    if app.kingWidth > 100 and app.kingHeight > 100:
        app.kingImage = app.kingImage.resize((app.kingWidth, app.kingHeight))
        app.blackKingImage = app.blackKingImage.resize((app.kingWidth, app.kingHeight))
    else:
        app.startGoingRight = True
        app.startGoingLeft = True
    
    if app.startGoingRight and app.goRight < 2.5*app.width/6:
        app.goRight += 5
        app.goLeft += 5
    elif app.startGoingRight:
        app.playerChooses = True


#This draws the background and calls the functions that draw the start screen
def startScreenMode_redrawAll(app, canvas):
        canvas.create_rectangle(0, 0, app.width, app.height, fill = 'gray23')
        startScreenMode_drawChess(app, canvas)
        startScreenMode_drawLogo(app, canvas)
        startScreenMode_drawChooseSide(app, canvas)


#This draws the logo
def startScreenMode_drawLogo(app, canvas):
    canvas.create_image(app.width/4 + app.goRight, app.height/4, image=ImageTk.PhotoImage(app.kingImage))
    canvas.create_image(3*app.width/4 - app.goLeft, app.height/4, image=ImageTk.PhotoImage(app.blackKingImage))


#This draws the word 'CHESS'
def startScreenMode_drawChess(app, canvas):
    if app.goRight >= 150:
        canvas.create_text(400, app.height/4, text = "C", font = 'Comic 50 bold', fill = 'white')
    if app.goRight >= 200:
        canvas.create_text(450, app.height/4, text = "H", font = 'Comic 50 bold', fill = 'white')
    if app.goRight >= 250:
        canvas.create_text(500, app.height/4, text = "E", font = 'Comic 50 bold', fill = 'white')
    if app.goRight >= 300:
        canvas.create_text(550, app.height/4, text = "S", font = 'Comic 50 bold', fill = 'white')
    if app.goRight >= 350:
        canvas.create_text(600, app.height/4, text = "S", font = 'Comic 50 bold', fill = 'white')


#This draws the two options 
def startScreenMode_drawChooseSide(app, canvas):
    if app.playerChooses:
        canvas.create_rectangle(app.width/2-150, app.height/2-25, app.width/2+150, app.height/2+25,
                                 fill = 'black', outline = 'white', width = 5)
        canvas.create_text(app.width/2, app.height/2, text = "WHITE", font = 'Comic 40 bold', fill = 'white')

        canvas.create_rectangle(app.width/2-150, 3*app.height/4-25, app.width/2+150, 3*app.height/4+25,
                                 fill = 'white', outline = 'black', width = 5)
        canvas.create_text(app.width/2, 3*app.height/4, text = "BLACK", font = 'Comic 40 bold', fill = 'black')




###################
# Whites Choices  #
###################

#Dependent on what is pressed we go into different modes
def whiteChoice_mousePressed(app, event):
    if app.width/2 - 150 < event.x < app.width/2 +150 and app.height/2 - 25 < event.y < app.height/2 + 25:
        app.mode = 'whiteMode'
        changeBoard(app)
    elif app.width/2 - 150 < event.x < app.width/2 +150 and 3*app.height/4 - 25 < event.y < 3*app.height/4 + 25:
        app.mode = 'whiteWithAIMode'
        changeBoard(app)
    elif 0 < event.x < 100 and 0 < event.y < 50:
        reset(app)

#This draws the possible different game modes(pvp, pvc)
def whiteChoice_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'gray23')
    canvas.create_rectangle(app.width/2-150, app.height/2-25, app.width/2+150, app.height/2+25,
                                 fill = 'black', outline = 'white', width = 5)
    canvas.create_text(app.width/2, app.height/2, text = "Player v Player", font = 'Comic 40 bold', fill = 'white')

    canvas.create_rectangle(app.width/2-150, 3*app.height/4-25, app.width/2+150, 3*app.height/4+25,
                                fill = 'white', outline = 'black', width = 5)
    canvas.create_text(app.width/2, 3*app.height/4, text = "Player v AI", font = 'Comic 40 bold', fill = 'black')

    canvas.create_text(10, 0, text = 'Back', font = 'Comic 30 bold', fill = 'white', anchor = 'nw')



####################
#  Blacks Choices  #
####################

#Dependent on what is pressed we go into different modes
def blackChoice_mousePressed(app, event):
    if app.width/2 - 150 < event.x < app.width/2 +150 and app.height/2 - 25 < event.y < app.height/2 + 25:
        app.mode = 'blackMode'
        changeBoard(app)
    elif app.width/2 - 150 < event.x < app.width/2 +150 and 3*app.height/4 - 25 < event.y < 3*app.height/4 + 25:
        app.mode = 'blackWithAIMode'
        changeBoard(app)
    elif 0 < event.x < 100 and 0 < event.y < 50:
        reset(app)

#This draws the possible different game modes(pvp, pvc)
def blackChoice_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'gray23')
    canvas.create_rectangle(app.width/2-150, app.height/2-25, app.width/2+150, app.height/2+25,
                                 fill = 'white', outline = 'black', width = 5)
    canvas.create_text(app.width/2, app.height/2, text = "Player v Player", font = 'Comic 40 bold', fill = 'black')

    canvas.create_rectangle(app.width/2-150, 3*app.height/4-25, app.width/2+150, 3*app.height/4+25,
                                fill = 'black', outline = 'white', width = 5)
    canvas.create_text(app.width/2, 3*app.height/4, text = "Player v AI", font = 'Comic 40 bold', fill = 'white')

    canvas.create_text(10, 0, text = 'Back', font = 'Comic 30 bold', fill = 'white', anchor = 'nw')


###########################
#        White Mode       #
###########################

#This either is for the Back button or calls the mouse pressed from white.py 
def whiteMode_mousePressed(app, event):
    if 0 < event.x < 100 and 0 < event.y < 50:
        reset(app)
    white.mousePressed(app, event)

#Calls the key pressed from white.py 
def whiteMode_keyPressed(app, event):
    white.keyPressed(app, event)

#calls the redrawAll from white.py 
def whiteMode_redrawAll(app, canvas):
    white.redrawAll(app, canvas)
    canvas.create_text(10, 0, text = 'Back', font = 'Comic 30 bold', fill = 'white', anchor = 'nw')



#########################
#   White with AI Mode  #
#########################

#This either is for the Back button or calls the mouse pressed from whiteWithAI.py 
def whiteWithAIMode_mousePressed(app, event):
    if 0 < event.x < 100 and 0 < event.y < 50:
        reset(app)
    whiteWithAI.mousePressed(app, event)

#This is for the AI to be called when its its turn
def whiteWithAIMode_timerFired(app):
    whiteWithAI.timerFired(app)

#Calls the key pressed from whiteWithAI.py 
def whiteWithAIMode_keyPressed(app, event):
    whiteWithAI.keyPressed(app, event)

#calls the redrawAll from whiteWithAI.py 
def whiteWithAIMode_redrawAll(app, canvas):
    whiteWithAI.redrawAll(app, canvas)
    canvas.create_text(10, 0, text = 'Back', font = 'Comic 30 bold', fill = 'white', anchor = 'nw')


#########################
#       Black Mode      #
#########################

#This either is for the Back button or calls the mouse pressed from black.py 
def blackMode_mousePressed(app, event):
    if 0 < event.x < 100 and 0 < event.y < 50:
        reset(app)
    black.mousePressed(app, event)

#Calls the key pressed from black.py 
def blackMode_keyPressed(app, event):
    black.keyPressed(app, event)

#calls the redrawAll from black.py 
def blackMode_redrawAll(app, canvas):
    black.redrawAll(app, canvas)
    canvas.create_text(10, 0, text = 'Back', font = 'Comic 30 bold', fill = 'white', anchor = 'nw')

#########################
#   Black with AI Mode  #
#########################

#This either is for the Back button or calls the mouse pressed from blackWithAI.py 
#This either is for the Back button or calls the mouse pressed from blackWithAI.py 
def blackWithAIMode_mousePressed(app, event):
    if 0 < event.x < 100 and 0 < event.y < 50:
        reset(app)
    blackWithAI.mousePressed(app, event)

#This is for the AI to be called when its its turn
def blackWithAIMode_timerFired(app):
    blackWithAI.timerFired(app)

#Calls the key pressed from blackWithAI.py 
def blackWithAIMode_keyPressed(app, event):
    blackWithAI.keyPressed(app, event)

#calls the redrawAll from blackWithAI.py 
def blackWithAIMode_redrawAll(app, canvas):
    blackWithAI.redrawAll(app, canvas)
    canvas.create_text(10, 0, text = 'Back', font = 'Comic 30 bold', fill = 'white', anchor = 'nw')


def main():
    runApp(width=1000, height=500)

if __name__ == '__main__':
    main()

