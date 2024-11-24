from colorama import Fore
import os
import json

def logo():
    print(Fore.RED +" __   __  ",Fore.WHITE +"          _   _ _____",Fore.GREEN + "     ___")
    print(Fore.RED +" \ \ / /  ",Fore.WHITE +"    /\   | \ | |  __ \\",Fore.GREEN + "   / _ \\")
    print(Fore.RED +"  \ V /   ",Fore.WHITE +"   /  \  |  \| | |  | |",Fore.GREEN + " | | | |")
    print(Fore.RED +"   > <    ",Fore.WHITE +"  / /\ \ | . ` | |  | |",Fore.GREEN + " | | | |")
    print(Fore.RED +"  / . \\   ",Fore.WHITE +" / ____ \| |\  | |__| |",Fore.GREEN + " | |_| |")
    print(Fore.RED +" /_/ \_\\  ",Fore.WHITE +"/_/    \_\_| \_|_____/",Fore.GREEN + "   \___/")
    print(Fore.RESET)

def main_menu():
    # logo()
    print("\n1. Play Game")
    print("2. Change Symbol")
    print("3. Display Games")
    print("4. Quit")

def clear_screen():
    os.system('clear')

def create_board(board_size):
    return [
        [" "] * board_size for _ in range(board_size)
    ]
def print_board(board, winning_positions=[]):
    board_size = len(board)
    print("   " + "   ".join(str(i) for i in range(board_size)))
    print("  " + "----" * board_size)
    for i in range(board_size):
        print(f"{i} |", end="")
        for j in range(board_size):
            if (i,j) in winning_positions:
                print(Fore.BLUE + f" {board[i][j]} " + Fore.RESET + "|", end="")
            else:
                print(f" {board[i][j]} |", end="")
        print("\n  " + "----" * board_size)

def move(board, row, col, player):
    if player == 1:
        board[row][col] = "X"
        player = 0
    else:
        board[row][col] = "O"

def check_winner(board):
    # check row for x and 0
    for i in range(len(board)):
        if all([x == "X" for x in board[i]]):
            return "X", [(i,j) for j in range(len(board))]
        if all([x == "O" for x in board[i]]):
            return "O", [(i,j) for j in range(len(board))]

    # check column
    for i in range(len(board)):
        if all([x == "X" for x in [board[j][i] for j in range(len(board))]]):
            return "X", [(j,i) for j in range(len(board))]
        if all([x == "O" for x in [board[j][i] for j in range(len(board))]]):
            return "O", [(j,i) for j in range(len(board))]

    # check diagonal
    if all([board[i][i] == "X" for i in range(len(board))]):
        return "X", [(i,i) for i in range(len(board))]
    if all([board[i][i] == "O" for i in range(len(board))]):
        return "O", [(i,i) for i in range(len(board))]

    # check other diagonal
    if all([board[i][len(board) - 1 - i] == "X" for i in range(len(board))]):
        return "X", [(i,len(board) - 1 - i) for i in range(len(board))]
    if all([board[i][len(board) - 1 - i] == "O" for i in range(len(board))]):
        return "O", [(i,len(board) - 1 - i) for i in range(len(board))]

    return None, []


def play_game(your_name, player):
    clear_screen()
    opponent_name = input("Enter your opponent's name: ")
    board_size = int(input("Enter the board size: "))
    while board_size % 2 == 0:
        print("Board size must be odd")
        board_size = int(input("Enter the board size: "))

    board = create_board(board_size)
    clear_screen()
    print("Game started")
    print("->", your_name, "VS", opponent_name, "<- \n")
    print_board(board)
    while True:
        row = int(input("Enter row: "))
        col = int(input("Enter column: "))
        try:
            if row < 0 or row >= board_size or col < 0 or col >= board_size:
                print("Invalid move")
        except ValueError:
            print("Invalid input, try again")
        if board[row][col] != " ":
            print("Invalid move")
        else:
            move(board, row, col, player)
            clear_screen()
            print("Game started")
            print("->", your_name, "VS", opponent_name, "<- \n")
            print_board(board)
            winner, winning_positions = check_winner(board)
            clear_screen()
            print("Game started")
            print("->", your_name, "VS", opponent_name, "<- \n")
            print_board(board, winning_positions)
            if winner:
                winner_name = your_name if winner == "X" else opponent_name
                save_game(board, player, opponent_name, winner_name)
                print(f"\nPlayer", Fore.BLUE + f"{winner_name}" + Fore.RESET,  "wins")
                break
        player = 1 if player == 0 else 0
    print("\nPress any key to exit")
    input()

def change_symbol(player):
    clear_screen()
    logo()
    symbol = "X" if player == 1 else "O"
    print(f"\nYou are playing as", Fore.BLUE + f"{symbol}" + Fore.RESET)
    print("Press 'c' key to", Fore.LIGHTMAGENTA_EX + "change symbol" + Fore.RESET)
    print("Press 'b' key to go back to the", Fore.BLUE + "Main Menu" + Fore.RESET)
    choice = input()
    while choice not in ["c", "b"]:
        print("Incorrect key, try again!")
        choice = input()
    if choice == "c":
        player = 0 if player == 1 else 1
        change_symbol(player)
    return player


def save_game(board, player, opponent, winner_name):
    board_data = {
        "player": player,
        "opponent": opponent,
        "winner": winner_name,
        "board": board,
        "board_size": len(board)
    }
    try:
        with open("games.json", "r") as json_file:
            games = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        games = []

    games.append(board_data)

    with open("games.json", "w") as json_file:
        json.dump(games, json_file, indent=2)


def print_all_games(page=1):
    games_per_page = 2
    try:
        with open("games.json", "r") as json_file:
            games = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No games found")
        return

    total_pages = (len(games) + games_per_page - 1) // games_per_page
    start_index = (page - 1) * games_per_page
    end_index = start_index + games_per_page

    for i, game in enumerate(games[start_index:end_index], start_index + 1):
        print(f"\nGame {i}")
        print(f"You VS  {game['opponent']}")
        if game['winner'] == game['opponent']:
            print(f"Winner: {game['opponent']}")
        else:
            print(f"Winner: You")
        winner, winning_positions = check_winner(game['board'])
        print_board(game['board'], winning_positions)
        print(f"Board size: {game['board_size']}")
        print("\n" + "-" * 50)

    print(f"\nPage {page} of {total_pages}")
    print("Press 'n' for next page, 'p' for previous page, 'b' to go back to the Main Menu")
    key = input().lower()
    if key == 'n' and page < total_pages:
        print_all_games(page + 1)
    elif key == 'p' and page > 1:
        print_all_games(page - 1)
    elif key == 'b':
        return
    else:
        print("Invalid key, try again!")
        print_all_games(page)

