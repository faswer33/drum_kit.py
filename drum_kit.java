// drum_kit.java — Java версия

import java.util.*;
import java.util.concurrent.*;

public class drum_kit {
    private int bpm;
    private double beatLen;
    private boolean running;
    private List<Map<String, Integer>> pattern;
    private Map<String, Drum> drums;

    static class Drum {
        String name, key, symbol;
        Drum(String name, String key, String symbol) {
            this.name = name; this.key = key; this.symbol = symbol;
        }
    }

    public drum_kit(int bpm) {
        this.bpm = bpm;
        this.beatLen = 60.0 / bpm;
        this.drums = new LinkedHashMap<>();
        drums.put("bd", new Drum("Бас", "1", "█"));
        drums.put("sd", new Drum("Малый", "2", "▓"));
        drums.put("hh", new Drum("Хай-хэт", "3", "▒"));
        drums.put("t1", new Drum("Том 1", "4", "░"));
        drums.put("t2", new Drum("Том 2", "5", "░"));
        drums.put("rd", new Drum("Райд", "6", "●"));
        drums.put("cr", new Drum("Крэш", "7", "◆"));
    }

    private List<Map<String, Integer>> generateRockPattern(String style) {
        List<Map<String, Integer>> pattern = new ArrayList<>();
        if (style.equals("shuffle")) {
            for (int i = 0; i < 16; i++) {
                Map<String, Integer> beat = new HashMap<>();
                beat.put("bd", 0); beat.put("sd", 0); beat.put("hh", 0);
                beat.put("t1", 0); beat.put("t2", 0); beat.put("rd", 0); beat.put("cr", 0);
                if (i % 8 == 0 || i % 8 == 4) beat.put("bd", 1);
                if (i % 8 == 2 || i % 8 == 6) beat.put("sd", 1);
                if (i % 2 == 0) beat.put("hh", 1);
                pattern.add(beat);
            }
        } else {
            for (int i = 0; i < 16; i++) {
                Map<String, Integer> beat = new HashMap<>();
                beat.put("bd", 0); beat.put("sd", 0); beat.put("hh", 0);
                beat.put("t1", 0); beat.put("t2", 0); beat.put("rd", 0); beat.put("cr", 0);
                if (i % 8 == 0) { beat.put("bd", 1); beat.put("cr", 1); }
                if (i % 8 == 4) beat.put("bd", 1);
                if (i % 8 == 2 || i % 8 == 6) beat.put("sd", 1);
                if (i % 4 == 0) beat.put("hh", 1);
                pattern.add(beat);
            }
        }
        return pattern;
    }

    private String playBeat(Map<String, Integer> beat) {
        StringBuilder line = new StringBuilder();
        for (String key : drums.keySet()) {
            if (beat.getOrDefault(key, 0) == 1) {
                line.append("\u001B[32m").append(drums.get(key).symbol).append("\u001B[0m ");
            } else {
                line.append("  ");
            }
        }
        return line.toString();
    }

    private void displayTimeline() {
        for (Drum d : drums.values()) {
            System.out.print(d.name + " ");
        }
        System.out.println("\n─────────────────────────");
    }

    public void run(String style) {
        this.pattern = generateRockPattern(style);
        this.running = true;

        System.out.println("\u001B[36m🥁 Rock Drum Kit (Java)\u001B[0m");
        System.out.println("Темп: " + bpm + " BPM");
        System.out.println("Стиль: " + style);
        System.out.println("Нажмите Ctrl+C для остановки...\n");

        displayTimeline();

        int beatIndex = 0;
        ScheduledExecutorService executor = Executors.newSingleThreadScheduledExecutor();
        executor.scheduleAtFixedRate(() -> {
            if (!running) {
                executor.shutdown();
                return;
            }
            Map<String, Integer> beat = pattern.get(beatIndex);
            String line = playBeat(beat);
            int bar = beatIndex / 4 + 1;
            int beatInBar = beatIndex % 4 + 1;
            System.out.println(bar + "." + beatInBar + "  " + line);
            beatIndex = (beatIndex + 1) % pattern.size();
        }, 0, (long)(beatLen / 2 * 1000), TimeUnit.MILLISECONDS);

        try {
            Thread.sleep(30000); // 30 секунд
        } catch (InterruptedException e) {}
        running = false;
        executor.shutdown();
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("🥁 Rock Drum Kit (Java)");
        System.out.print("Стиль (shuffle/straight): ");
        String style = scanner.nextLine().trim().toLowerCase();
        if (!style.equals("shuffle") && !style.equals("straight")) style = "shuffle";
        scanner.close();
        drum_kit kit = new drum_kit(120);
        kit.run(style);
    }
}
