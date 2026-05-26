import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

/**
 * CODSOFT Internship - Task 4
 * Window Notification using Java (Swing)
 *
 * A desktop notification window with:
 *  - Custom title, message, and icon
 *  - Styled appearance (font, color)
 *  - User interaction (OK / Dismiss)
 *  - Error handling
 *  - Auto-dismiss timer
 */
public class WindowNotification extends JFrame {

    private static final String NOTIFICATION_TITLE = "CodSoft Reminder";
    private static final String NOTIFICATION_MESSAGE = "Don't forget to submit your internship task today!";
    private static final int AUTO_DISMISS_SECONDS = 10;

    private JLabel timerLabel;
    private int countdown;
    private Timer autoTimer;

    public WindowNotification(String title, String message) {
        // Frame setup
        setTitle("Notification");
        setSize(400, 220);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null); // center on screen
        setResizable(false);
        setAlwaysOnTop(true);

        // Colors
        Color bgColor    = new Color(240, 248, 244);
        Color accentColor = new Color(29, 158, 117);
        Color textColor  = new Color(34, 34, 34);

        // Main panel
        JPanel mainPanel = new JPanel();
        mainPanel.setLayout(new BorderLayout(10, 10));
        mainPanel.setBackground(bgColor);
        mainPanel.setBorder(BorderFactory.createEmptyBorder(20, 24, 16, 24));

        // Top: Icon + Title row
        JPanel topPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 8, 0));
        topPanel.setBackground(bgColor);

        JLabel iconLabel = new JLabel("🔔");
        iconLabel.setFont(new Font("Segoe UI Emoji", Font.PLAIN, 28));

        JLabel titleLabel = new JLabel(title);
        titleLabel.setFont(new Font("Segoe UI", Font.BOLD, 18));
        titleLabel.setForeground(accentColor);

        topPanel.add(iconLabel);
        topPanel.add(titleLabel);

        // Center: Message
        JTextArea messageArea = new JTextArea(message);
        messageArea.setFont(new Font("Segoe UI", Font.PLAIN, 14));
        messageArea.setForeground(textColor);
        messageArea.setBackground(bgColor);
        messageArea.setEditable(false);
        messageArea.setLineWrap(true);
        messageArea.setWrapStyleWord(true);
        messageArea.setBorder(null);

        // Bottom: Buttons + Timer
        JPanel bottomPanel = new JPanel(new BorderLayout());
        bottomPanel.setBackground(bgColor);

        timerLabel = new JLabel("Auto-closing in " + AUTO_DISMISS_SECONDS + "s");
        timerLabel.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        timerLabel.setForeground(Color.GRAY);

        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT, 8, 0));
        buttonPanel.setBackground(bgColor);

        JButton dismissBtn = createStyledButton("Dismiss", Color.WHITE, new Color(180, 180, 180));
        JButton okBtn = createStyledButton("  OK  ", Color.WHITE, accentColor);

        dismissBtn.addActionListener(e -> closeNotification());
        okBtn.addActionListener(e -> {
            JOptionPane.showMessageDialog(this, "Thanks for acknowledging!", "Noted", JOptionPane.INFORMATION_MESSAGE);
            closeNotification();
        });

        buttonPanel.add(dismissBtn);
        buttonPanel.add(okBtn);

        bottomPanel.add(timerLabel, BorderLayout.WEST);
        bottomPanel.add(buttonPanel, BorderLayout.EAST);

        // Assemble
        mainPanel.add(topPanel, BorderLayout.NORTH);
        mainPanel.add(messageArea, BorderLayout.CENTER);
        mainPanel.add(bottomPanel, BorderLayout.SOUTH);

        add(mainPanel);

        // Start auto-dismiss countdown
        countdown = AUTO_DISMISS_SECONDS;
        autoTimer = new Timer(1000, e -> {
            countdown--;
            timerLabel.setText("Auto-closing in " + countdown + "s");
            if (countdown <= 0) {
                closeNotification();
            }
        });
        autoTimer.start();

        setVisible(true);
    }

    private JButton createStyledButton(String text, Color fg, Color bg) {
        JButton btn = new JButton(text);
        btn.setFont(new Font("Segoe UI", Font.BOLD, 13));
        btn.setForeground(fg);
        btn.setBackground(bg);
        btn.setFocusPainted(false);
        btn.setBorderPainted(false);
        btn.setCursor(new Cursor(Cursor.HAND_CURSOR));
        btn.setOpaque(true);
        return btn;
    }

    private void closeNotification() {
        if (autoTimer != null) autoTimer.stop();
        dispose();
        System.exit(0);
    }

    public static void main(String[] args) {
        // Set look and feel to system default
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
            System.err.println("Could not set look and feel: " + e.getMessage());
        }

        // Run on Event Dispatch Thread (Swing requirement)
        SwingUtilities.invokeLater(() -> {
            try {
                new WindowNotification(NOTIFICATION_TITLE, NOTIFICATION_MESSAGE);
            } catch (Exception e) {
                System.err.println("Failed to display notification: " + e.getMessage());
                JOptionPane.showMessageDialog(null,
                        "An error occurred: " + e.getMessage(),
                        "Error",
                        JOptionPane.ERROR_MESSAGE);
            }
        });
    }
}
