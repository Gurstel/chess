#All code is written and thought out solely by me, unless otherwise stated(ex. 15-112 website). 
#I asked for some debugging help from another student, Lars Barkman, but he never edited 
#any code or came up with solutions to my problems by himself. 

#In general, all knowledge of graphics, animations, and overall syntax for code came from https://www.cs.cmu.edu/~112/index.html
#(Look at schedule, then graphics/animations links)

#While making this project, I wrote, thought of, and understood all my code. After finishing 
#the base of the game(the game without castling, en passant, pawn promotion, and AI) 
#I decided to look at some other solutions out there and realized my approach is very common.
#This playlist is the one I stumbled across and found that my approach in moving pieces/legal moves and
#other functionalities are in line with this person's approach:
#https://www.youtube.com/playlist?list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_
#However, I never copied, or really got inspired to change or create code based on the differences in our code
#(ex. he used classes to implement everything, but I already used my model and didn't want to change it)
#I think that the thought process I had of making chess is very organic and exactly like you would think 
#in playing the game IRL so it makes sense that it's a common approach, especially since I don't think
#there are many other ways of approaching the game's rules, 
#but I still want to cite this person because since we had a very similar approach, I would use 
#his videos as a tool AFTER writing my code to see if what I did was still the common approach.
#Once again, I never copied down his code or edited my own project watching him code and I watched only up to the
#base game.


#From https://www.cs.cmu.edu/~112/notes/notes-graphics.html
from cmu_112_graphics import *

###############################################
#Initializing and Representing board on canvas#
###############################################


#Initiliazes all app attributes
def appStarted(app):
    app.margin = 50
    app.rows = 8  #chess board dimensions
    app.cols = 8  #chess board dimensions
    app.boardColors = ['wheat2', 'LightSalmon4', 'IndianRed1']
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


#Returns a dictionary that maps each piece to an image representing that piece
#Got pieces from https://github.com/ornicar/lila/issues/3411
def getPieceImages(app):
    pieceToImage = {}
    gridWidth  = app.width/2 - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    for key in app.pieceValues:
        if key.islower():
            pieceToImage[key] = app.scaleImage(app.loadImage(f'b{key}.png'), 2/9)
        else:
            pieceToImage[key] =  app.scaleImage(app.loadImage(f'{key}.png'), 2/9)
    return pieceToImage


#From https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
#Returns True if (x, y) is inside the grid defined by app.
def pointInGrid(app, x, y):
    return ((app.margin < x < app.width/2 - app.margin) and
            (app.margin < y < app.height - app.margin))


#From https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
#Returns (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
def getCell(app, x, y):
    if (not pointInGrid(app, x, y)):
        return (-1, -1)
    gridWidth  = app.width/2 - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellHeight = gridHeight / app.rows
    cellWidth = gridWidth / app.cols
    row = int((y - app.margin) / cellHeight)
    col = int((x - app.margin) / cellWidth)
    return (row, col)


#From https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
#Returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
def getCellBounds(app, row, col):
    gridWidth  = app.width/2 - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellHeight = gridHeight / app.rows
    cellWidth = gridWidth / app.cols
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight
    return (x0, y0, x1, y1)


#Draws the background and calls all the draw functions
def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'gray23')
    drawBoard(app, canvas)
    drawPieces(app, canvas)
    drawGameOver(app, canvas)
    drawMoves(app, canvas)
    drawNotation(app, canvas)


#Draws the board of the chess set
def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            x0, y0 , x1, y1 = getCellBounds(app, row, col)
            if (row+col)%2 == 0:
                canvas.create_rectangle(x0, y0, x1, y1, fill = app.boardColors[0], width = 0)
            else:
                canvas.create_rectangle(x0, y0, x1, y1, fill = app.boardColors[1], width = 0)

            if (app.startRow, app.startCol) != (-1, -1) and (row, col) == (app.startRow, app.startCol):
                canvas.create_rectangle(x0, y0, x1, y1, fill = app.boardColors[2], width = 0)


#Draws each piece on the board using a 2-D array of values 
def drawPieces(app, canvas):
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            currentPiece = app.board[row][col]
            if not currentPiece.isalpha():
                continue
            currentImage = app.pieceImages[currentPiece]
            x0, y0 , x1, y1 = getCellBounds(app, row, col)
            cx = (x0 + x1)//2
            cy = (y0 + y1)//2
            canvas.create_image(cx, cy, image = ImageTk.PhotoImage(currentImage))


