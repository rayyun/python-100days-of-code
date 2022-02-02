# Day82-Professional Portfolio Project 2 : Tic Tae Toe Game

class TicTacToe:
    def __init__(self):
        self.board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.game_board = [[' ' for _ in range(3)] for _ in range(3)]
        self.pos = {1: (0,0), 2: (0,1), 3: (0,2), 4: (1,0), 5: (1,1), 6: (1,2), 7: (2,0), 8: (2,1), 9: (2,2)}
        self.players = {'O': 1, 'X': -1, 1: 'O', -1: 'X'}
        self.rows, self.cols = [0] * 3, [0] * 3
        self.diag, self.anti_diag = 0, 0
        self.N = 3

    def displayBoard(self):
        print('\n........................................\n')

        for i in range(self.N):
            print(f' {self.board[i][0]} | {self.board[i][1]} | {self.board[i][2]} ', end='\t\t')
            print('==>>>', end='\t\t')
            print(f' {self.game_board[i][0]} | {self.game_board[i][1]} | {self.game_board[i][2]} ', end='\n')
            if i < self.N - 1:
                print('-----------', end='\t\t')
                print('==>>>', end='\t\t')
                print('-----------', end='\n')

        print('\n........................................\n')

    def gameStart(self):
        self.clearBoard()
        mark = self.choosePlayer()
        self.displayBoard()

        return mark


    def choosePlayer(self):
        mark = ''
        while mark not in ('O', 'X'):
            mark = input("\nSelect a player. O or X : ").upper()

        return mark

    def isBlank(self, position):
        if position == 0:
            return False

        x, y = self.getPos(position)

        return self.game_board[x][y] == ' '


    def getPos(self, position):
        x, y = self.pos[position]

        return (x, y)

    def playGame(self, mark):
        while True:
            position = input(f"Player {mark}\n\tPick a number : ")

            try:
                position = int(position)
            except:
                print("\t==> Wrong Input. Enter the number only!\n")
                continue

            if self.isBlank(position):
                break
            else:
                print(f"\t==> {position} was already occupied. Enter the other number!\n")

        x, y = self.getPos(position)
        player = self.players[mark]

        # if self.game_board[x][y] == ' ':
        self.game_board[x][y] = mark
        self.rows[x] += player
        self.cols[y] += player

        if x == y:
            self.diag += player

        if x + y == self.N - 1:
            self.anti_diag += player

        self.displayBoard()

        if self.winGame(player, x, y):
            # print(f"Player {mark} wins!!!")
            return False

        if self.isDraw():
            print("\n=== Draw!! ===\n")
            return False

            # self.playAgain()

        return True
        # else:
        #     print("Already occupied!! Choose another number!")
        #     # return False


    def winGame(self, player, x, y):
        if any(line == self.N * player for line in (self.rows[x], self.cols[y], self.diag, self.anti_diag)):
            print('*************************')
            print(f' Player {self.players[player]} Wins!!')
            print('*************************\n\n')
            return True

        return False

    def isDraw(self):
        # print("draw - ", not any([' ' in line for line in self.game_board]))
        return not any([' ' in line for line in self.game_board])


    def clearBoard(self):
        self.game_board = [[' ' for _ in range(3)] for _ in range(3)]
        self.rows, self.cols = [0] * 3, [0] * 3
        self.diag, self.anti_diag = 0, 0


game = TicTacToe()

print("#####################################")
print("   T i c   T a c   T o e  G a m e")
print("#####################################")

game_on = True

mark = game.gameStart()

while game_on:
    # game.playGame(mark)

    if not game.playGame(mark):
        again = input("Replay game? Y or N : ").upper()

        if again[0].upper() == 'Y':
            mark = game.gameStart()
        else:
            game_on = False
    else:
        mark = 'O' if mark == 'X' else 'X'