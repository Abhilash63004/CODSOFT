import java.util.Random;
import java.util.Scanner;

/**
 * CodSoft Java Internship - Task 1
 * Number Guessing Game
 *
 * Features:
 * - Random number between 1 and 100
 * - Feedback: too high / too low / correct
 * - Max 7 attempts per round
 * - Multiple rounds with play-again option
 * - Score tracking based on rounds won
 */
public class NumberGame {

    static final int MIN = 1;
    static final int MAX = 100;
    static final int MAX_ATTEMPTS = 7;

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Random random = new Random();

        int totalRounds = 0;
        int roundsWon = 0;

        System.out.println("╔══════════════════════════════════╗");
        System.out.println("║      CODSOFT - NUMBER GAME       ║");
        System.out.println("╚══════════════════════════════════╝");
        System.out.println("Guess the number between " + MIN + " and " + MAX + ".");
        System.out.println("You have " + MAX_ATTEMPTS + " attempts per round.\n");

        boolean playAgain = true;

        while (playAgain) {
            totalRounds++;
            int secretNumber = random.nextInt(MAX - MIN + 1) + MIN;
            int attemptsLeft = MAX_ATTEMPTS;
            boolean guessedCorrectly = false;

            System.out.println("─────────────────────────────────");
            System.out.println("Round " + totalRounds + " — I'm thinking of a number...");
            System.out.println("─────────────────────────────────");

            while (attemptsLeft > 0) {
                System.out.print("Enter your guess (" + attemptsLeft + " attempts left): ");

                // Input validation
                int guess;
                try {
                    guess = Integer.parseInt(scanner.nextLine().trim());
                } catch (NumberFormatException e) {
                    System.out.println("⚠  Please enter a valid number.\n");
                    continue;
                }

                if (guess < MIN || guess > MAX) {
                    System.out.println("⚠  Please guess between " + MIN + " and " + MAX + ".\n");
                    continue;
                }

                attemptsLeft--;

                if (guess == secretNumber) {
                    int attemptsUsed = MAX_ATTEMPTS - attemptsLeft;
                    System.out.println("\n✅  Correct! The number was " + secretNumber + ".");
                    System.out.println("    You got it in " + attemptsUsed + " attempt(s)!\n");
                    guessedCorrectly = true;
                    roundsWon++;
                    break;
                } else if (guess < secretNumber) {
                    System.out.println("📈  Too low! Try higher.\n");
                } else {
                    System.out.println("📉  Too high! Try lower.\n");
                }
            }

            if (!guessedCorrectly) {
                System.out.println("\n❌  Out of attempts! The number was: " + secretNumber + "\n");
            }

            // Ask to play again
            System.out.print("Play another round? (yes/no): ");
            String response = scanner.nextLine().trim().toLowerCase();
            playAgain = response.equals("yes") || response.equals("y");
            System.out.println();
        }

        // Final score
        System.out.println("╔══════════════════════════════════╗");
        System.out.println("║           FINAL SCORE            ║");
        System.out.println("╠══════════════════════════════════╣");
        System.out.printf ("║  Rounds Played : %-16d║%n", totalRounds);
        System.out.printf ("║  Rounds Won    : %-16d║%n", roundsWon);
        System.out.printf ("║  Rounds Lost   : %-16d║%n", totalRounds - roundsWon);
        System.out.println("╚══════════════════════════════════╝");
        System.out.println("Thanks for playing! Goodbye.");
        scanner.close();
    }
}
