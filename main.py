import PySimpleGUI as sg

layout = [[sg.Button(key=str(col)+str(row),size=(3,1), pad=(0,0)) for col in range(8)] for row in range(8)]
window = sg.Window("MiniChess", layout, finalize=True,no_titlebar=True, grab_anywhere=True,return_keyboard_events=True)

class Piece():
    def __init__(self, move_map = [],move_backwards = False, name = "",color=0):
        self.id = 0
        self.color = color
        self.move_map = move_map
        self.move_backwards = move_backwards
        self.name = name
    def can_move(self,relative_move):
        if (self.color == 1):
            relative_move = [x*-1 for x in relative_move]
        if (relative_move[1]<0 and not self.move_backwards): 
            return False
        elif (relative_move[1]<0 and self.move_backwards):
            relative_move[1] *=-1
        if (relative_move[0]<0):
            relative_move[0] *=-1
        if (self.move_map[relative_move[0]][relative_move[1]]):
            return True
        return False
    def __str__(self):
        return self.name
class Pawn(Piece):
    def __init__(self,color):super().__init__([[0,1,1],[0,1]], False,"P",color)
class King(Piece):
    def __init__(self,color):super().__init__([[0,1],[1,1]], True,"K",color)
class Queen(Piece):
    def __init__(self,color):super().__init__([[0,1,1,1,1,1,1,1],[1,1],[1,0,1],[1,0,0,1],[1,0,0,0,1],[1,0,0,0,0,1],[1,0,0,0,0,0,1],[1,0,0,0,0,0,0,1]], True,"Q",color)
class Bishop(Piece):
    def __init__(self,color):super().__init__([[0],[0,1],[0,0,1],[0,0,0,1],[0,0,0,0,1],[0,0,0,0,0,1],[0,0,0,0,0,0,1],[0,0,0,0,0,0,0,1]], True,"B",color)
class Rook(Piece):
    def __init__(self,color):super().__init__([[0,1,1,1,1,1,1,1],[1],[1],[1],[1],[1],[1],[1]], True,"R",color)
class Knight(Piece):
    def __init__(self,color):super().__init__([[0],[0,0,1],[0,1]], True,"T",color)

class Game:
    def __init__(self):
        self.board = [[""]*8 for i in range(8)]
        self.dead_pieces = []
        self.player_turn = 0
        self.board[0] = [Rook(0),Pawn(0),"","","","",Pawn(1),Rook(1)]
        self.board[1] = [Knight(0),Pawn(0),"","","","",Pawn(1),Knight(1)]
        self.board[2] = [Bishop(0),Pawn(0),"","","","",Pawn(1),Bishop(1)]
        self.board[3] = [Queen(0),Pawn(0),"","","","",Pawn(1),Queen(1)]
        self.board[4] = [King(0),Pawn(0),"","","","",Pawn(1),King(1)]
        self.board[5] = [Bishop(0),Pawn(0),"","","","",Pawn(1),Bishop(1)]
        self.board[6] = [Knight(0),Pawn(0),"","","","",Pawn(1),Knight(1)]
        self.board[7] = [Rook(0),Pawn(0),"","","","",Pawn(1),Rook(1)]
        self.setup_board = self.board

    def print_board(self):
        for y in range(0,8):
            for x in range(0,8):
                if (self.board[x][y]==""):layout[y][x].update(text=str(self.board[x][y]),button_color=[0,"#9a7b4c"])
                else:layout[y][x].update(text=str(self.board[x][y]),button_color=[self.board[x][y].color,"#9a7b4c"])
    def interference(self,move_from,move_to):
        sign = lambda x: x and (1, -1)[x<0]
        d = [sign(x[0]-x[1]) for x in zip(move_to, move_from)] #figuring out direction of movement
        cursor = [sum(x) for x in zip(move_from, d)]
        while cursor != move_to:
            if not self.board[cursor[0]][cursor[1]] == "":
                return True
            cursor = [sum(x) for x in zip(cursor, d)]
        return False
    def move(self,move_from,move_to):
        if (self.board[move_from[0]][move_from[1]].color == self.player_turn and self.board[move_from[0]][move_from[1]].can_move([x[0]-x[1] for x in zip(move_to, move_from)])):
            if (self.board[move_from[0]][move_from[1]].__class__.__name__ != "Knight" and self.interference(move_from,move_to)):return False
            if (self.board[move_to[0]][move_to[1]] != "" and self.board[move_to[0]][move_to[1]].color-self.board[move_from[0]][move_from[1]].color==0):return False
            if (self.board[move_to[0]][move_to[1]] != "" and self.board[move_from[0]][move_from[1]].__class__.__name__ == "Pawn" and abs(move_from[0]-move_to[0])==1 ):self.dead_pieces.append(self.board[move_to[0]][move_to[1]])
            elif (self.board[move_from[0]][move_from[1]].__class__.__name__ == "Pawn" and self.board[move_to[0]][move_to[1]] == "" and abs(move_from[0]-move_to[0])==1): return False
            elif (self.board[move_from[0]][move_from[1]].__class__.__name__ == "Pawn" and self.board[move_to[0]][move_to[1]] != "" and abs(move_from[0]-move_to[0])!=1): return False
            elif (self.board[move_to[0]][move_to[1]] != ""):self.dead_pieces.append(self.board[move_to[0]][move_to[1]])
            self.board[move_to[0]][move_to[1]] = self.board[move_from[0]][move_from[1]]
            self.board[move_from[0]][move_from[1]] = ""
            if (self.board[move_to[0]][move_to[1]].__class__.__name__ == "Pawn" and self.board[move_to[0]][move_to[1]].move_map==[[0,1,1],[0,1]]): self.board[move_to[0]][move_to[1]].move_map=[[0,1],[0,1]]
            return True
        else:
            return False    
        
game = Game()
while True:
    game.print_board()
    event1, _ = window.read()
    event2, _ = window.read()
    if event2 == 'Escape:27' and event1 == 'Escape:27': break
    try:
        moved = game.move([int(event1[0]),int(event1[1])],[int(event2[0]),int(event2[1])])
    except:
        moved = False
    if moved: game.player_turn = 1-game.player_turn

window.close()