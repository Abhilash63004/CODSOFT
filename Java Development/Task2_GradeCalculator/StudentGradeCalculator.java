import java.util.Scanner;

/**
 * CodSoft Java Internship - Task 2
 * Student Grade Calculator
 *
 * Features:
 * - Input marks for any number of subjects (out of 100)
 * - Calculates total marks and average percentage
 * - Assigns grade based on average (A+, A, B, C, D, F)
 * - Input validation (0–100 range)
 * - Displays a clean result summary
 */
public class StudentGradeCalculator {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("╔══════════════════════════════════════╗");
        System.out.println("║   CODSOFT - GRADE CALCULATOR         ║");
        System.out.println("╚══════════════════════════════════════╝\n");

        // Get student name
        System.out.print("Enter student name: ");
        String studentName = scanner.nextLine().trim();

        // Get number of subjects
        int numSubjects = 0;
        while (numSubjects <= 0) {
            System.out.print("Enter number of subjects: ");
            try {
                numSubjects = Integer.parseInt(scanner.nextLine().trim());
                if (numSubjects <= 0) System.out.println("⚠  Please enter a positive number.");
            } catch (NumberFormatException e) {
                System.out.println("⚠  Invalid input. Please enter a number.");
            }
        }

        // Collect marks
        double[] marks = new double[numSubjects];
        String[] subjectNames = new String[numSubjects];

        System.out.println("\nEnter marks for each subject (out of 100):");
        System.out.println("─────────────────────────────────────────");

        for (int i = 0; i < numSubjects; i++) {
            System.out.print("Subject " + (i + 1) + " name: ");
            subjectNames[i] = scanner.nextLine().trim();
            if (subjectNames[i].isEmpty()) subjectNames[i] = "Subject " + (i + 1);

            boolean validMark = false;
            while (!validMark) {
                System.out.print("Marks for " + subjectNames[i] + ": ");
                try {
                    marks[i] = Double.parseDouble(scanner.nextLine().trim());
                    if (marks[i] < 0 || marks[i] > 100) {
                        System.out.println("⚠  Marks must be between 0 and 100.");
                    } else {
                        validMark = true;
                    }
                } catch (NumberFormatException e) {
                    System.out.println("⚠  Please enter a valid number.");
                }
            }
        }

        // Calculate results
        double totalMarks = 0;
        for (double mark : marks) totalMarks += mark;

        double average = totalMarks / numSubjects;
        String grade = calculateGrade(average);
        String remark = getRemark(grade);

        // Display results
        System.out.println("\n╔══════════════════════════════════════╗");
        System.out.println("║            RESULT CARD               ║");
        System.out.println("╠══════════════════════════════════════╣");
        System.out.printf ("║  Student  : %-26s║%n", studentName);
        System.out.println("╠══════════════════════════════════════╣");
        System.out.println("║  Subject Breakdown:                  ║");

        for (int i = 0; i < numSubjects; i++) {
            String subjectLine = String.format("  %-20s : %5.1f / 100", subjectNames[i], marks[i]);
            System.out.printf("║  %-36s║%n", subjectLine);
        }

        System.out.println("╠══════════════════════════════════════╣");
        System.out.printf ("║  Total Marks  : %-6.1f / %-11d║%n", totalMarks, numSubjects * 100);
        System.out.printf ("║  Average %%    : %-22.2f║%n", average);
        System.out.printf ("║  Grade        : %-22s║%n", grade);
        System.out.printf ("║  Remark       : %-22s║%n", remark);
        System.out.println("╚══════════════════════════════════════╝");

        scanner.close();
    }

    /**
     * Assigns a letter grade based on average percentage.
     */
    static String calculateGrade(double average) {
        if (average >= 90) return "A+";
        else if (average >= 80) return "A";
        else if (average >= 70) return "B";
        else if (average >= 60) return "C";
        else if (average >= 50) return "D";
        else return "F";
    }

    /**
     * Returns a remark based on grade.
     */
    static String getRemark(String grade) {
        return switch (grade) {
            case "A+" -> "Outstanding!";
            case "A"  -> "Excellent!";
            case "B"  -> "Good";
            case "C"  -> "Average";
            case "D"  -> "Below Average";
            default   -> "Fail — Needs Improvement";
        };
    }
}
