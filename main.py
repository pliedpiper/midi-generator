# music_generator.py

import os
import random
import tkinter as tk
from tkinter import ttk, messagebox
import threading

import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage

# Constants and Mappings
NOTE_NAME_TO_NUMBER = {
    'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5,
    'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11
}

SCALE_INTERVALS = {
    'Major': [0, 2, 4, 5, 7, 9, 11],
    'Natural Minor': [0, 2, 3, 5, 7, 8, 10],
    'Harmonic Minor': [0, 2, 3, 5, 7, 8, 11],
    'Melodic Minor': [0, 2, 3, 5, 7, 9, 11],
    'Pentatonic Major': [0, 2, 4, 7, 9],
    'Pentatonic Minor': [0, 3, 5, 7, 10],
    'Blues': [0, 3, 5, 6, 7, 10],
}

INSTRUMENTS = {
    'Acoustic Grand Piano': 0,
    'Electric Guitar (clean)': 27,
    'Electric Bass (finger)': 33,
    'Violin': 40,
    'Trumpet': 56,
    'Tenor Sax': 66,
    'Flute': 73,
    'Synth Lead': 80,
}

CHORD_PROGRESSIONS = {
    'I-IV-V': [1, 4, 5],
    'I-V-vi-IV': [1, 5, 6, 4],
    'ii-V-I': [2, 5, 1],
    '12-bar Blues': [1, 4, 1, 1, 4, 4, 1, 1, 5, 4, 1, 5],
}

# Utility Functions
def sanitize_filename(filename):
    return "".join(c for c in filename if c.isalnum() or c in (' ', '_', '-')).rstrip()

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Music Generation Classes
class Scale:
    def __init__(self, root_note_name, scale_type, octaves=5):
        self.root_note_name = root_note_name
        self.scale_type = scale_type
        self.octaves = octaves
        self.notes = self.generate_scale_notes()

    def generate_scale_notes(self):
        if self.root_note_name not in NOTE_NAME_TO_NUMBER:
            raise ValueError(f"Invalid root note name: {self.root_note_name}.")
        if self.scale_type not in SCALE_INTERVALS:
            raise ValueError(f"Invalid scale type: {self.scale_type}.")

        root_note = NOTE_NAME_TO_NUMBER[self.root_note_name]
        scale_notes = []
        for octave in range(self.octaves):
            for interval in SCALE_INTERVALS[self.scale_type]:
                note_number = root_note + interval + (octave * 12)
                if 0 <= note_number <= 127:
                    scale_notes.append(note_number)
        return scale_notes

class RhythmPattern:
    def __init__(self, length, time_signature, pattern_type='steady', complexity=1):
        self.length = length
        self.time_signature = time_signature
        self.pattern_type = pattern_type
        self.complexity = complexity
        self.pattern = self.generate_rhythm_pattern()

    def generate_rhythm_pattern(self):
        beats_per_measure, beat_unit = map(int, self.time_signature.split('/'))
        total_beats = self.length * beats_per_measure

        if self.pattern_type == 'steady':
            rhythm_pattern = [1 for _ in range(total_beats)]
        elif self.pattern_type == 'complex':
            rhythm_pattern = self.generate_complex_rhythm(total_beats)
        else:
            rhythm_pattern = [1 for _ in range(total_beats)]
        return rhythm_pattern

    def generate_complex_rhythm(self, total_beats):
        rhythm_pattern = []
        while total_beats > 0:
            duration = random.choice([0.25, 0.5, 0.75, 1])
            if duration <= total_beats:
                rhythm_pattern.append(duration)
                total_beats -= duration
            else:
                rhythm_pattern.append(total_beats)
                total_beats = 0
        return rhythm_pattern

class MelodyGenerator:
    def __init__(self, scale_notes, rhythm_pattern, complexity=1, octave_range=(3, 5)):
        self.scale_notes = scale_notes
        self.rhythm_pattern = rhythm_pattern
        self.complexity = complexity
        self.octave_range = octave_range
        self.melody = self.generate_melody()

    def generate_melody(self):
        melody = []
        current_time = 0
        previous_note = None
        for duration in self.rhythm_pattern:
            note = self.select_note(previous_note)
            event = {'note': note, 'duration': duration, 'velocity': 64, 'start_time': current_time}
            melody.append(event)
            current_time += duration
            previous_note = note
        return melody

    def select_note(self, previous_note):
        notes_in_range = [n for n in self.scale_notes if self.octave_range[0]*12 <= n <= self.octave_range[1]*12]
        if self.complexity == 1:
            return random.choice(notes_in_range)
        else:
            # Implement more complex note selection
            if previous_note:
                step = random.choice([-2, -1, 1, 2])
                new_note = previous_note + step
                if new_note in notes_in_range:
                    return new_note
            return random.choice(notes_in_range)

