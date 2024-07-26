import sys

class MisereNim:
    def __init__(self, red, blue, first_player='comp'):
        self.red = red
        self.blue = blue
        self.turn = first_player

    def gamefinished(self):
        return self.red == 0 or self.blue == 0

    def evaluatinggame(self):
        if self.red == 0 or self.blue == 0:
            return 1 if self.turn == 'player' else -1
        return 0

    def available_moves(self):
        moves = []
        if self.blue >= 1:
            moves.append((0, -1))
        if self.red >= 1:
            moves.append((-1, 0))
        if self.blue >= 2:
            moves.append((0, -2))
        if self.red >= 2:
            moves.append((-2, 0))
        return moves

    def applyingmovement(self, move):
        self.red += move[0]
        self.blue += move[1]

    def backwardmove(self, move):
        self.red -= move[0]
        self.blue -= move[1]

    def alphabetapruning(self, depth, alpha, beta, playermaximize):
        score = self.evaluatinggame()
        if score != 0 or depth == 0:
            return score

        if playermaximize:
            max_eval = -float('inf')
            for move in self.available_moves():
                self.applyingmovement(move)
                evaluation = self.alphabetapruning(depth - 1, alpha, beta, False)
                self.backwardmove(move)
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            minevaluate = float('inf')
            for move in self.available_moves():
                self.applyingmovement(move)
                evaluation = self.alphabetapruning(depth - 1, alpha, beta, True)
                self.backwardmove(move)
                minevaluate = min(minevaluate, evaluation)
                beta = min(beta, minevaluate)
                if beta <= alpha:
                    break
            return minevaluate

    def optimal_move(self, depth=4):
        best_score = -float('inf')
        best_move = None
        for move in self.available_moves():
            self.applyingmovement(move)
            score = self.alphabetapruning(depth - 1, -float('inf'), float('inf'), False)
            self.backwardmove(move)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def startgame(self):
        while not self.gamefinished():
            if self.turn == 'comp':
                move = self.optimal_move()
                print(f"comp move: {move}")
                self.applyingmovement(move)
                self.turn = 'player'
            else:
                print(f"Red: {self.red}, Blue: {self.blue}")
                redmarbel = int(input("Red marbles to take (1 or 2): "))
                bluemarbel = int(input("Blue marbles to take (1 or 2): "))
                move = (-redmarbel, -bluemarbel)
                self.applyingmovement(move)
                self.turn = 'comp'

        if self.red == 0 or self.blue == 0:
            print(f"{self.turn} wins!")

# Command-line parsing
if len(sys.argv) != 5:
    print('''Use this prompt for run the game: python alphabeta_game.py <num of red marbel> <num of blue marbel> <version> <player>
              And Also make sure that this code is located one the user. ''')
    sys.exit(1)

num_red = int(sys.argv[1])
num_blue = int(sys.argv[2])
version = sys.argv[3]
first_player = sys.argv[4]

if version == 'misere':
    game = MisereNim(num_red, num_blue, first_player)
    game.startgame()
else:
    print("Invalid version. Use 'misere'.")
    sys.exit(1)
