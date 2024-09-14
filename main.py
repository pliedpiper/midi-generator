from midiutil import MIDIFile
import random

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

def create_midi_file(melody, filename="random_melody.mid"):
    """
    Creates a MIDI file from the given melody.

    Args:
        melody (list): A list of MIDI note numbers.
        filename (str): The output filename for the MIDI file.
    """
    track    = 0
    channel  = 0
    time     = 0    # In beats
    duration = 1    # In beats
    tempo    = 120  # In BPM
    volume   = 100  # 0-127, as per the MIDI standard

    midi = MIDIFile(1)  # One track
    midi.addTempo(track, time, tempo)

    for note in melody:
        midi.addNote(track, channel, note, time, duration, volume)
        time += duration

    with open(filename, "wb") as output_file:
        midi.writeFile(output_file)

def main():
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
    melody = generate_random_melody(scale_notes)
    filename = f"random_melody_{root_note}_{scale_type}_{octaves}octaves.mid"
    create_midi_file(melody, filename)
    print(f"Generated MIDI file: {filename}")

if __name__ == "__main__":
    main()
