from functions import *

def main():
    run = True
    your_name = "Denis"
    player = 1  # player starts as X
    while run:
        clear_screen()
        logo()
        main_menu()

        choice = input()
        while choice not in ["1", "2", "3","4"]:
            clear_screen()
            logo()
            main_menu()
            print(f"\n'{choice}' is not a valid option. Please select a valid option: ", end=" ")
            choice = input()

        if choice == "1":
            play_game(your_name, player)
        elif choice == "2":
            player = change_symbol(player)
        elif choice == "3":
            print_all_games()
        elif choice == "4":
            run = False

if __name__ == "__main__":
    main()