def create_ramp_events(vco_name, start_time, steps=8, duration=0.1):
    """
    Generates non-blocking ramp events for a VCO level NRPN.
    Returns a list of tuples: (event_time, 'ramp', vco_name, value)
    """
    events = []
    increment = 127 / steps
    step_delay = duration / steps

    for step in range(1, steps + 1):
        ramp_time = start_time + step * step_delay
        value = int(step * increment)
        events.append((ramp_time, "ramp", vco_name, value))
    return events
