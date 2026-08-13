# drum_kit.rb — Ruby версия

class DrumKit
  attr_accessor :bpm, :beat_len, :running, :pattern

  def initialize(bpm = 120)
    @bpm = bpm
    @beat_len = 60.0 / bpm
    @running = false
    @pattern = []
    @drums = {
      'bd' => { name: 'Бас', key: '1', symbol: '█' },
      'sd' => { name: 'Малый', key: '2', symbol: '▓' },
      'hh' => { name: 'Хай-хэт', key: '3', symbol: '▒' },
      't1' => { name: 'Том 1', key: '4', symbol: '░' },
      't2' => { name: 'Том 2', key: '5', symbol: '░' },
      'rd' => { name: 'Райд', key: '6', symbol: '●' },
      'cr' => { name: 'Крэш', key: '7', symbol: '◆' }
    }
  end

  def generate_rock_pattern(style = 'shuffle')
    pattern = []
    if style == 'shuffle'
      16.times do |i|
        beat = { 'bd' => 0, 'sd' => 0, 'hh' => 0, 't1' => 0, 't2' => 0, 'rd' => 0, 'cr' => 0 }
        beat['bd'] = 1 if i % 8 == 0 || i % 8 == 4
        beat['sd'] = 1 if i % 8 == 2 || i % 8 == 6
        beat['hh'] = 1 if i % 2 == 0
        pattern << beat
      end
    else
      16.times do |i|
        beat = { 'bd' => 0, 'sd' => 0, 'hh' => 0, 't1' => 0, 't2' => 0, 'rd' => 0, 'cr' => 0 }
        if i % 8 == 0
          beat['bd'] = 1
          beat['cr'] = 1
        end
        beat['bd'] = 1 if i % 8 == 4
        beat['sd'] = 1 if i % 8 == 2 || i % 8 == 6
        beat['hh'] = 1 if i % 4 == 0
        pattern << beat
      end
    end
    pattern
  end

  def play_beat(beat)
    line = ''
    @drums.each do |key, drum|
      if beat[key] == 1
        line += "\e[32m#{drum[:symbol]}\e[0m "
      else
        line += '  '
      end
    end
    line
  end

  def display_timeline
    @drums.each_value { |d| print "#{d[:name]} " }
    puts "\n─────────────────────────"
  end

  def run(style = 'shuffle')
    @pattern = generate_rock_pattern(style)
    @running = true

    puts "\e[36m🥁 Rock Drum Kit (Ruby)\e[0m"
    puts "Темп: #{@bpm} BPM"
    puts "Стиль: #{style}"
    puts "Нажмите Ctrl+C для остановки...\n"

    display_timeline

    beat_index = 0
    begin
      loop do
        beat = @pattern[beat_index]
        line = play_beat(beat)
        bar = beat_index / 4 + 1
        beat_in_bar = beat_index % 4 + 1
        puts "#{bar}.#{beat_in_bar}  #{line}"
        beat_index = (beat_index + 1) % @pattern.length
        sleep(@beat_len / 2)
      end
    rescue Interrupt
      puts "\n⏹️ Остановка..."
    end
  end
end

def main
  puts "🥁 Rock Drum Kit (Ruby)"
  print "Стиль (shuffle/straight): "
  style = gets.chomp.downcase
  style = 'shuffle' unless ['shuffle', 'straight'].include?(style)

  kit = DrumKit.new(120)
  kit.run(style)
end

main if __FILE__ == $0
