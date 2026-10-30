import sounddevice as sd
import json
import time
import numpy as np
from threading import Lock
from pathlib import Path
from utils import *



def get_default() -> dict:
    available = sd.query_devices()
    default = sd.default.device
    to_return = {
        "name": available[default[1]]["name"],
        "sr": available[default[1]]["default_samplerate"]
    }
    return to_return


def update_states(fp:Path|str, interval:float) -> None:
    while True:
        with Lock():
            with open(fp, "r", encoding="utf-8") as f:
                states = json.load(f)

            current_default = get_default()

            # Update only if necessary to avoid I/O load
            if (states["name"] != current_default["name"]) or (states["sr"] != current_default["sr"]):
                with open(fp, "w", encoding="utf-8") as f:
                    json.dump(current_default, f, ensure_ascii=False)

        time.sleep(interval)


def give_me_a_sine(freq:float, sr:int, duration:int) -> np.ndarray:
    """Creates a single sine cycle"""
    # Validate input
    freq = validate_float_arg(freq, "freq", min_value=0)
    sr = validate_int_arg(sr, "sr", min_value=8_000, max_value=96_000)   # higher SR uncommon
    duration = validate_int_arg(duration, "duration", min_value=1)      # no upper limit

    sine_wave = [np.sin(2 * np.pi * freq * x/sr) for x in range(sr)] * duration  # ensures full cycle
    return sine_wave


def play_sound(freq:float, states_fp:Path|str, play_duration:int, silence:int) -> None:
    # Validate input
    freq = validate_float_arg(freq, "freq", min_value=1)
    states_fp = validate_path_arg(states_fp, "states_fp")
    silence = validate_int_arg(silence, "silence", min_value=1)     # no upper limit

    # loop
    while True:
        # Ensure thread safety
        with Lock():
            with open(states_fp, "r", encoding="utf-8") as f:
                states = json.load(f)
                sample_rate = states["sr"]

        if not int(sample_rate) == sample_rate:
            raise ValueError("Cannot safely convert samplerate from float to int! Ensure set samplerate carries no decimals.")
        sample_rate = int(sample_rate)
        sine_to_play = give_me_a_sine(
            freq=freq,
            sr=sample_rate,
            duration=play_duration
        )

        print(f"Playing Audio at {freq}Hz at {sample_rate}Hz samplerate on device {states["name"]}")
        sd.play(sine_to_play, sample_rate, blocking=True)
        time.sleep(silence)
