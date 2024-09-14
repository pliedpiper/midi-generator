from midiutil import MIDIFile
import random
import os  # Import os module to handle directories

# Mapping of note names to MIDI note numbers (C4 = MIDI note 60)
note_name_to_number = {
    'C': 0,
    'C#': 1,
    'Db': 1,
    'D': 2,
    'D#': 3,
    'Eb': 3,
    'E': 4,
    'F': 5,
    'F#': 6,
    'Gb': 6,
    'G': 7,
    'G#': 8,
    'Ab': 8,
    'A': 9,
    'A#': 10,
    'Bb': 10,
    'B': 11
}

def get_scale(root_note_name, scale_type, octaves):
    """
    Generates a list of MIDI note numbers for the specified scale.
    
    Args:
        root_note_name (str): The root note (e.g., 'C', 'D#', 'F').
        scale_type (str): The type of scale ('major' or 'minor').
        octaves (int): The number of octaves to include.
    
    Returns:
        list: A list of MIDI note numbers in the specified scale.
    """
    if root_note_name not in note_name_to_number:
        raise ValueError(f"Invalid root note name: {root_note_name}")
    root_note = note_name_to_number[root_note_name]
    if scale_type == 'major':
        intervals = [0, 2, 4, 5, 7, 9, 11]
    elif scale_type == 'minor':
        intervals = [0, 2, 3, 5, 7, 8, 10]
    else:
        raise ValueError(f"Unsupported scale type: {scale_type}")
    scale_notes = []
    starting_octave = 4  # You can adjust the starting octave if needed
    for octave in range(starting_octave, starting_octave + octaves):
        for interval in intervals:
            note_number = root_note + interval + octave * 12
            if 0 <= note_number <= 127:  # MIDI note numbers range from 0 to 127
                scale_notes.append(note_number)
    return scale_notes

def generate_random_melody(scale_notes, length=32):
    """
    Generates a random melody from the given scale notes.
    
    Args:
        scale_notes (list): A list of MIDI note numbers in the scale.
        length (int): The number of notes in the melody.
    
    Returns:
        list: A list of MIDI note numbers representing the melody.
    """
    melody = []
    for _ in range(length):
        note = random.choice(scale_notes)
        melody.append(note)
    return melody

def generate_random_chords(scale_notes, length=16, chord_size=3):
    """
    Generates a sequence of random chords from the given scale notes.
    
    Args:
        scale_notes (list): A list of MIDI note numbers in the scale.
        length (int): The number of chords to generate.
        chord_size (int): The number of notes in each chord.
    
    Returns:
        list: A list of chords, where each chord is a list of MIDI note numbers.
    """
    chords = []
    for _ in range(length):
        root = random.choice(scale_notes)
        chord = [root]
        for i in range(1, chord_size):
            # For a basic triad, skip every other note in the scale
            index = scale_notes.index(root)
            next_index = (index + i * 2) % len(scale_notes)
            chord_note = scale_notes[next_index]
            chord.append(chord_note)
        chords.append(chord)
    return chords

def create_midi_file(melody_or_chords, is_chords=False, filename="random_music.mid"):
    """
    Creates a MIDI file from the given melody or chords.
    
    Args:
        melody_or_chords (list): A list of MIDI note numbers or chords.
        is_chords (bool): True if the input is chords, False if it's a melody.
        filename (str): The output filename for the MIDI file, including path.
    """
    track    = 0
    channel  = 0
    time     = 0    # In beats
    duration = 1    # In beats
    tempo    = 120  # In BPM
    volume   = 100  # 0-127, as per the MIDI standard

    midi = MIDIFile(1)  # One track
    midi.addTempo(track, time, tempo)

    for item in melody_or_chords:
        if is_chords:
            # If item is a chord (list of notes)
            for note in item:
                midi.addNote(track, channel, note, time, duration, volume)
        else:
            # If item is a single note
            midi.addNote(track, channel, item, time, duration, volume)
        time += duration

    # Write the MIDI file to the specified filename
    with open(filename, "wb") as output_file:
        midi.writeFile(output_file)

