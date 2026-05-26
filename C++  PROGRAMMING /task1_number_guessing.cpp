// ============================================================
// TASK 1: NUMBER GUESSING GAME
// CodSoft C++ Programming Internship
// ============================================================

#include <iostream>
#include <cstdlib>   // for rand(), srand()
#include <ctime>     // for time()
#include <limits>    // for numeric_limits
using namespace std;

// ── Function: Play one round ─────────────────────────────────
void playGame(int minVal, int maxVal) {
    // Generate a random number in [minVal, maxVal]
    int secret = minVal + rand() % (maxVal - minVal + 1);
    int guess   = 0;
    int attempts = 0;

    cout << "\n  A number has been chosen between "
         << minVal << " and " << maxVal << ".\n";
    cout << "  Can you guess it?\n\n";

    while (true) {
        cout << "  Enter your guess: ";

        // Input validation
        if (!(cin >> guess)) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "  [!] Invalid input. Please enter an integer.\n";
            continue;
        }

        attempts++;

        if (guess < minVal || guess > maxVal) {
            cout << "  [!] Please guess within the range ("
                 << minVal << " - " << maxVal << ").\n";
        } else if (guess < secret) {
            cout << "  Too LOW!  Try higher.\n";
        } else if (guess > secret) {
            cout << "  Too HIGH! Try lower.\n";
        } else {
            cout << "\n  *** Correct! The number was " << secret
                 << ". You got it in " << attempts
                 << (attempts == 1 ? " attempt" : " attempts")
                 << "! ***\n";
            break;
        }
    }
}

// ── Main ─────────────────────────────────────────────────────
int main() {
    srand(static_cast<unsigned int>(time(nullptr)));  // seed RNG

    cout << "====================================\n";
    cout << "      NUMBER GUESSING GAME          \n";
    cout << "         CodSoft Internship         \n";
    cout << "====================================\n";

    char playAgain = 'y';

    while (playAgain == 'y' || playAgain == 'Y') {
        // Let user pick difficulty
        cout << "\n  Choose difficulty:\n";
        cout << "    1. Easy   (1 - 50)\n";
        cout << "    2. Medium (1 - 100)\n";
        cout << "    3. Hard   (1 - 500)\n";
        cout << "  Your choice (1/2/3): ";

        int choice;
        cin >> choice;

        int minVal = 1, maxVal = 100;
        if      (choice == 1) { minVal = 1; maxVal = 50;  }
        else if (choice == 2) { minVal = 1; maxVal = 100; }
        else if (choice == 3) { minVal = 1; maxVal = 500; }
        else {
            cout << "  Invalid choice, defaulting to Medium.\n";
        }

        playGame(minVal, maxVal);

        cout << "\n  Play again? (y/n): ";
        cin >> playAgain;
    }

    cout << "\n  Thanks for playing! Goodbye.\n";
    cout << "====================================\n";
    return 0;
}
