import mido
import time
import threading
from helpers import (
    send_nrpns,
    build_nrpns,
)

from helpers import send_nrpns

port_name = "USB MIDI Device"

print(f"Opening MIDI output: {port_name}")


def play_note(midi_note, with_ramp, port_name, channel, outport):
    vco_names = {36: "vco1", 38: "vco2", 40: "vco3", 41: "vco4"}
    vco_name = vco_names[midi_note]

    outport.send(mido.Message("note_on", note=midi_note, velocity=127, channel=channel))

    if with_ramp:
        level_nrpn = build_nrpns(vco_name, {"level": 0})
        send_nrpns(level_nrpn, channel, outport)
        threading.Thread(
            target=make_ramp,
            args=(vco_name, "level", 8, 0, 127, 0.0001, port_name, channel, outport),
            daemon=True,
        ).start()


def make_ramp(
    vco_name, param_name, steps, start, end, duration, port_name, channel, outport
):
    for step in range(steps):
        increment = (end - start) / steps
        val = round(increment + (step * (increment)))
        level_nrpn = build_nrpns(vco_name, {param_name: val})
        send_nrpns(level_nrpn, channel, outport)
        time.sleep(duration / steps)
