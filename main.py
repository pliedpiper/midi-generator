import random
import os
from midiutil import MIDIFile

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

# Define intervals for various scales and modes
scale_intervals = {
    'major': [0, 2, 4, 5, 7, 9, 11],
    'natural_minor': [0, 2, 3, 5, 7, 8, 10],
    'harmonic_minor': [0, 2, 3, 5, 7, 8, 11],
    'melodic_minor': [0, 2, 3, 5, 7, 9, 11],
    'dorian': [0, 2, 3, 5, 7, 9, 10],
    'phrygian': [0, 1, 3, 5, 7, 8, 10],
    'lydian': [0, 2, 4, 6, 7, 9, 11],
    'mixolydian': [0, 2, 4, 5, 7, 9, 10],
    'locrian': [0, 1, 3, 5, 6, 8, 10],
    'pentatonic_major': [0, 2, 4, 7, 9],
    'pentatonic_minor': [0, 3, 5, 7, 10],
    'blues': [0, 3, 5, 6, 7, 10],
    # Add more scales as needed
}

# General MIDI instrument numbers
instruments = {
    'Acoustic Grand Piano': 0,
    'Electric Bass (finger)': 33,
    # Other instruments can be added if needed
}

def get_scale(root_note_name, scale_type, octaves):
    """
    Generates a list of MIDI note numbers for the specified scale and octaves.
    """
    if root_note_name not in note_name_to_number:
        raise ValueError(f"Invalid root note name: {root_note_name}")
    if scale_type not in scale_intervals:
        raise ValueError(f"Unsupported scale type: {scale_type}")

    root_note = note_name_to_number[root_note_name]
    intervals = scale_intervals[scale_type]
    scale_notes = []
    starting_octave = 4  # Default starting octave

    for octave in range(starting_octave, starting_octave + octaves):
        for interval in intervals:
            note_number = root_note + interval + octave * 12
            if 0 <= note_number <= 127:
                scale_notes.append(note_number)
    return scale_notes

def generate_steady_rhythm(length, time_signature):
    """
    Generates a rhythm pattern where notes are played on every beat.
    """
    beats_per_measure, beat_unit = map(int, time_signature.split('/'))
    total_beats = length * beats_per_measure
    beat_duration = 1  # Duration of one beat in MIDI time units

    rhythm_pattern = [beat_duration for _ in range(int(total_beats))]
    return rhythm_pattern

def generate_melody(scale_notes, rhythm_pattern):
    """
    Generates a melody from the given scale notes and rhythm pattern.
    """
    melody = []
    default_velocity = 100  # Default velocity
    for duration in rhythm_pattern:
        note = random.choice(scale_notes)
        melody.append({'note': note, 'duration': duration, 'velocity': default_velocity})
    return melody

def generate_chord_progression(scale_notes, progression_pattern, rhythm_pattern, chord_size=3):
    """
    Generates chords based on a chord progression pattern.
    """
    chords = []
    default_velocity = 100  # Default velocity
    scale_length = len(scale_notes)
    progression_length = len(progression_pattern)
    rhythm_length = len(rhythm_pattern)

    for i in range(rhythm_length):
        degree = progression_pattern[i % progression_length]
        duration = rhythm_pattern[i]
        root_index = (degree - 1) % scale_length
        root_note = scale_notes[root_index]
        chord = [root_note]

        # Build chord based on the specified chord size
        for interval_num in range(1, chord_size):
            interval = interval_num * 2  # Skip every other note in the scale
            note_index = (root_index + interval) % scale_length
            chord_note = scale_notes[note_index]
            chord.append(chord_note)

        chords.append({'notes': chord, 'duration': duration, 'velocity': default_velocity})
    return chords

