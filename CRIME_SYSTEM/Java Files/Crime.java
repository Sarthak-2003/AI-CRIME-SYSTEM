import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.*;
import javax.imageio.ImageIO;
import javax.swing.*;
import javax.swing.border.EmptyBorder;

public class Crime extends JFrame {

    private JPanel imagePanel;
    private JScrollPane scrollPane;
    private Timer timer;

    // Correct relative structure
    private File baseDir = new File("..");  // MAJOR-2
    private File imageFolder = new File(baseDir, "Java Files/Images");
    private File pythonFolder = new File(baseDir, "Python_Files");  // ✅ FIXED

    private String[] imageNames = {
            "Barricade.jpg",
            "Fingerprints.jpg",
            "Forensics.jpg",
            "Interrogation.jpg",
            "Map.jpg",
            "Search.jpg",
            "Computers.png",
            "Criminal.png",
            "Detective.png",
            "Finders.png"
    };

    public Crime() {

        setTitle("AI Crime Investigation System");
        setSize(1000, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        // FLAG
        File flagFile = new File(imageFolder, "Indian Flag.png");
        JLabel flagLabel = new JLabel(new ImageIcon(
                new ImageIcon(flagFile.getAbsolutePath())
                        .getImage().getScaledInstance(1000, 150, Image.SCALE_SMOOTH)
        ));
        flagLabel.setHorizontalAlignment(JLabel.CENTER);
        add(flagLabel, BorderLayout.NORTH);

        // IMAGE SCROLLER
        imagePanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 7, 2));
        imagePanel.setBackground(Color.BLACK);

        for (int i = 0; i < 2; i++) {
            for (String name : imageNames) {
                File imgFile = new File(imageFolder, name);
                imagePanel.add(createImageLabel(imgFile));
            }
        }

        scrollPane = new JScrollPane(imagePanel);
        scrollPane.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_NEVER);
        scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_NEVER);
        scrollPane.setBorder(null);
        scrollPane.setPreferredSize(new Dimension(1000, 260));
        add(scrollPane, BorderLayout.CENTER);

        // BUTTON PANEL
        JPanel buttonPanel = new JPanel();
        buttonPanel.setBackground(new Color(30, 30, 30));
        buttonPanel.setBorder(new EmptyBorder(10, 10, 10, 10));

        JButton analysisButton = createStyledButton("Crime Analysis", new Color(173, 216, 230));
        analysisButton.addActionListener(e -> {
            String input = JOptionPane.showInputDialog(this, "Enter Crime Description:");
            if (input != null && !input.trim().isEmpty()) {
                runPythonScript("CRIME.py", input.trim());
            }
        });

        JButton chartButton = createStyledButton("Generate Chart", new Color(144, 238, 144));
        chartButton.addActionListener(e -> runPythonScript("Chart.py"));


        // Add buttons to panel
        buttonPanel.add(analysisButton);
        buttonPanel.add(Box.createHorizontalStrut(20));
        buttonPanel.add(chartButton);
        buttonPanel.add(Box.createHorizontalStrut(20));

        add(buttonPanel, BorderLayout.SOUTH);

        // AUTO SCROLL
        timer = new Timer(10, e -> moveImages());
        timer.start();

        setVisible(true);
    }

    private JLabel createImageLabel(File imageFile) {
        try {
            BufferedImage img = ImageIO.read(imageFile);
            Image scaled = img.getScaledInstance(250, 250, Image.SCALE_SMOOTH);
            return new JLabel(new ImageIcon(scaled));
        } catch (Exception e) {
            System.out.println("Image not found: " + imageFile.getAbsolutePath());
            return new JLabel("Image Error");
        }
    }

    private void moveImages() {
        JScrollBar bar = scrollPane.getHorizontalScrollBar();
        bar.setValue(bar.getValue() + 1);

        if (bar.getValue() >= bar.getMaximum() - scrollPane.getViewport().getWidth()) {
            bar.setValue(0);
        }
    }

    private JButton createStyledButton(String text, Color bg) {
        JButton button = new JButton(text);
        button.setFocusPainted(false);
        button.setFont(new Font("SansSerif", Font.BOLD, 14));
        button.setBackground(bg);
        button.setForeground(Color.BLACK);
        button.setPreferredSize(new Dimension(180, 40));
        button.setCursor(new Cursor(Cursor.HAND_CURSOR));
        return button;
    }

    private void runPythonScript(String scriptName, String... args) 
    {
        try 
        {
            String pythonPath = "C:\\Python314\\python.exe"; // Ensure correct
            File scriptFile = new File(pythonFolder, scriptName);

            if (!scriptFile.exists()) 
            {
                System.out.println("Python script not found: " + scriptFile.getAbsolutePath());
                return;
            }

            ProcessBuilder builder = new ProcessBuilder();
            builder.command().add(pythonPath);
            builder.command().add(scriptFile.getAbsolutePath());

            for (String arg : args) 
            {
                builder.command().add(arg);
            }

            builder.redirectErrorStream(true);

            Process process = builder.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));

            String line;
            while ((line = reader.readLine()) != null) 
            {
                System.out.println(line);
            }

            int exitCode = process.waitFor();
            System.out.println("Python exited with code: " + exitCode);

            if (exitCode == 0) 
            {
                JOptionPane.showMessageDialog(this,
                        "Analysis Completed Successfully!",
                        "Success",
                        JOptionPane.INFORMATION_MESSAGE);
            } 
            else 
            {
                JOptionPane.showMessageDialog(this,
                        "Error occurred. Check console.",
                        "Error",
                        JOptionPane.ERROR_MESSAGE);
            }

        } 
        catch (Exception e) 
        {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(Crime::new);
    }
}
