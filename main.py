class Piece():
    def __init__(self, capabilities = []):
        self.id = 0
        self.color = 0
        self.capabilities = capabilities

    def can_move(self,move_from,move_to):
        pass




class Game:
    def __init__(self):
        self.board = [[None]*8]*8
        self.dead_pieces = []

    def print_board(self):
        for i in self.board:
            print(i)

    def step(self):
        

    def move(self,move_from,move_to):
        if (self.board[move_from[0]][move_from[1]].can_move(move_to)):
            if (self.board[move_to[0][move_to[1]]]!= None):
                self.dead_pieces.append(self.board[move_to[0][move_to[1]]])
            self.board[move_to[0][move_to[1]]] = self.board[move_from[0]][move_from[1]]
            self.board[move_from[0]][move_from[1]] = None
            return True
        else:
            return False

def main():
    game = Game()
    game.print_board()


if __name__=="__main__":
    main()