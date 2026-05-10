import json
import mido
import os
import random

# Get the directory where the current script lives
BASE_DIR = os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, "../configs/params_by_voice.json")) as f:
    params = json.load(f)


def get_nrpn(voice_name, param):
    nrpn = params[voice_name][param]["nrpn"]
    return nrpn


def transform_nrpn(nrpn):
    nrpn_msb = (nrpn >> 7) & 0x7F
    nrpn_lsb = nrpn & 0x7F
    return [nrpn_msb, nrpn_lsb]


def build_nrpns(voice_name, params_to_send):
    """
    voice_name: str, e.g. 'vco1'
    params_to_send: dict of param_name -> value
    returns: list of nrpn dicts
    """
    nrpns = []
    for param, value in params_to_send.items():
        nrpn = get_nrpn(voice_name, param)
        nrpns.append({"nrpn": nrpn, "value": value})
    return nrpns


# add randomness to nrpns
def build_drunk_nrpns(voice_name, params_to_send):
    nrpns = []
    for param, value in params_to_send.items():
        nrpn = get_nrpn(voice_name, param)

        if param == "mod_depth" or param == "mod_speed":
            if random.random() > 0.5:
                plus_or_minus = random.choice([-1, 1])
                value += 1 * plus_or_minus
                # clamp value between 0-127 (MIDI safe)
                value = max(0, min(127, value))

        nrpns.append({"nrpn": nrpn, "value": value})

    return nrpns


def send_nrpns(nrpns, channel, outport):
    for nrpn_dict in nrpns:
        nrpn = nrpn_dict["nrpn"]
        value = nrpn_dict["value"]
        nrpn_msb, nrpn_lsb = transform_nrpn(nrpn)

        outport.send(
            mido.Message("control_change", control=99, value=nrpn_msb, channel=channel)
        )
        outport.send(
            mido.Message("control_change", control=98, value=nrpn_lsb, channel=channel)
        )
        outport.send(
            mido.Message("control_change", control=6, value=value, channel=channel)
        )
        outport.send(
            mido.Message("control_change", control=38, value=0, channel=channel)
        )
