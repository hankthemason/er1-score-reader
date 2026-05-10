import json
import os

BASE_DIR = os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, "../configs/chromatic_pitch_map.json")) as f:
    pitch_map = json.load(f)


def get_pitch_params(midi_note):
    pitch = pitch_map[str(midi_note)]["pitch"]
    mod_depth = pitch_map[str(midi_note)]["mod_depth"]

    return [pitch, mod_depth]
