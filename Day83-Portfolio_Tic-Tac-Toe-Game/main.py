# Day83-Professional Portfolio Project 2 : Tic Tae Toe Game
from colorama import Fore, Back, Style, init

init()

class TicTacToe:
    def __init__(self, size=3):
        self.board = [[m * size + n + 1 for n in range(size)] for m in range(size)]
        self.game_board = [[' ' for _ in range(size)] for _ in range(size)]
        self.players = {'O': 1, 'X': -1, 1: 'O', -1: 'X'}
        self.rows, self.cols = [0] * size, [0] * size
        self.diag, self.anti_diag = 0, 0
        self.N = size

    def boardSize(self):
        size = 0

        while True:
            try:
                size = int(input("What size game of Tic Tac Toe? (2 - 9) : "))
            except:
                print("Invalid Input! Enter the number only (2 - 9).")
                continue

            if 2 <= size <= 9:
                break
            else:
                print("Out of range!! Enter the number only (2 - 9).")

        self.N = size
        return size


    def displayBoard(self):
        print('\n........................................\n')

        for i in range(self.N):
            for j in range(self.N):
                if self.board[i][j] < 10:
                    space = '  '
                else:
                    space = ' '

                if j == self.N - 1:
                    print(f'{space}{self.board[i][j]}', end='      ')
                else:
                    print(f'{space}{self.board[i][j]} |', end='')

            print('==>>>', end='     ')

            for j in range(self.N):
                # with colorama package
                if self.game_board[i][j] == 'X':
                    colored_mark = Fore.GREEN + self.game_board[i][j] + Style.RESET_ALL
                else:
                    colored_mark = Fore.MAGENTA + self.game_board[i][j] + Style.RESET_ALL

                if j == self.N - 1:
                    print(f' {colored_mark}', end='\n')
                else:
                    print(f' {colored_mark} |', end='')

                ## w/o colorama package
                # if j == self.N - 1:
                #     print(f' {self.game_board[i][j]}', end='\n')
                # else:
                #     print(f' {self.game_board[i][j]} |', end='')

            if i < self.N - 1:
                print('----' * self.N + '-' * (self.N - 1), end='     ')
                print('==>>>', end='     ')
                print('---' * self.N + '-' * (self.N - 1), end='\n')

        print('\n........................................\n')

    def gameStart(self):
        self.N = self.boardSize()
        self.clearBoard(self.N)
        mark = self.choosePlayer()
        self.displayBoard()

        return mark


    def choosePlayer(self):
        mark = ''
        while mark not in ('O', 'X'):
            mark = input("\nSelect a player. O or X : ").upper()

        return mark

    def isBlank(self, position):
        x, y = self.getPos(position)

        return self.game_board[x][y] == ' '


    def getPos(self, position):
        x = (position - 1) // self.N
        y = (position - 1) % self.N

        return (x, y)

    def playGame(self, mark):
        while True:
            position = input(f"Player {mark}\n\tPick a number : ")

            try:
                position = int(position)
            except:
                print("\t==> Wrong Input. Enter the number only!\n")
                continue

            if position <= 0 or position > self.N * self.N:
                print(f"\t==> {position} is out of range. Enter the other number!\n")
                continue

            if self.isBlank(position):
                break
            else:
                print(f"\t==> {position} was already occupied. Enter the other number!\n")

        x, y = self.getPos(position)
        player = self.players[mark]

        self.game_board[x][y] = mark
        self.rows[x] += player
        self.cols[y] += player

        if x == y:
            self.diag += player

        if x + y == self.N - 1:
            self.anti_diag += player

        self.displayBoard()

        if self.winGame(player, x, y):
            return False

        if self.isDraw():
            print("\n=== Draw!! ===\n")
            return False

        return True


    def winGame(self, player, x, y):
        if any(line == self.N * player for line in (self.rows[x], self.cols[y], self.diag, self.anti_diag)):
            print('*************************')
            print(f' Player {self.players[player]} Wins!!')
            print('*************************\n\n')
            return True

        return False

    def isDraw(self):
        return not any([' ' in line for line in self.game_board])


    def clearBoard(self, size):
        self.board = [[m * size + n + 1 for n in range(size)] for m in range(size)]
        self.game_board = [[' ' for _ in range(size)] for _ in range(size)]
        self.rows, self.cols = [0] * size, [0] * size
        self.diag, self.anti_diag = 0, 0


print("#####################################")
print("   T i c   T a c   T o e  G a m e")
print("#####################################")

game = TicTacToe()
game_on = True

mark = game.gameStart()

while game_on:
    # game.playGame(mark)

    if not game.playGame(mark):
        again = input("Replay game? Y or N : ").upper()

        if again == '' or again[0].upper() == 'Y':
            mark = game.gameStart()
        else:
            game_on = False
    else:
        mark = 'O' if mark == 'X' else 'X'