#Draws "Checkmate" when there is a checkmate
def drawGameOver(app, canvas):
    if app.gameOver:
        if app.checkmate:
            canvas.create_text(app.width/4, 25, text = "Checkmate! Press 'r' to restart", fill = 'white', font = 'ITF 16 bold')
        else:
            canvas.create_text(app.width/4, 25, text = "Stalemate! Press 'r' to restart", fill = 'white', font = 'ITF 16 bold')


#Draws all the previous moves
def drawMoves(app, canvas):
    gridWidth = app.height - 2*app.margin
    moveSet = 1
    x = 0
    y = 0
    moveIndex = 0
    moves = 1
    nextLine = 0
    for move in app.pastMoves:
        x += 50
        piece, startRow, startCol, row, col = move
        moveNotation = getMoveNotation(app, piece, row, col)
        if moveIndex%2 == 1:
            canvas.create_text(gridWidth + app.margin + x + nextLine, app.margin + y, text = moveNotation, 
                                fill = 'white', font = 'ITF 16 bold', anchor = 'n')
        else:
            canvas.create_text(gridWidth + app.margin + x + nextLine, app.margin + y, text = f'{moves}: {moveNotation}', 
                                fill = 'white', font = 'ITF 16 bold', anchor = 'n')
        moveIndex += 1
        if x == 100:
            x = 0
        if moveIndex > 0 and moveIndex%2 == 0:
            y += 30
            moves += 1
        if app.margin + y > app.margin + gridWidth:
            y = 0
            nextLine += 120
            


#Draws the coordinates in chess around the chess board
def drawNotation(app, canvas):
    gridWidth  = app.width/2 - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellHeight = gridHeight/app.rows
    cellWidth = gridWidth / app.cols
    for i in range(app.rows):
        canvas.create_text(2*app.margin/3, app.margin + cellWidth/2 + (i*cellHeight), text = 8 - i,
                           fill = 'white', font = 'ITF 16 bold')
    for i in range(app.cols):
        canvas.create_text(app.margin + cellWidth/2 + (i*cellHeight), app.margin + gridHeight + 5,
                           text = chr(ord('a')+i), fill = 'white', font = 'ITF 16 bold', anchor = 'n')







###############################################
#             Logic for moving pieces         #
###############################################


