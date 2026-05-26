# CodSoft Python Internship - Task 4
# Rock Paper Scissors Game
# Features: multi-round play, score tracking, win/loss/tie feedback

import random

CHOICES = ["rock", "paper", "scissors"]

EMOJI = {
    "rock":     "🪨",
    "paper":    "📄",
    "scissors": "✂️ ",
}

# What beats what
BEATS = {
    "rock":     "scissors",
    "paper":    "rock",
    "scissors": "paper",
}


def get_winner(player, computer):
    """Returns 'player', 'computer', or 'tie'."""
    if player == computer:
        return "tie"
    elif BEATS[player] == computer:
        return "player"
    else:
        return "computer"


def print_result(player_choice, computer_choice, winner):
    print(f"\n  You chose    : {EMOJI[player_choice]}  {player_choice.capitalize()}")
    print(f"  Computer chose: {EMOJI[computer_choice]}  {computer_choice.capitalize()}")
    print()
    if winner == "tie":
        print("  🤝  It's a tie!")
    elif winner == "player":
        print("  🎉  You win this round!")
    else:
        print("  💻  Computer wins this round!")


def print_scoreboard(player_score, computer_score, ties):
    total = player_score + computer_score + ties
    print(f"\n  ┌─────────────────────────────────┐")
    print(f"  │  SCOREBOARD  (Round {total})          │")
    print(f"  ├─────────────────────────────────┤")
    print(f"  │  You      : {player_score:<22}│")
    print(f"  │  Computer : {computer_score:<22}│")
    print(f"  │  Ties     : {ties:<22}│")
    print(f"  └─────────────────────────────────┘")


def get_player_choice():
    shortcuts = {"r": "rock", "p": "paper", "s": "scissors"}
    while True:
        raw = input("\n  Your choice — [R]ock / [P]aper / [S]cissors: ").strip().lower()
        if raw in shortcuts:
            return shortcuts[raw]
        if raw in CHOICES:
            return raw
        print("  ⚠  Invalid choice. Type rock, paper, scissors (or r/p/s).")


def main():
    print("╔══════════════════════════════════════╗")
    print("║   CODSOFT - ROCK PAPER SCISSORS      ║")
    print("╚══════════════════════════════════════╝")
    print("  First to 3 wins takes the match!\n")

    player_score   = 0
    computer_score = 0
    ties           = 0
    WIN_TARGET     = 3

    while True:
        player_choice   = get_player_choice()
        computer_choice = random.choice(CHOICES)
        winner          = get_winner(player_choice, computer_choice)

        print_result(player_choice, computer_choice, winner)

        if winner == "player":
            player_score += 1
        elif winner == "computer":
            computer_score += 1
        else:
            ties += 1

        print_scoreboard(player_score, computer_score, ties)

        # Check match winner
        if player_score == WIN_TARGET:
            print("\n  🏆  You won the match! Congratulations!")
            break
        elif computer_score == WIN_TARGET:
            print("\n  💀  Computer won the match. Better luck next time!")
            break

        again = input("\n  Play next round? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            print("\n  Thanks for playing! Goodbye 👋")
            break

    # Final summary
    if player_score > computer_score:
        verdict = "You won overall! 🎉"
    elif computer_score > player_score:
        verdict = "Computer won overall 💻"
    else:
        verdict = "Overall it's a draw! 🤝"

    print(f"\n  {verdict}")
    print(f"  Final — You: {player_score}  |  Computer: {computer_score}  |  Ties: {ties}\n")


if __name__ == "__main__":
    main()
