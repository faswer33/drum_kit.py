


### 1. `drum_kit.py` (Python)

```python
# drum_kit.py — Python версия

import time
import random
import threading
import os
from colorama import init, Fore, Style

init(autoreset=True)

class DrumKit:
    def __init__(self, bpm=120):
        self.bpm = bpm
        self.beat_length = 60 / bpm
        self.running = False
        self.pattern = []
        self.drums = {
            'bd': {'name': 'Бас', 'key': '1', 'symbol': '█'},
            'sd': {'name': 'Малый', 'key': '2', 'symbol': '▓'},
            'hh': {'name': 'Хай-хэт', 'key': '3', 'symbol': '▒'},
            't1': {'name': 'Том 1', 'key': '4', 'symbol': '░'},
            't2': {'name': 'Том 2', 'key': '5', 'symbol': '░'},
            'rd': {'name': 'Райд', 'key': '6', 'symbol': '●'},
            'cr': {'name': 'Крэш', 'key': '7', 'symbol': '◆'}
        }

    def generate_rock_pattern(self, style='shuffle'):
        """Генерирует рок-ритм."""
        pattern = []
        if style == 'shuffle':
            # Шаффл: бас на 1 и 3, малый на 2 и 4, хай-хэт на все восьмые
            for i in range(16):
                beat = {'bd': 0, 'sd': 0, 'hh': 0, 't1': 0, 't2': 0, 'rd': 0, 'cr': 0}
                if i % 8 == 0 or i % 8 == 4:
                    beat['bd'] = 1
                if i % 8 == 2 or i % 8 == 6:
                    beat['sd'] = 1
                if i % 2 == 0:
                    beat['hh'] = 1
                pattern.append(beat)
        elif style == 'straight':
            # Прямой рок: бас на 1 и 3, малый на 2 и 4, хай-хэт на четверти
            for i in range(16):
                beat = {'bd': 0, 'sd': 0, 'hh': 0, 't1': 0, 't2': 0, 'rd': 0, 'cr': 0}
                if i % 8 == 0:
                    beat['bd'] = 1
                    beat['cr'] = 1
                if i % 8 == 4:
                    beat['bd'] = 1
                if i % 8 == 2 or i % 8 == 6:
                    beat['sd'] = 1
                if i % 4 == 0:
                    beat['hh'] = 1
                pattern.append(beat)
        return pattern

    def play_beat(self, beat):
        """Воспроизводит один удар."""
        line = ""
        for drum in self.drums.values():
            if beat.get(drum['symbol'][0], 0):
                line += Fore.GREEN + drum['symbol'] + Style.RESET_ALL + " "
            else:
                line += "  "
        return line

    def display_timeline(self):
        """Отображает таймлайн."""
        drum_names = [d['name'] for d in self.drums.values()]
        print(Fore.CYAN + "  " + " ".join(drum_names))
        print("─" * (len(drum_names) * 3))

    def run(self, style='shuffle'):
        """Запускает проигрывание паттерна."""
        self.pattern = self.generate_rock_pattern(style)
        self.running = True

        print(Fore.CYAN + f"🥁 Rock Drum Kit (Python)")
        print(f"Темп: {self.bpm} BPM")
        print(f"Стиль: {style}")
        print("Нажмите Ctrl+C для остановки...\n")

        self.display_timeline()

        beat_index = 0
        try:
            while self.running:
                beat = self.pattern[beat_index]
                line = self.play_beat(beat)
                # Отображаем номер такта
                bar = (beat_index // 4) + 1
                beat_in_bar = (beat_index % 4) + 1
                print(f"{bar}.{beat_in_bar}  {line}")

                beat_index = (beat_index + 1) % len(self.pattern)
                time.sleep(self.beat_length / 2)  # Восьмые ноты

        except KeyboardInterrupt:
            self.running = False
            print("\n⏹️ Остановка...")

    def interactive_mode(self):
        """Режим интерактивной игры на клавиатуре."""
        print(Fore.CYAN + "🥁 Интерактивный режим (Python)")
        print("Нажмите клавиши 1-7 для удара:")
        for key, drum in self.drums.items():
            print(f"  {drum['key']} — {drum['name']}")
        print("  q — выход")

        try:
            while True:
                if os.name == 'nt':
                    # Windows
                    import msvcrt
                    if msvcrt.kbhit():
                        ch = msvcrt.getch().decode('ascii').lower()
                        if ch == 'q':
                            break
                        for drum in self.drums.values():
                            if ch == drum['key']:
                                print(Fore.GREEN + f"🥁 {drum['name']}!" + Style.RESET_ALL)
                else:
                    # Unix
                    import termios, sys, tty
                    fd = sys.stdin.fileno()
                    old_settings = termios.tcgetattr(fd)
                    try:
                        tty.setraw(fd)
                        ch = sys.stdin.read(1)
                        if ch == 'q':
                            break
                        for drum in self.drums.values():
                            if ch == drum['key']:
                                print(Fore.GREEN + f"🥁 {drum['name']}!" + Style.RESET_ALL)
                    finally:
                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except KeyboardInterrupt:
            print("\n⏹️ Выход...")

def main():
    drum = DrumKit(bpm=120)
    print("🥁 Rock Drum Kit (Python)")
    print("Выберите режим:")
    print("1. Автоматический проигрыватель")
    print("2. Интерактивный режим (игра на клавиатуре)")
    choice = input("Ваш выбор (1/2): ").strip()

    if choice == '2':
        drum.interactive_mode()
    else:
        style = input("Стиль (shuffle/straight): ").strip().lower()
        if style not in ['shuffle', 'straight']:
            style = 'shuffle'
        drum.run(style)

if __name__ == "__main__":
    main()