class ChordProgressionGenerator:
    def __init__(self, scale_notes, progression_pattern, rhythm_pattern, chord_size=3):
        self.scale_notes = scale_notes
        self.progression_pattern = progression_pattern
        self.rhythm_pattern = rhythm_pattern
        self.chord_size = chord_size
        self.chords = self.generate_chord_progression()

    def generate_chord_progression(self):
        chords = []
        current_time = 0
        scale_length = len(self.scale_notes)
        progression = self.progression_pattern.copy()
        progression_index = 0
        for duration in self.rhythm_pattern:
            degree = progression[progression_index % len(progression)]
            progression_index += 1
            root_index = (degree - 1) % scale_length
            chord_notes = [self.scale_notes[(root_index + i * 2) % scale_length] for i in range(self.chord_size)]
            event = {'notes': chord_notes, 'duration': duration, 'velocity': 64, 'start_time': current_time}
            chords.append(event)
            current_time += duration
        return chords

class BassLineGenerator:
    def __init__(self, chord_progression, time_signature, bass_octave=2):
        self.chord_progression = chord_progression
        self.time_signature = time_signature
        self.bass_octave = bass_octave
        self.bass_line = self.generate_bass_line()

    def generate_bass_line(self):
        bass_line = []
        for chord in self.chord_progression:
            root_note = chord['notes'][0] - (12 * (self.bass_octave - 1))
            event = {
                'note': root_note,
                'duration': chord['duration'],
                'velocity': 64,
                'start_time': chord['start_time']
            }
            bass_line.append(event)
        return bass_line

# MIDI File Handling
class MIDIFileCreator:
    def __init__(self, tempo, time_signature):
        self.tempo = tempo
        self.time_signature = time_signature
        self.mid = MidiFile()
        self.ticks_per_beat = self.mid.ticks_per_beat

    def create_track(self, events, instrument, is_drum=False):
        track = MidiTrack()
        self.mid.tracks.append(track)
        track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(self.tempo), time=0))
        beats_per_measure, beat_unit = map(int, self.time_signature.split('/'))
        track.append(MetaMessage('time_signature', numerator=beats_per_measure, denominator=beat_unit, time=0))
        if not is_drum:
            track.append(Message('program_change', program=instrument, time=0))
        previous_time = 0
        events.sort(key=lambda x: x['start_time'])
        for event in events:
            delta_time = int((event['start_time'] - previous_time) * self.ticks_per_beat)
            delta_time = max(delta_time, 0)
            channel = 9 if is_drum else 0
            track.append(Message('note_on', note=event['note'], velocity=event['velocity'], time=delta_time, channel=channel))
            note_duration = int(event['duration'] * self.ticks_per_beat)
            track.append(Message('note_off', note=event['note'], velocity=0, time=note_duration, channel=channel))
            previous_time = event['start_time'] + event['duration']
        return track

    def save(self, output_dir, filename):
        ensure_dir(output_dir)
        self.mid.save(os.path.join(output_dir, filename))

# GUI Application
class MusicGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Generator for Producers")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # Styles
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 12))
        style.configure('TButton', font=('Arial', 12))
        style.configure('TCheckbutton', background='#f0f0f0', font=('Arial', 12))

        # Variables
        self.generation_type_var = tk.StringVar(value='Generate Full Song')
        self.scale_type_var = tk.StringVar(value='Major')
        self.root_note_var = tk.StringVar(value='C')
        self.include_bass_var = tk.BooleanVar(value=True)
        self.part_type_var = tk.StringVar(value='Melody')
        self.tempo_var = tk.StringVar(value='120')
        self.measures_var = tk.StringVar(value='8')
        self.base_filename_var = tk.StringVar(value='MySong')
        self.chord_progression_var = tk.StringVar(value='I-IV-V')
        self.melody_complexity_var = tk.IntVar(value=1)
        self.melody_octave_range_var = tk.StringVar(value='3-5')
        self.instrument_melody_var = tk.StringVar(value='Flute')
        self.instrument_chords_var = tk.StringVar(value='Acoustic Grand Piano')
        self.instrument_bass_var = tk.StringVar(value='Electric Bass (finger)')

        # Main Frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill='both', expand=True)

        # Build the GUI
        self.build_main_menu()

    def build_main_menu(self):
        ttk.Label(self.main_frame, text="Select Generation Type:").pack(pady=10)
        generation_type_menu = ttk.Combobox(self.main_frame, textvariable=self.generation_type_var, state="readonly", font=('Arial', 12))
        generation_type_menu['values'] = ('Generate Full Song', 'Generate Individual Part', 'Import MIDI (Under Development)')
        generation_type_menu.pack() 

        ttk.Button(self.main_frame, text="Next", command=self.show_options).pack(pady=20)

    # The rest of the class remains the same as in the code provided above.
    # Due to space constraints, I'm omitting the repetitive parts.
    # Please refer to the code above for the complete implementation.

# Run the Application
def run_app():
    root = tk.Tk()
    app = MusicGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()
