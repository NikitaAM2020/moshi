import random
from math import exp
from copy import deepcopy

# задаємо початкову температуру для алгоритму відпалу
TEMPERATURE = 1000


def calculate_number_of_threats(n):
    """Обчислення кількості конфріктів"""
    if n < 2:
        return 0
    if n == 2:
        return 1
    return (n - 1) * n / 2


def create_board(n):
    """Створення шахової дошки з ферзем у рядку"""
    chess_board = {}
    temp = list(range(n))
    random.shuffle(temp)
    column = 0

    while len(temp) > 0:
        row = random.choice(temp)
        chess_board[column] = row
        temp.remove(row)
        column += 1

    print(f"Початкова шахова дошка розміром {n}x{n}:")
    print('\n'.join([". "*value + "Q " + ". "*(n-value-1) for value in chess_board.values()]))
    return chess_board


def cost(chess_board):
    """Обчислення конфріктів, що загрожують ферзю"""

    threat = 0
    m_chessboard = {}
    a_chessboard = {}

    for column in chess_board:
        temp_m = column - chess_board[column]
        temp_a = column + chess_board[column]

        if temp_m not in m_chessboard:
            m_chessboard[temp_m] = 1
        else:
            m_chessboard[temp_m] += 1

        if temp_a not in a_chessboard:
            a_chessboard[temp_a] = 1
        else:
            a_chessboard[temp_a] += 1

    for i in m_chessboard:
        threat += calculate_number_of_threats(m_chessboard[i])

    for i in a_chessboard:
        threat += calculate_number_of_threats(a_chessboard[i])

    return threat


def simulated_annealing():
    """Реалізація алгоримту відпалу"""

    solution_found = False
    answer = create_board(N)

    # Для уникнення повторного перерахунку, коли не вдається знайти кращий розв'язок
    cost_answer = cost(answer)

    t = TEMPERATURE
    cooling_rate = 0.99

    while t > 0:
        t *= cooling_rate
        successor = deepcopy(answer)
        while True:
            index_1 = random.randrange(0, N - 1)
            index_2 = random.randrange(0, N - 1)
            if index_1 != index_2:
                break
        # Поміняти місцями обрані ферзі
        successor[index_1], successor[index_2] = successor[index_2], successor[index_1]
        delta = cost(successor) - cost_answer
        if delta < 0 or random.uniform(0, 1) < exp(-delta / t):
            answer = deepcopy(successor)
            cost_answer = cost(answer)
        if cost_answer == 0:
            solution_found = True
            print_chess_board(answer)
            break

    if solution_found is False:
        print("На жаль, розв'язок не вдалося знайти")


def print_chess_board(board):
    """Вивід нової шахової дошки"""

    print(f"\nНова шахова дошка {N}x{N} :")
    print('\n'.join([". "*value + "Q " + ". "*(N-value-1) for value in board.values()]))
    print("\nОновлені позиції ферзів:")
    print('\n'.join(["{} в {} стовпці".format(column+1, row+1) for column, row in board.items()]))

def main():
    global N
    N = int(input("Введіть розмірність шахової дошки N: "))
    simulated_annealing()


if __name__ == "__main__":
    main()
