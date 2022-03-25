import PySimpleGUI as sg
class Piece():
    def __init__(self, move_map = [],move_backwards = False, name = "",color=0):self.id,self.color,self.move_map,self.move_backwards,self.name = 0,color,move_map,move_backwards,name
    def can_move(self,relative_move):
        if (self.color == 1):relative_move = [x*-1 for x in relative_move]
        if (relative_move[1]<0 and not self.move_backwards): return False
        elif (relative_move[1]<0 and self.move_backwards):relative_move[1] *=-1
        if (relative_move[0]<0):relative_move[0] *=-1
        if (len(self.move_map)>relative_move[0] and len(self.move_map[relative_move[0]])>relative_move[1] and self.move_map[relative_move[0]][relative_move[1]]):return True
        return False
    def __str__(self): return self.name
class Pawn(Piece):
    def __init__(self,color):super().__init__([[0,1,1],[0,1]], False,"♟",color)
class King(Piece):
    def __init__(self,color):super().__init__([[0,1],[1,1]], True,"♚",color)
class Queen(Piece):
    def __init__(self,color):super().__init__([[0,1,1,1,1,1,1,1],[1,1],[1,0,1],[1,0,0,1],[1,0,0,0,1],[1,0,0,0,0,1],[1,0,0,0,0,0,1],[1,0,0,0,0,0,0,1]], True,"♛",color)
class Bishop(Piece):
    def __init__(self,color):super().__init__([[0],[0,1],[0,0,1],[0,0,0,1],[0,0,0,0,1],[0,0,0,0,0,1],[0,0,0,0,0,0,1],[0,0,0,0,0,0,0,1]], True,"♝",color)
class Rook(Piece):
    def __init__(self,color):super().__init__([[0,1,1,1,1,1,1,1],[1],[1],[1],[1],[1],[1],[1]], True,"♜",color)
class Knight(Piece):
    def __init__(self,color):super().__init__([[0],[0,0,1],[0,1]], True,"♞",color)
class Game:
    def __init__(self):self.player_turn,self.board = 0,[[Rook(0),Pawn(0),"","","","",Pawn(1),Rook(1)],[Knight(0),Pawn(0),"","","","",Pawn(1),Knight(1)],[Bishop(0),Pawn(0),"","","","",Pawn(1),Bishop(1)],[Queen(0),Pawn(0),"","","","",Pawn(1),Queen(1)],[King(0),Pawn(0),"","","","",Pawn(1),King(1)],[Bishop(0),Pawn(0),"","","","",Pawn(1),Bishop(1)],[Knight(0),Pawn(0),"","","","",Pawn(1),Knight(1)],[Rook(0),Pawn(0),"","","","",Pawn(1),Rook(1)]]
    def print_board(self):
        for (y,x) in [(y,x) for y in range(8) for x in range(8)]:
            if (self.board[x][y]==""):window.Rows[y][x].update(text=str(self.board[x][y]),button_color=["","#"+"9a7b4c"*((x+y)%2)+"c5b8a6"*((x+y+1)%2)])
            else:window.Rows[y][x].update(text=str(self.board[x][y]),button_color=["#"+"FFFFFF"*(1-self.board[x][y].color)+"000000"*self.board[x][y].color,"#"+"9a7b4c"*((x+y)%2)+"c5b8a6"*((x+y+1)%2)])
    def interference(self,move_from,move_to):
        sign = lambda x: x and (1, -1)[x<0]
        d = [sign(x[0]-x[1]) for x in zip(move_to, move_from)]
        cursor = [sum(x) for x in zip(move_from, d)]
        while cursor != move_to:
            if not self.board[cursor[0]][cursor[1]] == "":return True
            cursor = [sum(x) for x in zip(cursor, d)]
        return False 
    def testCheck(self):#TODO Handle checkmate
        king_x,king_y = list(filter(None,[[(j,i) for j,el in enumerate(col) if el.__class__.__name__ == "King" and el.color == self.player_turn] for i, col in enumerate(self.board)]))[0][0]
        for (row,col) in [(y,x) for y in range(8) for x in range(8)]:
                if self.board[row][col]!="" and self.board[row][col].color==1-self.player_turn and self.board[row][col].can_move([x[0]-x[1] for x in zip([king_y,king_x], [row,col])]):
                    if (self.board[row][col].__class__.__name__ == "Pawn"): return True*(abs(col-king_x)==1)
                    elif (self.board[row][col].__class__.__name__ == "Knight" or not self.interference([row,col],[king_y,king_x])):return True
        return False
    def move(self,move_from,move_to): #TODO Castle mechanics #TODO possible line cuts here
        if (self.board[move_from[0]][move_from[1]].color == self.player_turn and self.board[move_from[0]][move_from[1]].can_move([x[0]-x[1] for x in zip(move_to, move_from)])): #Checks right player is playing and that the piece has the capability to move there
            tmp_board = [x[:] for x in self.board] # Save old board before anything
            if (self.board[move_from[0]][move_from[1]].__class__.__name__ != "Knight" and self.interference(move_from,move_to)):return False #If the piece is not knight, checks if something is in the way of the move
            if (self.board[move_to[0]][move_to[1]] != "" and self.board[move_to[0]][move_to[1]].color-self.board[move_from[0]][move_from[1]].color==0):return False #If the destination has a friendly piece, dont move
            elif (self.board[move_from[0]][move_from[1]].__class__.__name__ == "Pawn" and self.board[move_to[0]][move_to[1]] == "" and abs(move_from[0]-move_to[0])==1): return False #If we're a pawn trying to go diagonally to a empty slot, prevent it
            elif (self.board[move_from[0]][move_from[1]].__class__.__name__ == "Pawn" and self.board[move_to[0]][move_to[1]] != "" and abs(move_from[0]-move_to[0])!=1): return False #If we're a pawn going straight and the destination is not empty, do not allow killing
            self.board[move_to[0]][move_to[1]],self.board[move_from[0]][move_from[1]] = self.board[move_from[0]][move_from[1]],"" #Set destination to new piece and remove old piece from old position
            if self.testCheck():
                self.board = tmp_board[:]
                return False
            if (self.board[move_to[0]][move_to[1]].__class__.__name__ == "Pawn" and self.board[move_to[0]][move_to[1]].move_map==[[0,1,1],[0,1]]): self.board[move_to[0]][move_to[1]].move_map=[[0,1],[0,1]] # If we're a pawn with extended moveset and we just moved, remove the extended moveset
            return True # End method successfully
        else:return False # Move failed  
window = sg.Window("MiniChess", [[sg.Button(key=str(col)+str(row),size=(3,1), pad=(0,0),font='Courier 20') for col in range(8)] for row in range(8)], finalize=True,no_titlebar=True,keep_on_top=True)  
game = Game()
while True:
    game.print_board()
    [event1, _],[event2, _] = window.read(),window.read()
    try:
        if game.move([int(event1[0]),int(event1[1])],[int(event2[0]),int(event2[1])]): game.player_turn = 1-game.player_turn
    except:pass