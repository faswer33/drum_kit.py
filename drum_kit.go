// drum_kit.go — Go версия

package main

import (
	"fmt"
	"math/rand"
	"os"
	"time"
)

type DrumKit struct {
	BPM       int
	BeatLen   float64
	Running   bool
	Pattern   []map[string]int
	Drums     map[string]Drum
}

type Drum struct {
	Name   string
	Key    string
	Symbol string
}

func NewDrumKit(bpm int) *DrumKit {
	return &DrumKit{
		BPM:     bpm,
		BeatLen: 60.0 / float64(bpm),
		Drums: map[string]Drum{
			"bd": {"Бас", "1", "█"},
			"sd": {"Малый", "2", "▓"},
			"hh": {"Хай-хэт", "3", "▒"},
			"t1": {"Том 1", "4", "░"},
			"t2": {"Том 2", "5", "░"},
			"rd": {"Райд", "6", "●"},
			"cr": {"Крэш", "7", "◆"},
		},
	}
}

func (d *DrumKit) generateRockPattern(style string) []map[string]int {
	pattern := []map[string]int{}
	if style == "shuffle" {
		for i := 0; i < 16; i++ {
			beat := map[string]int{"bd": 0, "sd": 0, "hh": 0, "t1": 0, "t2": 0, "rd": 0, "cr": 0}
			if i%8 == 0 || i%8 == 4 {
				beat["bd"] = 1
			}
			if i%8 == 2 || i%8 == 6 {
				beat["sd"] = 1
			}
			if i%2 == 0 {
				beat["hh"] = 1
			}
			pattern = append(pattern, beat)
		}
	} else {
		for i := 0; i < 16; i++ {
			beat := map[string]int{"bd": 0, "sd": 0, "hh": 0, "t1": 0, "t2": 0, "rd": 0, "cr": 0}
			if i%8 == 0 {
				beat["bd"] = 1
				beat["cr"] = 1
			}
			if i%8 == 4 {
				beat["bd"] = 1
			}
			if i%8 == 2 || i%8 == 6 {
				beat["sd"] = 1
			}
			if i%4 == 0 {
				beat["hh"] = 1
			}
			pattern = append(pattern, beat)
		}
	}
	return pattern
}

func (d *DrumKit) playBeat(beat map[string]int) string {
	line := ""
	for _, drum := range d.Drums {
		if beat[drum.Name] == 1 {
			line += "\x1b[32m" + drum.Symbol + "\x1b[0m "
		} else {
			line += "  "
		}
	}
	return line
}

func (d *DrumKit) displayTimeline() {
	for _, drum := range d.Drums {
		fmt.Printf("%s ", drum.Name)
	}
	fmt.Println()
	fmt.Println("─────────────────────────")
}

func (d *DrumKit) run(style string) {
	d.Pattern = d.generateRockPattern(style)
	d.Running = true

	fmt.Printf("\x1b[36m🥁 Rock Drum Kit (Go)\x1b[0m\n")
	fmt.Printf("Темп: %d BPM\n", d.BPM)
	fmt.Printf("Стиль: %s\n", style)
	fmt.Println("Нажмите Ctrl+C для остановки...\n")

	d.displayTimeline()

	beatIndex := 0
	ticker := time.NewTicker(time.Duration(d.BeatLen/2 * float64(time.Second)))
	defer ticker.Stop()

	for range ticker.C {
		if !d.Running {
			break
		}
		beat := d.Pattern[beatIndex]
		line := d.playBeat(beat)
		bar := beatIndex/4 + 1
		beatInBar := beatIndex%4 + 1
		fmt.Printf("%d.%d  %s\n", bar, beatInBar, line)
		beatIndex = (beatIndex + 1) % len(d.Pattern)
	}
}

func main() {
	fmt.Println("🥁 Rock Drum Kit (Go)")
	fmt.Println("1. Автоматический проигрыватель")
	fmt.Print("Ваш выбор (1): ")
	choice := ""
	fmt.Scanln(&choice)

	drum := NewDrumKit(120)

	if choice == "2" {
		// Интерактивный режим (упрощённо)
		fmt.Println("Интерактивный режим не реализован в Go версии")
	} else {
		fmt.Print("Стиль (shuffle/straight): ")
		style := ""
		fmt.Scanln(&style)
		if style != "shuffle" && style != "straight" {
			style = "shuffle"
		}
		drum.run(style)
	}
}
