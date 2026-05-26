// ============================================================
// TASK 2: SIMPLE CALCULATOR
// CodSoft C++ Programming Internship
// ============================================================

#include <iostream>
#include <iomanip>   // for setprecision
#include <cmath>     // for sqrt, pow
#include <limits>
using namespace std;

// ── Display Menu ─────────────────────────────────────────────
void showMenu() {
    cout << "\n  ┌─────────────────────────────┐\n";
    cout << "  │        OPERATIONS           │\n";
    cout << "  ├─────────────────────────────┤\n";
    cout << "  │  1. Addition       (+)      │\n";
    cout << "  │  2. Subtraction    (-)      │\n";
    cout << "  │  3. Multiplication (*)      │\n";
    cout << "  │  4. Division       (/)      │\n";
    cout << "  │  5. Modulus        (%)      │\n";
    cout << "  │  6. Power          (^)      │\n";
    cout << "  │  7. Square Root    (√)      │\n";
    cout << "  │  0. Exit                    │\n";
    cout << "  └─────────────────────────────┘\n";
    cout << "  Choose an operation (0-7): ";
}

// ── Get validated double input ────────────────────────────────
double getNumber(const string& prompt) {
    double num;
    while (true) {
        cout << prompt;
        if (cin >> num) return num;
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        cout << "  [!] Invalid input. Please enter a number.\n";
    }
}

// ── Main ─────────────────────────────────────────────────────
int main() {
    cout << "====================================\n";
    cout << "        SIMPLE CALCULATOR           \n";
    cout << "       CodSoft Internship           \n";
    cout << "====================================\n";

    int choice;
    double a, b, result;

    do {
        showMenu();

        // Input validation for menu choice
        if (!(cin >> choice)) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "  [!] Invalid choice.\n";
            continue;
        }

        if (choice == 0) break;

        if (choice < 1 || choice > 7) {
            cout << "  [!] Please choose between 0 and 7.\n";
            continue;
        }

        // Square root only needs one number
        if (choice == 7) {
            a = getNumber("  Enter number: ");
            if (a < 0) {
                cout << "  [!] Cannot compute square root of a negative number.\n";
                continue;
            }
            result = sqrt(a);
            cout << fixed << setprecision(4);
            cout << "\n  √" << a << " = " << result << "\n";
            continue;
        }

        // All other operations need two numbers
        a = getNumber("  Enter first number : ");
        b = getNumber("  Enter second number: ");

        cout << fixed << setprecision(4);

        switch (choice) {
            case 1:
                result = a + b;
                cout << "\n  " << a << " + " << b << " = " << result << "\n";
                break;
            case 2:
                result = a - b;
                cout << "\n  " << a << " - " << b << " = " << result << "\n";
                break;
            case 3:
                result = a * b;
                cout << "\n  " << a << " * " << b << " = " << result << "\n";
                break;
            case 4:
                if (b == 0) {
                    cout << "  [!] Error: Division by zero is not allowed.\n";
                } else {
                    result = a / b;
                    cout << "\n  " << a << " / " << b << " = " << result << "\n";
                }
                break;
            case 5:
                if (b == 0) {
                    cout << "  [!] Error: Modulus by zero is not allowed.\n";
                } else {
                    result = fmod(a, b);
                    cout << "\n  " << a << " % " << b << " = " << result << "\n";
                }
                break;
            case 6:
                result = pow(a, b);
                cout << "\n  " << a << " ^ " << b << " = " << result << "\n";
                break;
        }

    } while (choice != 0);

    cout << "\n  Thank you for using the Calculator!\n";
    cout << "====================================\n";
    return 0;
}