def generate_drum_pattern(length=16, complexity='simple'):
    """
    Generates a drum pattern compatible with Addictive Drums 2.
    
    Args:
        length (int): The number of measures in the drum pattern.
        complexity (str): 'simple' or 'complex' drum pattern.
    
    Returns:
        list: A list of dictionaries representing drum events.
    """
    drum_pattern = []
    # MIDI note numbers for Addictive Drums 2 mapping
    drums = {
        'kick': 36,          # C1
        'snare': 38,         # D1
        'closed_hat': 42,    # F#1
        'open_hat': 46,      # A#1
        'low_tom': 45,       # A1
        'mid_tom': 48,       # C2
        'high_tom': 50,      # D2
        'crash_cymbal': 49,  # C#2
        'ride_cymbal': 51    # D#2
    }

    beats_per_measure = 4
    subdivision = 4  # 16th notes
    total_steps = length * beats_per_measure * subdivision
    step_duration = 1 / subdivision  # Duration of each step in beats

    for step in range(total_steps):
        time = step * step_duration
        events = []

        # Simple Pattern
        if complexity == 'simple':
            # Kick on beats 1 and 3
            if step % (subdivision * beats_per_measure) == 0 or step % (subdivision * beats_per_measure) == subdivision * 2:
                events.append({'note': drums['kick'], 'time': time, 'duration': step_duration})
            # Snare on beats 2 and 4
            if step % (subdivision * beats_per_measure) == subdivision * 1 or step % (subdivision * beats_per_measure) == subdivision * 3:
                events.append({'note': drums['snare'], 'time': time, 'duration': step_duration})
            # Hi-hat on every 8th note
            if step % (subdivision // 2) == 0:
                events.append({'note': drums['closed_hat'], 'time': time, 'duration': step_duration})
        # Complex Pattern
        elif complexity == 'complex':
            # Kick patterns with variations
            if random.random() < 0.5:
                events.append({'note': drums['kick'], 'time': time, 'duration': step_duration})
            # Snare with ghost notes
            if step % (subdivision * beats_per_measure) == subdivision * 1 or step % (subdivision * beats_per_measure) == subdivision * 3:
                events.append({'note': drums['snare'], 'time': time, 'duration': step_duration})
            elif random.random() < 0.1:
                events.append({'note': drums['snare'], 'time': time, 'duration': step_duration * 0.5})
            # Hi-hat with openings
            if step % (subdivision // 2) == 0:
                if random.random() < 0.2:
                    events.append({'note': drums['open_hat'], 'time': time, 'duration': step_duration})
                else:
                    events.append({'note': drums['closed_hat'], 'time': time, 'duration': step_duration})
            # Toms and cymbals occasionally
            if random.random() < 0.05:
                events.append({'note': random.choice([drums['low_tom'], drums['mid_tom'], drums['high_tom']]), 'time': time, 'duration': step_duration})
            if random.random() < 0.02:
                events.append({'note': drums['crash_cymbal'], 'time': time, 'duration': step_duration})
        else:
            raise ValueError("Invalid complexity level. Choose 'simple' or 'complex'.")

        drum_pattern.extend(events)

    return drum_pattern

def create_drum_midi_file(drum_pattern, complexity, filename="drum_pattern.mid"):
    """
    Creates a MIDI file from the given drum pattern.
    
    Args:
        drum_pattern (list): A list of drum events.
        complexity (str): The complexity level ('simple' or 'complex').
        filename (str): The output filename for the MIDI file.
    """
    track    = 0
    channel  = 9  # MIDI channel 10 (drums), channels are 0-15
    tempo    = 120  # In BPM
    volume   = 100  # 0-127, as per the MIDI standard

    midi = MIDIFile(1)  # One track
    midi.addTempo(track, 0, tempo)

    for event in drum_pattern:
        midi.addNote(track, channel, event['note'], event['time'], duration=event['duration'], volume=volume)

    # Ensure the 'drum midis' directory and subdirectory exist
    output_dir = os.path.join("drum midis", complexity)
    os.makedirs(output_dir, exist_ok=True)

    # Save the MIDI file into the appropriate subdirectory
    output_path = os.path.join(output_dir, filename)

    with open(output_path, "wb") as output_file:
        midi.writeFile(output_file)

def generate_drum_midi():
    try:
        length = int(input("Enter the number of measures for the drum pattern: ").strip())
        if length <= 0:
            raise ValueError("Length must be positive.")
    except ValueError as e:
        print(f"Invalid input for length: {e}")
        return

    complexity = input("Enter 'simple' for a simple pattern or 'complex' for a complex pattern: ").strip().lower()
    if complexity not in ['simple', 'complex']:
        print("Invalid complexity level. Choose 'simple' or 'complex'.")
        return

    drum_pattern = generate_drum_pattern(length, complexity)
    filename = f"drum_pattern_{complexity}_{length}measures.mid"
    create_drum_midi_file(drum_pattern, complexity, filename=filename)
    print(f"Generated MIDI file: {os.path.join('drum midis', complexity, filename)}")

def generate_melody_or_chords(generation_type):
    root_note = input("Enter the root note (e.g., C, D#, F): ").strip()
    scale_type = input("Enter the scale type (major or minor): ").strip().lower()
    try:
        octaves = int(input("Enter the number of octaves: ").strip())
        if octaves <= 0:
            raise ValueError("Number of octaves must be positive.")
    except ValueError as e:
        print(f"Invalid input for octaves: {e}")
        return
    try:
        scale_notes = get_scale(root_note, scale_type, octaves)
    except ValueError as e:
        print(e)
        return

    # Create the output directory based on the key
    output_dir = os.path.join("Generated Midi", f"{root_note}_{scale_type}")
    os.makedirs(output_dir, exist_ok=True)

    if generation_type == 'melody':
        melody = generate_random_melody(scale_notes)
        filename = f"random_melody_{root_note}_{scale_type}_{octaves}octaves.mid"
        filepath = os.path.join(output_dir, filename)
        create_midi_file(melody, is_chords=False, filename=filepath)
    elif generation_type == 'chords':
        try:
            chord_length = int(input("Enter the number of chords to generate: ").strip())
            if chord_length <= 0:
                raise ValueError("Number of chords must be positive.")
            chord_size = int(input("Enter the number of notes in each chord (e.g., 3 for triads): ").strip())
            if chord_size <= 0:
                raise ValueError("Chord size must be positive.")
        except ValueError as e:
            print(f"Invalid input for chords: {e}")
            return
        chords = generate_random_chords(scale_notes, length=chord_length, chord_size=chord_size)
        filename = f"random_chords_{root_note}_{scale_type}_{octaves}octaves.mid"
        filepath = os.path.join(output_dir, filename)
        create_midi_file(chords, is_chords=True, filename=filepath)
    else:
        print("Invalid option. Please enter 'melody' or 'chords'.")
        return

    print(f"Generated MIDI file: {filepath}")

def main():
    generation_type = input("Enter 'melody' to generate a melody, 'chords' to generate chords, or 'drums' to generate drum patterns: ").strip().lower()
    if generation_type == 'drums':
        generate_drum_midi()
    elif generation_type in ['melody', 'chords']:
        generate_melody_or_chords(generation_type)
    else:
        print("Invalid option. Please enter 'melody', 'chords', or 'drums'.")
        return

if __name__ == "__main__":
    main()
