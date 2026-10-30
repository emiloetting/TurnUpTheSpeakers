from pathlib import Path
from sys_check import *
from threading import Thread



STATE_JSON = Path(__file__).parent / "states.json"
UPDATE_INTERVAL = 1    # [sec]
SINE_FREQ = 25         # [Hz]
PLAY_EVERY = 10*60     # [sec]
PLAY_DURATRION = 5     # [sec]



updater = Thread(
    target=update_states, 
    daemon=True, 
    name="State Updater",
    kwargs={
        "fp": STATE_JSON, 
        "interval": UPDATE_INTERVAL
        }
    )

player = Thread(
    target=play_sound, 
    daemon=True, 
    name="Audio Player",
    kwargs={
        "freq": SINE_FREQ, 
        "states_fp": STATE_JSON, 
        "play_duration": PLAY_DURATRION, 
        "silence": int(PLAY_EVERY-PLAY_DURATRION)
        }
    )


if __name__ == "__main__":
    updater.start()
    player.start()

    while True:
        time.sleep(1)