#Dependent on when the mouse is pressed, certain events happen:
#-If it is the first click, you select a piece
#-If it is a second click and is out of bounds or not legal it resets so that 
#you can press another piece as first click
#-If it is a second click and is legal it updates the selected piece's position
def mousePressed(app, event):
    if app.gameOver:
        return
    row, col = getCell(app, event.x, event.y)
    #if this is a first move, then you aren't moving a piece so movingPiece = False
    #otherwise you are moving a piece so movingPiece = True
    if (app.startRow, app.startCol) == (None, None):
        movingPiece = False
    else:
        movingPiece = True

    #out of bounds
    if (row, col) == (-1, -1): 
        (app.startRow, app.startCol) = (None, None)
    
    #you are supposed to move the piece and you pressed the same piece or
    #pressed an illegal place
    elif (movingPiece == True and
        ((row, col) == (app.startRow, app.startCol) or 
        not isLegalMove(app, app.startRow, app.startCol, row, col))):
        (app.startRow, app.startCol) = (None, None)

    #you are supposed to move the piece and it is legal 
    #(this short-circuits if you aren't supposed to move the piece)
    elif movingPiece == True and isLegalMove(app, app.startRow, app.startCol, row, col):
        capturedPiece = app.board[row][col]
        movePiece(app, app.startRow, app.startCol, row, col)

        #we need the current players king to see if moving will cause a check
        if app.whitesMove:
            king = 'K'
        else:
            king = 'k'

        kingRow, kingCol = getPieceRowAndCol(app, king)

        #If a white pawn has reached the end of the board, make it a piece the user chooses
        if app.board[row][col] == 'P' and row == 0 and not isKingCurrentlyInCheck(app, kingRow, kingCol):
            app.board[row][col] = choosePiece(app, '')
            app.whitesMove = not app.whitesMove
            app.pastMoves.append((app.board[row][col], app.startRow, app.startCol, row, col))
            (app.startRow, app.startCol) = (None, None)
            if isInCheckmate(app):
                app.pastMoves.append((app.board[row][col], app.startRow, app.startCol, row, col))
                app.gameOver = True
        #If a white pawn has reached the end of the board, make it a piece the user chooses 
        elif app.board[row][col] == 'p' and row == 7 and not isKingCurrentlyInCheck(app, kingRow, kingCol):
            app.board[row][col] = choosePiece(app, '')
            app.whitesMove = not app.whitesMove
            app.pastMoves.append((app.board[row][col], app.startRow, app.startCol, row, col))
            (app.startRow, app.startCol) = (None, None)
            if isInCheckmate(app):
                app.pastMoves.append((app.board[row][col], app.startRow, app.startCol, row, col))
                app.gameOver = True

        #If you are doing en passant and the king isn't in check, continue with legality and remove pawn you are taking
        elif app.board[row][col] == 'P' and col == app.startCol + 1 and not isKingCurrentlyInCheck(app, kingRow, kingCol) and capturedPiece == '_':
            app.board[row+1][col] = '_'
            app.whitesMove = not app.whitesMove
            app.pastMoves.append((app.board[row][col], app.startRow, app.startCol, row, col))
            (app.startRow, app.startCol) = (None, None)
            if isInCheckmate(app):
                app.pastMoves.append((app.board[row][col], app.startRow, app.startCol, row, col))
                app.gameOver = True
        elif app.board[row][col] == 'P' and col == app.startCol - 1 and not isKingCurrentlyInCheck(app, kingRow, kingCol) and capturedPiece == '_':
            app.board[row+1][col] = '_'
            app.whitesMove = not app.whitesMove
            app.pastMoves.append((app.board[row][col], app.startRow, app.startCol, row, col))
            (app.startRow, app.startCol) = (None, None)
            if isInCheckmate(app):
                app.pastMoves.append((app.board[row][col], app.startRow, app.startCol, row, col))
                app.gameOver = True
        elif app.board[row][col] == 'p' and col == app.startCol + 1 and not isKingCurrentlyInCheck(app, kingRow, kingCol) and capturedPiece == '_':
            app.board[row-1][col] = '_'
            app.whitesMove = not app.whitesMove
            app.pastMoves.append((app.board[row][col], app.startRow, app.startCol, row, col))
            (app.startRow, app.startCol) = (None, None)
            if isInCheckmate(app):
                app.pastMoves.append((app.board[row][col], app.startRow, app.startCol, row, col))
                app.gameOver = True
        elif app.board[row][col] == 'p' and col == app.startCol - 1 and not isKingCurrentlyInCheck(app, kingRow, kingCol)and capturedPiece == '_':
            app.board[row-1][col] = '_'
            app.whitesMove = not app.whitesMove
            app.pastMoves.append((app.board[row][col], app.startRow, app.startCol, row, col))
            (app.startRow, app.startCol) = (None, None)
            if isInCheckmate(app):
                app.pastMoves.append((app.board[row][col], app.startRow, app.startCol, row, col))
                app.gameOver = True


        #If the king is trying to castle and it is in check or will be in check if it castles, reset the move (next 4 if-statements)
        elif app.startRow == 7 and app.startCol == 4 and row == 7 and col == 6 and (isKingCurrentlyInCheck(app, kingRow, kingCol) or isKingCurrentlyInCheck(app, kingRow, kingCol - 1) or isKingCurrentlyInCheck(app, kingRow, kingCol - 2) or 'p' in app.board[6][3:6]):
            app.board[app.startRow][app.startCol] = app.board[row][col]
            app.board[row][col] = capturedPiece
            (app.startRow, app.startCol) = (None, None)
        elif app.startRow == 7 and app.startCol == 4 and row == 7 and col == 2 and (isKingCurrentlyInCheck(app, kingRow, kingCol) or isKingCurrentlyInCheck(app, kingRow, kingCol + 1) or isKingCurrentlyInCheck(app, kingRow, kingCol + 2) or 'p' in app.board[6][1:5]):
            app.board[app.startRow][app.startCol] = app.board[row][col]
            app.board[row][col] = capturedPiece
            (app.startRow, app.startCol) = (None, None)
        elif app.startRow == 0 and app.startCol == 4 and row == 0 and col == 2 and (isKingCurrentlyInCheck(app, kingRow, kingCol) or isKingCurrentlyInCheck(app, kingRow, kingCol - 1) or isKingCurrentlyInCheck(app, kingRow, kingCol - 2) or 'P' in app.board[1][1:5]):
            app.board[app.startRow][app.startCol] = app.board[row][col]
            app.board[row][col] = capturedPiece
            (app.startRow, app.startCol) = (None, None)
        elif app.startRow == 0 and app.startCol == 4 and row == 0 and col == 2 and (isKingCurrentlyInCheck(app, kingRow, kingCol) or isKingCurrentlyInCheck(app, kingRow, kingCol + 1) or isKingCurrentlyInCheck(app, kingRow, kingCol + 2) or 'P' in app.board[1][3:6]):
            app.board[app.startRow][app.startCol] = app.board[row][col]
            app.board[row][col] = capturedPiece
            (app.startRow, app.startCol) = (None, None)
        
        #if the king is in check, revert the move, otherwise move it
        elif isKingCurrentlyInCheck(app, kingRow, kingCol):
            app.board[app.startRow][app.startCol] = app.board[row][col]
            app.board[row][col] = capturedPiece
            (app.startRow, app.startCol) = (None, None)
        #it's legal and move it (check if we can still castle as well)
        else:
            canPlayerCastle(app, row, col)
            isPlayerCastling(app, row, col)
            app.whitesMove = not app.whitesMove
            app.pastMoves.append((app.board[row][col], app.startRow, app.startCol, row, col))
            (app.startRow, app.startCol) = (None, None)
            if isInCheckmate(app):
                app.pastMoves.append((app.board[row][col], app.startRow, app.startCol, row, col))
                app.gameOver = True
    #this is a first click and it is a click on a piece
    elif app.board[row][col] != '_': 
        if (app.whitesMove and app.board[row][col] not in app.blacksPieces or
            not app.whitesMove and app.board[row][col] not in app.whitesPieces):
            (app.startRow, app.startCol) = (row, col)

