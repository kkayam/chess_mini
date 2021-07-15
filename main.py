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
    def __init__(self,color):super().__init__([[0,1,1]], False,"P",color)
class King(Piece):
    def __init__(self,color):super().__init__([[0,1],[1]], True,"K",color)
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
        self.board = [["□"]*8 for i in range(8)]
        self.dead_pieces = []
        self.player_turn = 0
        self.board[0] = [Rook(0),Pawn(0),"□","□","□","□",Pawn(1),Rook(1)]
        self.board[1] = [Knight(0),Pawn(0),"□","□","□","□",Pawn(1),Knight(1)]
        self.board[2] = [Bishop(0),Pawn(0),"□","□","□","□",Pawn(1),Bishop(1)]
        self.board[3] = [Queen(0),Pawn(0),"□","□","□","□",Pawn(1),Queen(1)]
        self.board[4] = [King(0),Pawn(0),"□","□","□","□",Pawn(1),King(1)]
        self.board[5] = [Bishop(0),Pawn(0),"□","□","□","□",Pawn(1),Bishop(1)]
        self.board[6] = [Knight(0),Pawn(0),"□","□","□","□",Pawn(1),Knight(1)]
        self.board[7] = [Rook(0),Pawn(0),"□","□","□","□",Pawn(1),Rook(1)]
        self.setup_board = self.board

    def print_board(self):
        for i in self.dead_pieces:
            print(i, end='')
            print(" ", end='')
        print()
        print("  ", end='')
        for i in range(0,8):
            print(i, end='')
            print(" ", end='')
        print()
        for y in range(0,8):
            print(y, end='')
            print(" ", end='')
            for x in range(0,8):
                print(self.board[x][y], end='')
                print(" ", end='')
            print()
    def interference(self,move_from,move_to):
        sign = lambda x: x and (1, -1)[x<0]
        d = [sign(x[0]-x[1]) for x in zip(move_to, move_from)]
        cursor = move_from
        cursor = [sum(x) for x in zip(cursor, d)]
        while cursor != move_to:
            if not self.board[cursor[0]][cursor[1]] == "□":
                return True
            cursor = [sum(x) for x in zip(cursor, d)]
        return False
    def move(self,move_from,move_to):
        # try:01
            if (self.board[move_from[0]][move_from[1]].color == self.player_turn and self.board[move_from[0]][move_from[1]].can_move([x[0]-x[1] for x in zip(move_to, move_from)])):
                if (self.interference(move_from,move_to)):return False
                if (self.board[move_to[0]][move_to[1]] != "□" and self.board[move_to[0]][move_to[1]].color-self.board[move_from[0]][move_from[1]].color==0):return False
                if (self.board[move_to[0]][move_to[1]] != "□"):
                    self.dead_pieces.append(self.board[move_to[0]][move_to[1]])
                self.board[move_to[0]][move_to[1]] = self.board[move_from[0]][move_from[1]]
                self.board[move_from[0]][move_from[1]] = "□"
                return True
            else:
                return False    
        # except:
        #     return False
    def turn(self):
        moved = False
        self.print_board()
        while not moved:
            move = input("Move Player "+str(self.player_turn)+": ")
            moved = self.move([int(move[0]),int(move[1])],[int(move[2]),int(move[3])])
        self.player_turn = 1-self.player_turn

game = Game()
while True:
    game.turn()