def generate_bass_line(chord_progression, time_signature, total_measures, bass_octave=2):
    """
    Generates a bass line with notes the length of a measure.
    """
    bass_line = []
    default_velocity = 100  # Default velocity
    beats_per_measure, _ = map(int, time_signature.split('/'))
    measure_duration = beats_per_measure * 1  # Each beat is duration 1

    for measure in range(total_measures):
        chord = chord_progression[measure * beats_per_measure]
        root_note = chord['notes'][0] - 12 * (4 - bass_octave)  # Adjust to bass octave
        bass_line.append({'note': root_note, 'duration': measure_duration, 'velocity': default_velocity})
    return bass_line

def generate_drum_pattern(length, complexity='simple'):
    """
    Generates a drum pattern compatible with Addictive Drums 2.
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

def create_drum_midi_file(drum_pattern, output_dir, filename="drum_pattern.mid", tempo=120):
    """
    Creates a MIDI file from the given drum pattern.
    """
    track    = 0
    channel  = 9  # MIDI channel 10 (drums), channels are 0-15
    volume   = 100  # 0-127, as per the MIDI standard

    midi = MIDIFile(1)  # One track
    midi.addTempo(track, 0, tempo)

    for event in drum_pattern:
        midi.addNote(track, channel, event['note'], event['time'], duration=event['duration'], volume=volume)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, filename)
    with open(output_path, "wb") as output_file:
        midi.writeFile(output_file)

def create_combined_midi_file(tracks, drum_pattern, output_dir, filename="song.mid", tempo=120, time_signature="4/4"):
    """
    Creates a combined MIDI file with chords, melody, bass, and drums.
    """
    midi = MIDIFile(len(tracks) + 1)  # Tracks + Drums

    beats_per_measure, beat_unit = map(int, time_signature.split('/'))

    for track_num, track in enumerate(tracks):
        midi.addTrackName(track_num, 0, track['name'])
        midi.addTempo(track_num, 0, tempo)
        midi.addTimeSignature(track_num, 0, beats_per_measure, int(beat_unit ** 0.5), 24)
        midi.addProgramChange(track_num, track['channel'], 0, track['instrument'])

        for event in track['events']:
            start_time = event.get('start_time', 0)
            if 'note' in event:
                midi.addNote(track_num, track['channel'], event['note'], start_time, event['duration'], event['velocity'])
            elif 'notes' in event:
                for note in event['notes']:
                    midi.addNote(track_num, track['channel'], note, start_time, event['duration'], event['velocity'])

    # Drums Track
    drum_track_num = len(tracks)
    midi.addTrackName(drum_track_num, 0, 'Drums')
    midi.addTempo(drum_track_num, 0, tempo)
    midi.addTimeSignature(drum_track_num, 0, beats_per_measure, int(beat_unit ** 0.5), 24)

    for event in drum_pattern:
        midi.addNote(drum_track_num, 9, event['note'], event['time'], event['duration'], 100)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, filename)
    with open(output_path, "wb") as output_file:
        midi.writeFile(output_file)

def create_midi_file(tracks, output_dir, filename="composition.mid", tempo=120, time_signature="4/4"):
    """
    Creates a MIDI file from the given tracks and saves it in the specified directory.
    """
    midi = MIDIFile(len(tracks))
    beats_per_measure, beat_unit = map(int, time_signature.split('/'))

    for track_num, track in enumerate(tracks):
        midi.addTrackName(track_num, 0, track['name'])
        midi.addTempo(track_num, 0, tempo)
        midi.addTimeSignature(track_num, 0, beats_per_measure, int(beat_unit ** 0.5), 24)
        midi.addProgramChange(track_num, track['channel'], 0, track['instrument'])

        for event in track['events']:
            start_time = event.get('start_time', 0)
            if 'note' in event:
                midi.addNote(track_num, track['channel'], event['note'], start_time, event['duration'], event['velocity'])
            elif 'notes' in event:
                for note in event['notes']:
                    midi.addNote(track_num, track['channel'], note, start_time, event['duration'], event['velocity'])

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, filename)
    with open(output_path, "wb") as output_file:
        midi.writeFile(output_file)

def main():
    print("Welcome to the Advanced MIDI Generator!")
    generation_type = input("Choose generation type ('song', 'melody', 'chords', 'drums', 'import'): ").strip().lower()

    if generation_type == 'import':
        # Placeholder for MIDI import and modification feature
        print("MIDI import and modification feature is under development.")
        return

    elif generation_type == 'song':
        # Generate a song with drums, chords, melody, and optional bass
        root_note = input("Enter the root note for the song (e.g., C, D#, F): ").strip()
        print("Available scales/modes:")
        for scale in scale_intervals.keys():
            print(f"- {scale}")
        scale_type = input("Enter the scale/mode for the song: ").strip().lower()
        octaves = 1
        tempo = random.randint(60, 140)
        time_signature = '4/4'
        total_length = 32  # Total number of measures
        section_length = 8  # Measures per section (Verse/Chorus)

        print(f"Generating song in key: {root_note} {scale_type}, Tempo: {tempo} BPM")

        try:
            scale_notes = get_scale(root_note, scale_type, octaves)
        except ValueError as e:
            print(e)
            return

        # Generate rhythm pattern with notes on every beat
        beats_per_measure, _ = map(int, time_signature.split('/'))
        rhythm_pattern = generate_steady_rhythm(total_length, time_signature)

        # Decide on including bass line
        include_bass = input("Include bass line? (yes/no, default 'yes'): ").strip().lower() or 'yes'

        # Initialize tracks
        chord_tracks = []
        melody_tracks = []
        bass_tracks = []

        # Define song structure: Verse (8 measures) -> Chorus (8 measures) -> Verse (8 measures) -> Chorus (8 measures)
        sections = ['Verse', 'Chorus', 'Verse', 'Chorus']
        current_time = 0

        # Generate drum pattern for the entire song
        drum_pattern = generate_drum_pattern(total_length, complexity='simple')

        # Generate music for each section
        for section in sections:
            # Generate chords
            if section == 'Verse':
                progression_pattern = [random.randint(1, 7) for _ in range(section_length)]
            elif section == 'Chorus':
                progression_pattern = [random.randint(1, 7) for _ in range(section_length)]
            # Adjust chord size if desired
            chord_size = 3  # Triads
            section_rhythm = generate_steady_rhythm(section_length, time_signature)
            chords = generate_chord_progression(scale_notes, progression_pattern, section_rhythm, chord_size=chord_size)
            for chord in chords:
                chord['start_time'] = current_time
                current_time += chord['duration']

            chord_tracks.append({
                'name': f'Chords',
                'channel': 0,
                'events': chords,
                'instrument': instruments['Acoustic Grand Piano']
            })

            # Generate melody
            melody_events = generate_melody(scale_notes, section_rhythm)
            current_time_melody = current_time - sum(section_rhythm)
            for note in melody_events:
                note['start_time'] = current_time_melody
                current_time_melody += note['duration']

            melody_tracks.append({
                'name': f'Melody',
                'channel': 1,
                'events': melody_events,
                'instrument': instruments['Acoustic Grand Piano']
            })

            # Generate bass line
            if include_bass == 'yes':
                # Total measures so far
                total_measures = int(current_time / beats_per_measure)
                bass_events = generate_bass_line(chords, time_signature, section_length)
                current_time_bass = current_time - sum(section_rhythm)
                for note in bass_events:
                    note['start_time'] = current_time_bass
                    current_time_bass += note['duration']

                bass_tracks.append({
                    'name': f'Bass',
                    'channel': 2,
                    'events': bass_events,
                    'instrument': instruments['Electric Bass (finger)']
                })

        # Combine tracks
        combined_chord_events = []
        for track in chord_tracks:
            combined_chord_events.extend(track['events'])

        combined_melody_events = []
        for track in melody_tracks:
            combined_melody_events.extend(track['events'])

        if include_bass == 'yes':
            combined_bass_events = []
            for track in bass_tracks:
                combined_bass_events.extend(track['events'])
            bass_tracks_combined = [{
                'name': 'Bass',
                'channel': 2,
                'events': combined_bass_events,
                'instrument': instruments['Electric Bass (finger)']
            }]
        else:
            bass_tracks_combined = []

        # Create song directory
        root_note_formatted = root_note.replace('#', 'sharp').replace('b', 'flat')
        scale_type_formatted = scale_type.replace(' ', '_')
        song_folder_name = f"{root_note_formatted}_{scale_type_formatted}_{tempo}bpm_song"
        output_dir = os.path.join("songs", song_folder_name)
        os.makedirs(output_dir, exist_ok=True)

        # Create individual MIDI files
        create_midi_file([{
            'name': 'Chords',
            'channel': 0,
            'events': combined_chord_events,
            'instrument': instruments['Acoustic Grand Piano']
        }], output_dir=output_dir, filename="chords.mid", tempo=tempo, time_signature=time_signature)

        create_midi_file([{
            'name': 'Melody',
            'channel': 1,
            'events': combined_melody_events,
            'instrument': instruments['Acoustic Grand Piano']
        }], output_dir=output_dir, filename="melody.mid", tempo=tempo, time_signature=time_signature)

        if bass_tracks_combined:
            create_midi_file(bass_tracks_combined, output_dir=output_dir, filename="bass.mid", tempo=tempo, time_signature=time_signature)

        create_drum_midi_file(drum_pattern, output_dir=output_dir, filename="drums.mid", tempo=tempo)

        # Create combined MIDI file
        all_tracks = [
            {
                'name': 'Chords',
                'channel': 0,
                'events': combined_chord_events,
                'instrument': instruments['Acoustic Grand Piano']
            },
            {
                'name': 'Melody',
                'channel': 1,
                'events': combined_melody_events,
                'instrument': instruments['Acoustic Grand Piano']
            }
        ]
        if bass_tracks_combined:
            all_tracks.append(bass_tracks_combined[0])

        create_combined_midi_file(all_tracks, drum_pattern, output_dir=output_dir, filename="song.mid", tempo=tempo, time_signature=time_signature)

        print(f"Generated song files in: {output_dir}")
        print("Files created:")
        print(f"- chords.mid")
        print(f"- melody.mid")
        if bass_tracks_combined:
            print(f"- bass.mid")
        print(f"- drums.mid")
        print(f"- song.mid (combined MIDI file)")

    else:
        # Common settings for melody and chords
        if generation_type in ['melody', 'chords']:
            root_note = input("Enter the root note (e.g., C, D#, F): ").strip()
            root_note_formatted = root_note.replace('#', 'sharp').replace('b', 'flat')
            print("Available scales/modes:")
            for scale in scale_intervals.keys():
                print(f"- {scale}")
            scale_type = input("Enter the scale/mode: ").strip().lower()
            scale_type_formatted = scale_type.replace(' ', '_')
            octaves = int(input("Enter the number of octaves (default 1): ") or "1")
            tempo = int(input("Enter the tempo in BPM (default 120): ") or "120")
            time_signature = input("Enter the time signature (e.g., '4/4', '3/4', default '4/4'): ") or "4/4"

            try:
                scale_notes = get_scale(root_note, scale_type, octaves)
            except ValueError as e:
                print(e)
                return

            rhythm_length = int(input("Enter the number of measures (default 4): ") or "4")
            # Generate rhythm pattern with notes on every beat
            rhythm_pattern = generate_steady_rhythm(rhythm_length, time_signature)

            # Use 'Acoustic Grand Piano' as default instrument
            instrument_name = 'Acoustic Grand Piano'
            instrument_number = instruments[instrument_name]

            if generation_type == 'melody':
                melody = generate_melody(scale_notes, rhythm_pattern)
                tracks = [{
                    'name': 'Melody',
                    'channel': 0,
                    'events': melody,
                    'instrument': instrument_number
                }]
                # Directory structure: Generated Midi/<Key>/melody/
                key_folder = f"{root_note_formatted}_{scale_type_formatted}"
                output_dir = os.path.join("Generated Midi", key_folder, "melody")
                filename = f"melody_{key_folder}_{tempo}bpm.mid"

                # Create MIDI file
                create_midi_file(tracks, output_dir=output_dir, filename=filename, tempo=tempo, time_signature=time_signature)
                print(f"Generated MIDI file: {os.path.join(output_dir, filename)}")

            elif generation_type == 'chords':
                # Chord progression
                progression_input = input("Enter chord progression degrees separated by spaces (e.g., '1 4 5 1', default '1 5 6 4', or 'random' to randomize): ") or "1 5 6 4"
                if progression_input.strip().lower() == 'random':
                    progression_length = int(input("Enter the number of chords in the progression (default 4): ") or "4")
                    progression_pattern = [random.randint(1, 7) for _ in range(progression_length)]
                    print(f"Randomly generated chord progression: {' '.join(map(str, progression_pattern))}")
                else:
                    progression_pattern = list(map(int, progression_input.strip().split()))
                # Ask for chord size
                chord_size = int(input("Enter the number of notes in each chord (e.g., 3 for triads, 4 for seventh chords, default 3): ") or "3")
                chords = generate_chord_progression(scale_notes, progression_pattern, rhythm_pattern, chord_size=chord_size)
                tracks = [{
                    'name': 'Chords',
                    'channel': 0,
                    'events': chords,
                    'instrument': instrument_number
                }]

                # Option to generate bass line
                include_bass = input("Include bass line? (yes/no, default 'no'): ").strip().lower() or 'no'
                bass_tracks = []
                if include_bass == 'yes':
                    bass_events = generate_bass_line(chords, time_signature, rhythm_length)
                    bass_tracks = [{
                        'name': 'Bass',
                        'channel': 1,
                        'events': bass_events,
                        'instrument': instruments['Electric Bass (finger)']
                    }]

                # Directory structure: Generated Midi/<Key>/chords/
                key_folder = f"{root_note_formatted}_{scale_type_formatted}"
                output_dir = os.path.join("Generated Midi", key_folder, "chords")
                filename = f"chords_{key_folder}_{tempo}bpm.mid"

                # Create MIDI file
                all_tracks = tracks + bass_tracks
                create_midi_file(all_tracks, output_dir=output_dir, filename=filename, tempo=tempo, time_signature=time_signature)
                print(f"Generated MIDI file: {os.path.join(output_dir, filename)}")

        elif generation_type == 'drums':
            # Drum pattern generation
            length = int(input("Enter the number of measures for the drum pattern (default 4): ") or "4")
            tempo = int(input("Enter the tempo in BPM (default 120): ") or "120")
            complexity = input("Enter 'simple' for a simple pattern or 'complex' for a complex pattern (default 'simple'): ").strip().lower() or 'simple'
            if complexity not in ['simple', 'complex']:
                print("Invalid complexity level. Choose 'simple' or 'complex'.")
                return

            drum_pattern = generate_drum_pattern(length, complexity)
            # Directory structure: Generated Midi/drums/<complexity>/
            output_dir = os.path.join("Generated Midi", "drums", complexity)
            filename = f"drum_pattern_{complexity}_{tempo}bpm_{length}measures.mid"

            # Create MIDI file
            create_drum_midi_file(drum_pattern, output_dir=output_dir, filename=filename, tempo=tempo)
            print(f"Generated MIDI file: {os.path.join(output_dir, filename)}")

        else:
            print("Invalid generation type.")
            return

if __name__ == "__main__":
    main()