#Learned user input from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
def choosePiece(app, secondTime):
    piece = app.getUserInput(f'{secondTime} Choose a piece: Queen, Rook, Bishop, or Knight')
    if (piece not in {'Queen', 'Rook', 'Bishop', 'Knight', 'queen', 'rook', 'bishop', 'knight', 'Q', 'R', 'B', 'K', 'q', 'r', 'b', 'k'}):
        app.message = 'Invalid Piece'
        return choosePiece(app, 'Invalid Piece!')
    else:
        if app.whitesMove:
            if piece in {'Queen', 'queen', 'Q', 'q'}:
                return 'Q'
            elif piece in {'Rook', 'rook', 'R', 'r'}:
                return 'R'
            elif piece in {'Bishop', 'bishop', 'B', 'b'}:
                return 'B'
            else:
                return 'N'
        else:
            if piece in {'Queen', 'queen', 'Q', 'q'}:
                return 'q'
            elif piece in {'Rook', 'rook', 'R', 'r'}:
                return 'r'
            elif piece in {'Bishop', 'bishop', 'B', 'b'}:
                return 'b'
            else:
                return 'n'
            

#This returns the row and col of a given piece on the board (meant for king)
def getPieceRowAndCol(app, piece):
    for row in range(app.rows):
        for col in range(app.cols):
            if app.board[row][col] == piece:
                return row, col
    return (-1, -1)


#This will return the chess notation for moving
def getMoveNotation(app, pieceSelected, row, col):
    rowNotation = str(8 - row)
    colNotation = chr(ord('a') + col)
    if pieceSelected == 'P' or pieceSelected == 'p':
        return colNotation + rowNotation
    return pieceSelected.upper() + colNotation + rowNotation


#This will move the piece
def movePiece(app, startRow, startCol, newRow, newCol):
    app.board[newRow][newCol] = app.board[startRow][startCol]
    app.board[startRow][startCol] = '_'


#We should check that the move isn't the king or rook because if it is and it isn't trying to castle,
#then we can't castle that side anymore
def canPlayerCastle(app, newRow, newCol):
    if app.whitesMove:
        if (app.startRow == 7 and app.startCol == 4) and (newRow != 7 or newCol != 6):
            app.whiteCanCastleRightSide = False
        if (app.startRow == 7 and app.startCol == 4) and (newRow != 7 or newCol != 2):
            app.whiteCanCastleLeftSide = False
        elif app.startRow == 7 and app.startCol == 0:
            app.whiteCanCastleLeftSide = False
        elif app.startRow == 7 and app.startCol == 7:
            app.whiteCanCastleRightSide = False
    else:
        if (app.startRow == 0 and app.startCol == 4) and (newRow != 0 or newCol != 6):
            app.blackCanCastleRightSide = False
        if (app.startRow == 0 and app.startCol == 4) and (newRow != 0 or newCol != 2):
            app.blackCanCastleLeftSide = False
        elif app.startRow == 0 and app.startCol == 0:
            app.blackCanCastleLeftSide = False
        elif app.startRow == 0 and app.startCol == 7:
            app.blackCanCastleRightSide = False


#This checks if the move is a castling move and if it is and castling is legal then move the rook
def isPlayerCastling(app, newRow, newCol):
    if app.whitesMove:
        if (app.startRow == 7 and app.startCol == 4) and (newRow == 7 and newCol == 6) and app.whiteCanCastleRightSide:
            print("hi")
            movePiece(app, 7, 7, 7, 5)
        elif (app.startRow == 7 and app.startCol == 4) and (newRow == 7 and newCol == 2) and app.whiteCanCastleLeftSide:
            movePiece(app, 7, 0, 7, 3)
    else:
        if (app.startRow == 0 and app.startCol == 4) and (newRow == 0 and newCol == 6) and app.blackCanCastleRightSide:
            movePiece(app, 0, 7, 0, 5)
        elif (app.startRow == 0 and app.startCol == 4) and (newRow == 0 and newCol == 2) and app.blackCanCastleLeftSide:
            movePiece(app, 0, 0, 0, 3)



