import sys

class StandardNim:
    def __init__(self, red, blue, first='comp'):
        self.red = red
        self.blue = blue
        self.turn = first

    
    def reversingmovement(self, move):
        self.red -= move[0]
        self.blue -= move[1]


    def evaluatinggame(self):
        if self.red == 0 or self.blue == 0:
            return -1 if self.turn == 'player' else 1
        return 0
    
    def gamefinished(self):
        return self.red == 0 or self.blue == 0
    
    def applyingmovement(self, move):
        self.red += move[0]
        self.blue += move[1]

    def available_moves(self):
        moves = []
        if self.red >= 2:
            moves.append((-2, 0))
        if self.blue >= 2:
            moves.append((0, -2))
        if self.red >= 1:
            moves.append((-1, 0))
        if self.blue >= 1:
            moves.append((0, -1))
        return moves

    def bestmove(self, depth=4):
        goodscore = -float('inf')
        bestmove = None
        for move in self.available_moves():
            self.applyingmovement(move)
            score = self.minmaxalgo(depth - 1, False)
            self.reversingmovement(move)
            if score > goodscore:
                goodscore = score
                bestmove = move
        return bestmove

    def minmaxalgo(self, depth, playermaximize):
        score = self.evaluatinggame()
        if score != 0 or depth == 0:
            return score

        if playermaximize:
            maxevaluate = -float('inf')
            for move in self.available_moves():
                self.applyingmovement(move)
                evaluation = self.minmaxalgo(depth - 1, False)
                self.reversingmovement(move)
                maxevaluate = max(maxevaluate, evaluation)
            return maxevaluate
        else:
            minevaluate = float('inf')
            for move in self.available_moves():
                self.applyingmovement(move)
                evaluation = self.minmaxalgo(depth - 1, True)
                self.reversingmovement(move)
                minevaluate = min(minevaluate, evaluation)
            return minevaluate

    

    def playinggame(self):
        while not self.gamefinished():
            if self.turn == 'comp':
                move = self.bestmove()
                print(f"Computer move: {move}")
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


if len(sys.argv) != 5:
    print('''Use this prompt for run the game: python MinMax_game.py <num of red marbel> <num of blue marbel> <version> <first-player>
              And Also make sure that this code is located one the user. ''')
    sys.exit(1)

num_red = int(sys.argv[1])
num_blue = int(sys.argv[2])
version = sys.argv[3]
firstplayer = sys.argv[4]

if version == 'standard':
    game = StandardNim(num_red, num_blue, firstplayer)
    game.playinggame()
else:
    print("Invalid version. Use 'standard'")
    sys.exit(1)




    
