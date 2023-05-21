from tkinter import *


class TicTackToe:
    def __init__(self):
        self.board = [' '] * 9
        self.player = 'X'
        self.computer = 'O'

        self.root = Tk()
        self.root.title("Лабораторна робота #6 Хрестики-нулики")
        self.root.geometry('455x540')

        self.buttons = []

        for i in range(9):
            self.buttons.append(Button(self.root, text=' ', width=7, height=3, font=('Courier New', 25, 'bold'),
                                       command=lambda I=i: self.move(I), bg='#D4F7EE'))
            self.buttons[i].grid(row=i // 3, column=i % 3)

        self.root.mainloop()

    def move(self, index):
        if self.board[index] == ' ':
            self.board[index] = self.player
            self.buttons[index].config(text=self.player, state=DISABLED)
            if self.check_winner(self.board, self.player):
                self.game_over("Вітаємо, ви виграли!")
            elif self.check_tie(self.board):
                self.game_over("Нічія!")
            else:
                self.computer_move()

    def computer_move(self):
        best_score = -float('inf')
        best_move = None
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = self.computer
                score = self.minimax(self.board, False)
                self.board[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = i
        self.board[best_move] = self.computer
        self.buttons[best_move].config(text=self.computer, state=DISABLED)
        if self.check_winner(self.board, self.computer):
            self.game_over("Комп'ютер виграв!")
        elif self.check_tie(self.board):
            self.game_over("Нічія!")

    def minimax(self, board, maximizing_player):
        if self.check_winner(board, self.computer):
            return 1
        elif self.check_winner(board, self.player):
            return -1
        elif self.check_tie(board):
            return 0
        if maximizing_player:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = self.computer
                    score = self.minimax(board, False)
                    board[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = self.player
                    score = self.minimax(board, True)
                    board[i] = ' '
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self, board, player):
        win = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
        for i in win:
            if board[i[0]] == board[i[1]] == board[i[2]] == player:
                return True
        return False

    def check_tie(self, board):
        return all(x != ' ' for x in board)

    def game_over(self, message):
        for button in self.buttons:
            button.config(state=DISABLED)
        label = Label(self.root, text=message)
        label.grid(row=3, column=0, columnspan=3, pady=10)
        play_again = Button(self.root, text="Грати знову", font=('Courier New', 13), bg='#D4F7EE', width=12, height=2, bd=1, relief='solid',
                            command=self.restart)
        play_again.grid(row=4, column=0, columnspan=3)

    def restart(self):
        self.board = [' '] * 9
        self.player = 'X'
        self.computer = 'O'
        for i in range(9):
            self.buttons[i].config(text=' ', state=NORMAL)
        for widget in self.root.grid_slaves():
            if isinstance(widget, Label):
                widget.destroy()
        label = Label(self.root, text='')
        label.grid(row=3, column=0, columnspan=3)
        play_again = Button(self.root, text="Грати знову!", font=('Courier New', 13), bg='#D4F7EE', width=12, height=2, bd=1, relief='solid',
                            command=self.restart)
        play_again.grid(row=4, column=0, columnspan=3)


game = TicTackToe()