###############################################
#                  Legality                   #
###############################################


#This checks if a piece on a row and col is legal to move to a
#selected row and col. Returns True if so, False otherwise
def isLegalMove(app, startRow, startCol, newRow, newCol):
    setOfAllLegalMoves = set()
    pieceSelected = app.board[startRow][startCol]

    #First check if the piece you are trying to move is the same color as current player
    if ((app.whitesMove and pieceSelected not in app.whitesPieces) or
        (not app.whitesMove and pieceSelected not in app.blacksPieces)):
        return False

    #Now check what piece you are moving and set setOfLegalMoves to the return 
    #of getLegal____Moves
    if pieceSelected == 'p' or pieceSelected == 'P':
        setOfAllLegalMoves = getLegalPawnMoves(app, startRow, startCol)
    elif pieceSelected == 'n' or pieceSelected == 'N':
        setOfAllLegalMoves = getLegalKnightMoves(app, startRow, startCol)
    elif pieceSelected == 'b' or pieceSelected == 'B':
        setOfAllLegalMoves = getLegalBishopMoves(app, startRow, startCol)
    elif pieceSelected == 'r' or pieceSelected == 'R':
        setOfAllLegalMoves = getLegalRookMoves(app, startRow, startCol)
    elif pieceSelected == 'q' or pieceSelected == 'Q':
        setOfAllLegalMoves = getLegalQueenMoves(app, startRow, startCol)
    else: 
        setOfAllLegalMoves = getLegalKingMoves(app, startRow, startCol)

    return (newRow, newCol) in setOfAllLegalMoves


