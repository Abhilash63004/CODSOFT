// ============================================================
// TASK 3: TIC-TAC-TOE GAME
// CodSoft C++ Programming Internship
// ============================================================

#include <iostream>
#include <array>
#include <limits>
using namespace std;

// ── Board represented as 3x3 char array ──────────────────────
using Board = array<array<char, 3>, 3>;

// ── Initialize board with position numbers (1-9) ─────────────
void initBoard(Board& board) {
    char num = '1';
    for (auto& row : board)
        for (auto& cell : row)
            cell = num++;
}

// ── Display the board ─────────────────────────────────────────
void displayBoard(const Board& board) {
    cout << "\n";
    cout << "  ┌───┬───┬───┐\n";
    for (int r = 0; r < 3; r++) {
        cout << "  │";
        for (int c = 0; c < 3; c++) {
            char ch = board[r][c];
            // Color X as bold, O normal
            if      (ch == 'X') cout << " X │";
            else if (ch == 'O') cout << " O │";
            else                cout << " " << ch << " │";
        }
        cout << "\n";
        if (r < 2) cout << "  ├───┼───┼───┤\n";
    }
    cout << "  └───┴───┴───┘\n\n";
}

// ── Check if a player has won ─────────────────────────────────
bool checkWin(const Board& board, char player) {
    for (int i = 0; i < 3; i++) {
        // Check rows
        if (board[i][0] == player && board[i][1] == player && board[i][2] == player)
            return true;
        // Check columns
        if (board[0][i] == player && board[1][i] == player && board[2][i] == player)
            return true;
    }
    // Check diagonals
    if (board[0][0] == player && board[1][1] == player && board[2][2] == player)
        return true;
    if (board[0][2] == player && board[1][1] == player && board[2][0] == player)
        return true;
    return false;
}

// ── Check if the board is full (draw) ────────────────────────
bool checkDraw(const Board& board) {
    for (const auto& row : board)
        for (const auto& cell : row)
            if (cell != 'X' && cell != 'O')
                return false;
    return true;
}

// ── Get a valid move from the current player ──────────────────
int getMove(const Board& board, char player) {
    int pos;
    while (true) {
        cout << "  Player " << player << ", enter position (1-9): ";
        if (!(cin >> pos)) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "  [!] Invalid input. Enter a number 1-9.\n";
            continue;
        }
        if (pos < 1 || pos > 9) {
            cout << "  [!] Out of range. Choose between 1 and 9.\n";
            continue;
        }
        // Find the cell
        int r = (pos - 1) / 3;
        int c = (pos - 1) % 3;
        if (board[r][c] == 'X' || board[r][c] == 'O') {
            cout << "  [!] Position " << pos << " is already taken. Choose another.\n";
            continue;
        }
        return pos;
    }
}

// ── Play one full game ────────────────────────────────────────
void playGame() {
    Board board;
    initBoard(board);

    char currentPlayer = 'X';
    int moves = 0;

    cout << "\n  ──── NEW GAME ────\n";
    cout << "  Use the numpad layout to pick your position:\n";
    cout << "    7 | 8 | 9\n    4 | 5 | 6\n    1 | 2 | 3\n";

    while (true) {
        displayBoard(board);

        int pos = getMove(board, currentPlayer);
        int r = (pos - 1) / 3;
        int c = (pos - 1) % 3;
        board[r][c] = currentPlayer;
        moves++;

        if (checkWin(board, currentPlayer)) {
            displayBoard(board);
            cout << "  *** Player " << currentPlayer
                 << " WINS! Congratulations! ***\n";
            return;
        }
        if (checkDraw(board)) {
            displayBoard(board);
            cout << "  *** It's a DRAW! Well played! ***\n";
            return;
        }

        // Switch players
        currentPlayer = (currentPlayer == 'X') ? 'O' : 'X';
    }
}

// ── Main ─────────────────────────────────────────────────────
int main() {
    cout << "====================================\n";
    cout << "        TIC-TAC-TOE GAME            \n";
    cout << "       CodSoft Internship           \n";
    cout << "====================================\n";
    cout << "  Two players: X goes first.\n";

    char again = 'y';
    int winsX = 0, winsO = 0, draws = 0;

    while (again == 'y' || again == 'Y') {
        playGame();

        cout << "\n  Play again? (y/n): ";
        cin >> again;
    }

    cout << "\n  Thanks for playing Tic-Tac-Toe!\n";
    cout << "====================================\n";
    return 0;
}
