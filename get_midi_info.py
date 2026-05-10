import mido

MIDI_FILE = "./fugue-1.1-parts1.mid"
mid = mido.MidiFile(MIDI_FILE)

print(f"Type: {mid.type}")
print(f"Number of tracks: {len(mid.tracks)}")
print(f"Ticks per beat: {mid.ticks_per_beat}")
print(f"Length (seconds): {mid.length:.2f}")

for i, track in enumerate(mid.tracks):
    print(f"\nTrack {i}: {track.name}")
    print(f"Number of messages: {len(track)}")

print(mid.tracks[0])