#Pawns are implemented by hard-coding the rows in which it can either move two or one, 
#dependent on color. This function uses that idea and implements the rules to which pawns can move
#It returns a list of all the legal moves. The way this is is implemented is that we see who's
#turn it is. If it's white, we check if the pawn hasn't moved yet(a.k.a on row 6). If it is then we
#check for the possiblity of moving up two. If it isn't then we get rid of that possibility. The same
#for black except we check for row 1 for the moving up two
def getLegalPawnMoves(app, startRow, startCol):
    legalMoves = set()
    #This checks for en passant. If the opponent just jumped its pawn up 2 and you have a pawn next to it
    #add taking it is as if it jumped 1 to legal moves.
    if app.whitesMove:
        if startRow == 3:
            if lastMoveIsJumpToTheRightOfPawn(app, startRow, startCol):
                legalMoves.add((startRow-1, startCol+1))
            elif lastMoveIsJumpToTheLeftOfPawn(app, startRow, startCol):
                legalMoves.add((startRow-1, startCol-1))
    else:
        if startRow == 4:
            if lastMoveIsJumpToTheRightOfPawn(app, startRow, startCol):
                legalMoves.add((startRow+1, startCol+1))
            elif lastMoveIsJumpToTheLeftOfPawn(app, startRow, startCol):
                legalMoves.add((startRow+1, startCol-1))

    if app.whitesMove:
        if startRow == 6:
            for drow in (-1, -2):
                for dcol in (-1, 0, 1):
                    #If you are trying to move diagonally and up two
                    if (drow == -2) and (dcol == -1 or dcol == 1):
                        continue

                    newRow = startRow + drow
                    newCol = startCol + dcol

                    if not (0 <= newRow < app.rows and 0 <= newCol < app.cols):
                        continue


                    #If you are trying to take something
                    if dcol == -1 or dcol == 1:
                        #If it is an opponents piece add it to legalMoves
                        if (app.whitesMove and app.board[newRow][newCol] in app.blacksPieces or
                        not app.whitesMove and app.board[newRow][newCol] in app.whitesPieces):
                            legalMoves.add((newRow, newCol))

                    if drow == -2 and app.board[newRow+1][newCol] in app.allPieces:
                        continue

                    #If you are trying to move up and the new spot is a piece 
                    # then continue since it isn't legal
                    #otherwise add the piece to your legal set
                    if dcol == 0:
                        if ((app.whitesMove and app.board[newRow][newCol] in app.allPieces) or
                            (not app.whitesMove and app.board[newRow][newCol] in app.allPieces)):
                            continue
                        else:
                            legalMoves.add((newRow, newCol))
        else:
            for drow in (-1,):
                for dcol in (-1, 0, 1):
                    #If you are trying to move diagonally and up two
                    newRow = startRow + drow
                    newCol = startCol + dcol

                    if not (0 <= newRow < app.rows and 0 <= newCol < app.cols):
                        continue


                    #If you are trying to take something
                    if dcol == -1 or dcol == 1:
                        #If it is an opponents piece add it to legalMoves
                        if (app.whitesMove and app.board[newRow][newCol] in app.blacksPieces or
                        not app.whitesMove and app.board[newRow][newCol] in app.whitesPieces):
                            legalMoves.add((newRow, newCol))

                    #If you are trying to move up and the new spot is a piece 
                    # then continue since it isn't legal
                    #otherwise add the piece to your legal set
                    if dcol == 0:
                        if ((app.whitesMove and app.board[newRow][newCol] in app.allPieces) or
                            (not app.whitesMove and app.board[newRow][newCol] in app.allPieces)):
                            continue
                        else:
                            legalMoves.add((newRow, newCol))
    else:
        if startRow == 1:
            for drow in (1, 2):
                for dcol in (-1, 0, 1):
                    #If you are trying to move diagonally and up two
                    if (drow == 2) and (dcol == -1 or dcol == 1):
                        continue

                    newRow = startRow + drow
                    newCol = startCol + dcol

                    if not (0 <= newRow < app.rows and 0 <= newCol < app.cols):
                        continue


                    #If you are trying to take something
                    if dcol == -1 or dcol == 1:
                        #If it is an opponents piece add it to legalMoves
                        if (app.whitesMove and app.board[newRow][newCol] in app.blacksPieces or
                        not app.whitesMove and app.board[newRow][newCol] in app.whitesPieces):
                            legalMoves.add((newRow, newCol))

                    if drow == 2 and app.board[newRow-1][newCol] in app.allPieces:
                        continue

                    #If you are trying to move up and the new spot is a piece 
                    # then continue since it isn't legal
                    #otherwise add the piece to your legal set
                    if dcol == 0:
                        if ((app.whitesMove and app.board[newRow][newCol] in app.allPieces) or
                            (not app.whitesMove and app.board[newRow][newCol] in app.allPieces)):
                            continue
                        else:
                            legalMoves.add((newRow, newCol))
        else:
            for drow in (1,):
                for dcol in (-1, 0, 1):

                    newRow = startRow + drow
                    newCol = startCol + dcol

                    if not (0 <= newRow < app.rows and 0 <= newCol < app.cols):
                        continue


                    #If you are trying to take something
                    if dcol == -1 or dcol == 1:
                        #If it is an opponents piece add it to legalMoves
                        if ((app.whitesMove and app.board[newRow][newCol] in app.blacksPieces) or
                        (not app.whitesMove and app.board[newRow][newCol] in app.whitesPieces)):
                            legalMoves.add((newRow, newCol))

                    #If you are trying to move up and the new spot is a piece 
                    # then continue since it isn't legal
                    #otherwise add the piece to your legal set
                    if dcol == 0:
                        if ((app.whitesMove and app.board[newRow][newCol] in app.allPieces) or
                            (not app.whitesMove and app.board[newRow][newCol] in app.allPieces)):
                            continue
                        else:
                            legalMoves.add((newRow, newCol))
    return legalMoves


#This goes through all the combinations of possible moves a knight can move to
#If the combination is actually legal it adds it to the set
#At the end we return that set 
def getLegalKnightMoves(app, startRow, startCol):
    legalMoves = set()
    for drow in (-2, -1, 1, 2):
        for dcol in (-2, -1, 1, 2):
            #Isn't a move set of the knight
            if abs(drow) == abs(dcol):
                continue
            newRow = startRow + drow
            newCol = startCol + dcol

            #If it isn't in bounds
            if not (0 <= newRow < app.rows and 0 <= newCol < app.cols):
                continue
            
            #If the new spot is a piece of the same color then continue since it isn't legal
            #otherwise add the piece to your legal set
            if ((app.whitesMove and app.board[newRow][newCol] in app.whitesPieces) or
                (not app.whitesMove and app.board[newRow][newCol] in app.blacksPieces)):
                continue
            else:
                legalMoves.add((newRow, newCol))
    return legalMoves


