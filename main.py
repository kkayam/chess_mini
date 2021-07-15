class Piece():
    def __init__(self, move_map = [],move_backwards = False, name = ""):
        self.id = 0
        self.color = 0
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


class Peon(Piece):
    def __init__(self):
        self.move_map = [[0,1,1]]
        self.move_backwards = True
        self.name = "P"
        super().__init__(self.move_map, self.move_backwards,self.name)

class Game:
    def __init__(self):
        self.board = [[0]*8 for i in range(8)]
        self.dead_pieces = []
        self.player_turn = 0
        self.board[0][1] = Peon()

    def print_board(self):
        for y in range(0,8):
            for x in range(0,8):
                print(self.board[x][y], end='')
                print(" ", end='')
            print()

    def move(self,move_from,move_to):
        try:
            if (self.board[move_from[0]][move_from[1]].can_move([x[0]-x[1] for x in zip(move_to, move_from)])):
                    if (self.board[move_to[0]][move_to[1]] != None):
                        self.dead_pieces.append(self.board[move_to[0]][move_to[1]])
                    self.board[move_to[0]][move_to[1]] = self.board[move_from[0]][move_from[1]]
                    self.board[move_from[0]][move_from[1]] = 0
                    return True
            else:
                return False    
        except:
            return False

    def turn(self):
        moved = False
        self.print_board()
        while not moved:
            move = input("Move")
            moved = self.move([int(move[0]),int(move[1])],[int(move[2]),int(move[3])])

def main():
    game = Game()
    done = False
    while not done:
        game.turn()


if __name__=="__main__":
    main()