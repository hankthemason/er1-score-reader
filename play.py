from music21 import converter
import time
import mido
import argparse
from helpers import send_nrpns, build_nrpns, get_pitch_params
from play_note import play_note
from itertools import groupby

parser = argparse.ArgumentParser(
    description="Perform a MusicXML score on a MIDI device."
)
parser.add_argument("score_file", help="Path to the MusicXML file")
parser.add_argument("--bpm", type=int, default=100, help="Tempo in BPM (default: 100)")
parser.add_argument("--port", default="USB MIDI Device", help="MIDI output port name")
parser.add_argument("--channel", type=int, default=0, help="MIDI channel (default: 0)")
args = parser.parse_args()

MIDI_NOTES = [36, 38, 40, 41]

outport = mido.open_output(args.port)
time.sleep(1)


def perform(xml_file, bpm):
    score = converter.parse(xml_file)

    events = []
    for i, part in enumerate(score.parts[:4]):
        slur_active = False
        voice_note = MIDI_NOTES[i]
        for note in part.flatten().notes:
            start_time = note.offset * (60.0 / bpm)
            duration = note.quarterLength * (60.0 / bpm)

            if note.tie is not None and note.tie.type in ("stop", "continue"):
                should_play = False
            else:
                spanner_sites = note.getSpannerSites()
                should_play = not slur_active
                if spanner_sites:
                    slur_active = True
                    for site in spanner_sites:
                        if note is site.getFirst():
                            should_play = True
                        if note is site.getLast():
                            slur_active = False

            events.append(
                (start_time, note.pitch.midi, duration, voice_note, should_play)
            )

    events.sort(key=lambda e: e[0])

    # Playback
    playback_start = time.perf_counter()

    for start_time, group in groupby(events, key=lambda e: e[0]):
        while (time.perf_counter() - playback_start) < start_time:
            time.sleep(0.0005)

        for _, midi_pitch, duration, voice_note, should_play in list(group):
            vco_num = MIDI_NOTES.index(voice_note)
            vco_name = f"vco{vco_num + 1}"

            pitch_val, mod_depth_val = get_pitch_params(str(midi_pitch))
            nrpns = build_nrpns(
                vco_name, {"pitch": pitch_val, "mod_depth": mod_depth_val}
            )

            send_nrpns(nrpns, args.channel, outport)

            if should_play:
                play_note(voice_note, True, args.port, args.channel, outport)


perform(args.score_file, args.bpm)