#This works like getLegalKnightMoves but a bishop can 'slide'
#through the board meaning in every direction, we have to check that direction
#until we hit a piece or the edge of the board
def getLegalBishopMoves(app, startRow, startCol):
    legalMoves = set()
    for drow in (-1, 1):
        for dcol in (-1, 1):
            newRow = startRow + drow
            newCol = startCol + dcol

            #while your new row and new col aren't at an edge or haven't hit a piece
            #of the same color, keep going in that direction
            while((0 <= newRow < app.rows and 0 <= newCol < app.cols) and
                ((app.whitesMove and app.board[newRow][newCol] not in app.whitesPieces) or
                (not app.whitesMove and app.board[newRow][newCol] not in app.blacksPieces))):

                #If you've hit an opponent's piece that means that's your last possible move
                #in this direction, so add it and then get out of this loop and go to the
                #next direction
                if (app.whitesMove and app.board[newRow][newCol] in app.blacksPieces or
                    not app.whitesMove and app.board[newRow][newCol] in app.whitesPieces):
                    legalMoves.add((newRow, newCol))
                    break

                #At this point, it seems that this is an open square so just add it and
                #go to the next square in this direction
                legalMoves.add((newRow, newCol))
                newRow += drow
                newCol += dcol
    return legalMoves


#This works exactly like Bishop Moves except your directions are vertical/horizontal
#instead of diagonal
def getLegalRookMoves(app, startRow, startCol):
    legalMoves = set()
    for drow in (-1, 0, 1):
        for dcol in (-1, 0, 1):
            #Isn't a move set of the knight
            if abs(drow) == abs(dcol):
                continue

            newRow = startRow + drow
            newCol = startCol + dcol

            #while your new row and new col aren't at an edge or haven't hit a piece
            #of the same color, keep going in that direction
            while((0 <= newRow < app.rows and 0 <= newCol < app.cols) and
                ((app.whitesMove and app.board[newRow][newCol] not in app.whitesPieces) or
                (not app.whitesMove and app.board[newRow][newCol] not in app.blacksPieces))):

                #If you've hit an opponent's piece that means that's your last possible move
                #in this direction, so add it and then get out of this loop and go to the
                #next direction
                if (app.whitesMove and app.board[newRow][newCol] in app.blacksPieces or
                    not app.whitesMove and app.board[newRow][newCol] in app.whitesPieces):
                    legalMoves.add((newRow, newCol))
                    break

                #At this point, it seems that this is an open square so just add it and
                #go to the next square in this direction
                legalMoves.add((newRow, newCol))
                newRow += drow
                newCol += dcol
    return legalMoves


#If you think about it, a queen is a bishop+rook when it comes to possible moves
#so all you have to do is return the added sets of those two pieces getLegal
#functions
def getLegalQueenMoves(app, startRow, startCol):
    bishopSet = getLegalBishopMoves(app, startRow, startCol)
    rookSet = getLegalRookMoves(app, startRow, startCol)
    legalMoves = bishopSet|rookSet
    return legalMoves


#This gets all the legal moves of the king by checking the squares around it
#If the square is either clear or an enemy piece it is legal
#DOES NOT CHECK FOR LEGALITY IN TERMS OF CHECK/CHECKMATE
def getLegalKingMoves(app, startRow, startCol):
    legalMoves = set()

    #If the king can castle, add to moves
    if app.whitesMove:
        if startRow == 7 and startCol == 4 and app.whiteCanCastleRightSide:
            if app.board[7][5] == '_' and app.board[7][6] == '_':
                    legalMoves.add((7, 6))
        if startRow == 7 and startCol == 4 and app.whiteCanCastleLeftSide:
            if app.board[7][3] == '_' and app.board[7][2] == '_' and app.board[7][1] == '_':
                    legalMoves.add((7, 2))
    else:
        if startRow == 0 and startCol == 4 and app.blackCanCastleRightSide:
            if app.board[0][5] == '_' and app.board[0][6] == '_':
                legalMoves.add((0, 6))
        if startRow == 0 and startCol == 4 and app.blackCanCastleLeftSide:
            if app.board[0][3] == '_' and app.board[0][2] == '_' and app.board[0][1] == '_':
                legalMoves.add((0, 2))


    for drow in (-1, 0, 1):
        for dcol in (-1, 0, 1):
            #Isn't a move set of the king
            if drow == 0 and dcol == 0:
                continue
            newRow = startRow + drow
            newCol = startCol + dcol

            #If it isn't in bounds
            if not (0 <= newRow < app.rows and 0 <= newCol < app.cols):
                continue
            
            #If the new spot is a piece of the same color then continue since it isn't legal
            #otherwise add the piece to your legal set
            if ((app.whitesMove and app.board[newRow][newCol] in app.whitesPieces) or
                (not app.whitesMove and app.board[newRow][newCol] in app.blacksPieces)):
                continue

            legalMoves.add((newRow, newCol))
    return legalMoves


