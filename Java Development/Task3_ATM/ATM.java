import java.util.Scanner;

/**
 * CodSoft Java Internship - Task 3
 * ATM Interface
 *
 * Features:
 * - PIN authentication
 * - Check balance
 * - Deposit money
 * - Withdraw money (with sufficient balance check)
 * - Transaction history
 * - Clean menu-driven interface
 */
public class ATM {

    private BankAccount account;
    private String correctPin;
    private StringBuilder transactionHistory;

    public ATM(BankAccount account, String pin) {
        this.account = account;
        this.correctPin = pin;
        this.transactionHistory = new StringBuilder();
    }

    // ─── ATM Operations ───────────────────────────────────────────

    public void checkBalance() {
        System.out.println("\n  ✅  Account Balance");
        System.out.println("  ─────────────────────────────");
        System.out.printf ("  Account Holder : %s%n", account.getAccountHolder());
        System.out.printf ("  Account Number : %s%n", account.getAccountNumber());
        System.out.printf ("  Balance        : ₹%.2f%n", account.getBalance());
        System.out.println("  ─────────────────────────────\n");
    }

    public void deposit(double amount) {
        if (amount <= 0) {
            System.out.println("\n  ⚠  Deposit amount must be greater than zero.\n");
            return;
        }
        if (account.deposit(amount)) {
            System.out.printf("%n  ✅  ₹%.2f deposited successfully.%n", amount);
            System.out.printf("  New Balance: ₹%.2f%n%n", account.getBalance());
            transactionHistory.append(String.format("DEPOSIT   ₹%.2f | Balance: ₹%.2f%n",
                    amount, account.getBalance()));
        }
    }

    public void withdraw(double amount) {
        if (amount <= 0) {
            System.out.println("\n  ⚠  Withdrawal amount must be greater than zero.\n");
            return;
        }
        if (amount > account.getBalance()) {
            System.out.println("\n  ❌  Insufficient balance.");
            System.out.printf("  Available: ₹%.2f%n%n", account.getBalance());
            return;
        }
        if (account.withdraw(amount)) {
            System.out.printf("%n  ✅  ₹%.2f withdrawn successfully.%n", amount);
            System.out.printf("  Remaining Balance: ₹%.2f%n%n", account.getBalance());
            transactionHistory.append(String.format("WITHDRAW  ₹%.2f | Balance: ₹%.2f%n",
                    amount, account.getBalance()));
        }
    }

    public void showTransactionHistory() {
        System.out.println("\n  ─── Transaction History ───────────────");
        if (transactionHistory.length() == 0) {
            System.out.println("  No transactions yet.");
        } else {
            System.out.print("  " + transactionHistory.toString().replace("\n", "\n  ").trim());
        }
        System.out.println("\n  ───────────────────────────────────────\n");
    }

    // ─── PIN Authentication ───────────────────────────────────────

    private boolean authenticate(Scanner scanner) {
        int tries = 3;
        while (tries > 0) {
            System.out.print("  Enter your 4-digit PIN: ");
            String pin = scanner.nextLine().trim();
            if (pin.equals(correctPin)) return true;
            tries--;
            if (tries > 0)
                System.out.println("  ❌  Wrong PIN. " + tries + " attempt(s) remaining.\n");
        }
        System.out.println("\n  🔒  Card blocked after 3 failed attempts. Goodbye.");
        return false;
    }

    // ─── Main Menu ────────────────────────────────────────────────

    public void run(Scanner scanner) {
        printHeader();
        if (!authenticate(scanner)) return;

        System.out.println("\n  Welcome, " + account.getAccountHolder() + "!");

        boolean running = true;
        while (running) {
            printMenu();
            System.out.print("  Choose option: ");
            String choice = scanner.nextLine().trim();

            switch (choice) {
                case "1" -> checkBalance();
                case "2" -> {
                    System.out.print("\n  Enter deposit amount (₹): ");
                    deposit(parseAmount(scanner));
                }
                case "3" -> {
                    System.out.print("\n  Enter withdrawal amount (₹): ");
                    withdraw(parseAmount(scanner));
                }
                case "4" -> showTransactionHistory();
                case "5" -> {
                    System.out.println("\n  Thank you for using CodSoft ATM. Goodbye! 👋\n");
                    running = false;
                }
                default -> System.out.println("\n  ⚠  Invalid option. Please choose 1–5.\n");
            }
        }
    }

    private double parseAmount(Scanner scanner) {
        try {
            return Double.parseDouble(scanner.nextLine().trim());
        } catch (NumberFormatException e) {
            System.out.println("  ⚠  Invalid amount entered.");
            return -1;
        }
    }

    private void printHeader() {
        System.out.println("╔══════════════════════════════════════╗");
        System.out.println("║        CODSOFT ATM MACHINE           ║");
        System.out.println("╚══════════════════════════════════════╝");
    }

    private void printMenu() {
        System.out.println("┌─────────────────────────────────────┐");
        System.out.println("│  1. Check Balance                   │");
        System.out.println("│  2. Deposit                         │");
        System.out.println("│  3. Withdraw                        │");
        System.out.println("│  4. Transaction History             │");
        System.out.println("│  5. Exit                            │");
        System.out.println("└─────────────────────────────────────┘");
    }

    // ─── Entry Point ─────────────────────────────────────────────

    public static void main(String[] args) {
        // Demo account: PIN is 1234, starting balance ₹10,000
        BankAccount account = new BankAccount("Rahul Sharma", "ACC-98765", 10000.00);
        ATM atm = new ATM(account, "1234");

        Scanner scanner = new Scanner(System.in);
        atm.run(scanner);
        scanner.close();
    }
}
