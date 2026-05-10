### Python Dependencies

Installed via pip:

- `music21`
- `mido`
- `python-rtmidi`

---

## Format

This program ingests a `.musicxml` file and 'plays' it on a Korg Electribe ER-1 drum machine. The ER-1 has 4 oscillators that are triggered by MIDI notes 36, 38, 40, and 41; it does not read or produce MIDI notes as such. Therefore, notes must be translated to values that can be transmitted to the `pitch`, `mod depth`, and `mod speed` parameters as [NRPNs](https://en.wikipedia.org/wiki/NRPN).

The ER-1 has 4 voltage controlled oscillators and is therefore capable of up to 4 voice polyphony. The `.musicxml` files have to be formatted in a specific way so that the voices are distributed properly. If you have a 4-voice score already, where each voice has its own stave, you can export it as a `musicxml` file and play it with no further changes needed. If you are arranging a score or writing one from scratch, arrange it such that each voice gets its own stave and is completely monophonic.

## Setup

### 1. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

`pip install -r requirements.txt`

### 3. MIDI setup

To run the program, you must know the ER-1's MIDI channel and the name of the MIDI port it is connected to (these are supplied as arguments). If you don't know the port name, you can get a list of available ports by using the command: `python3 list_ports.py`.

## Usage

Run the main script:
`python play.py <file_name> --bpm <bpm> --port <port_name> --channel <channel_number>`

Example:
`python3 play.py example-fugue.musicxml --bpm 137 --port "USB MIDI Device" --channel 10`