#To check if the king is in check we need to look at every opponents piece's legal
#moves and if one of those opponents piece's hits the kings location then it is in check!
#However, we run into an infinite loop if we don't make sure we only check this once so we 
#can't put it into legalKingMoves.
#Note: To check opponents move we need to change current player to the opponent
#while we check because isLegal is implemented with the current player
def isKingCurrentlyInCheck(app, kingsRow, kingsCol):
    app.whitesMove = not app.whitesMove
    for row in range(app.rows):
        for col in range(app.cols):
            if ((app.whitesMove and app.board[row][col] not in app.whitesPieces) or
                (not app.whitesMove and app.board[row][col] not in app.blacksPieces)):
                continue
            if isLegalMove(app, row, col, kingsRow, kingsCol):
                app.whitesMove = not app.whitesMove
                return True
    app.whitesMove = not app.whitesMove
    return False


#The way we check for checkmate is simply by going through the list of all the
#current players possible moves and seeing if their king is still in check.
#If for any of the moves it's not in check we return False, otherwise True
def isInCheckmate(app):
    if app.whitesMove:
        king = 'K'
    else:
        king = 'k'

    kingRow, kingCol = getPieceRowAndCol(app, king)
    setOfAllLegalMoves = set()
    setForStalemate = set()

    for row in range(app.rows):
        for col in range(app.cols):

            if (app.whitesMove and app.board[row][col] not in app.whitesPieces or
                not app.whitesMove and app.board[row][col] not in app.blacksPieces):
                continue

            pieceSelected = app.board[row][col]
            if pieceSelected == 'p' or pieceSelected == 'P':
                setOfAllLegalMoves = getLegalPawnMoves(app, row, col)
            elif pieceSelected == 'n' or pieceSelected == 'N':
                setOfAllLegalMoves = getLegalKnightMoves(app, row, col)
            elif pieceSelected == 'b' or pieceSelected == 'B':
                setOfAllLegalMoves = getLegalBishopMoves(app, row, col)
            elif pieceSelected == 'r' or pieceSelected == 'R':
                setOfAllLegalMoves = getLegalRookMoves(app, row, col)
            elif pieceSelected == 'q' or pieceSelected == 'Q':
                setOfAllLegalMoves = getLegalQueenMoves(app, row, col)
            else: 
                setOfAllLegalMoves = getLegalKingMoves(app, row, col)

            for move in setOfAllLegalMoves:
                newRow, newCol = move
                capturedPiece = app.board[newRow][newCol]
                movePiece(app, row, col, newRow, newCol)
                if pieceSelected != king and not isKingCurrentlyInCheck(app, kingRow, kingCol):
                    app.board[row][col] = app.board[newRow][newCol]
                    app.board[newRow][newCol] = capturedPiece
                    return False
                elif pieceSelected == king and not isKingCurrentlyInCheck(app, newRow, newCol):
                    app.board[row][col] = app.board[newRow][newCol]
                    app.board[newRow][newCol] = capturedPiece
                    return False
                app.board[row][col] = app.board[newRow][newCol]
                app.board[newRow][newCol] = capturedPiece
    
    if not isKingCurrentlyInCheck(app, kingRow, kingCol):
        app.stalemate = True
    else:
        app.checkmate = True
    return True


#This is simply to RESET the game
def keyPressed(app, event):
    if event.key == 'r':
        appStarted(app)


#This checks if the last move is the opponents pawn jumping 2 to the right of the current pawn
def lastMoveIsJumpToTheRightOfPawn(app, curRow, curCol):
    pieceSelected, lastMoveStartRow, lastMoveStartCol, lastMoveEndRow, lastMoveEndCol = app.pastMoves[-1]
    if app.whitesMove:
        if lastMoveStartRow == 1 and lastMoveStartCol == curCol + 1 and lastMoveEndRow == 3:
            return True
    else:
        if lastMoveStartRow == 6 and lastMoveStartCol == curCol + 1 and lastMoveEndRow == 4:
            return True
    return False


#This checks if the last move is the opponents pawn jumping 2 to the left of the current pawn
def lastMoveIsJumpToTheLeftOfPawn(app, curRow, curCol):
    pieceSelected, lastMoveStartRow, lastMoveStartCol, lastMoveEndRow, lastMoveEndCol = app.pastMoves[-1]
    if app.whitesMove:
        if lastMoveStartRow == 1 and lastMoveStartCol == curCol - 1 and lastMoveEndRow == 3:
            return True
    else:
        if lastMoveStartRow == 6 and lastMoveStartCol == curCol - 1 and lastMoveEndRow == 4:
            return True
    return False


def main():
    runApp(width=1000, height=500)

if __name__ == '__main__':
    main()


