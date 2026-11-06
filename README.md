<img width=100% alt="TURN Up The Speakers" src="https://github.com/user-attachments/assets/13500d94-6fb7-4405-b8a9-401d7a676d33" />  

## About
KRK Rokit speakers will automatically go into standby mode if the audio input stays below a certain threshold for a specific period of time. 
When playing audio at night, low volume listening is the only way possible if you want ot be respectful towards your neighbors, family, etc.. 
However, in these cases, the automatic switch into standby disables further audio Output at the current volume. 
The only way to reactivate your speakers is to bring the volume above that threshold, although a small time interval with high enough volume is sufficient. 
Hence, an audio input at a certain volume is required for a continuous listening experience. 
In order to achieve this, every x minutes an unaudible audio output (around 20 Hertz) is played. Neither does it bother your neighbors, nor does it audibly interfere with your regular audio Output. 
This is what this application provides.


## Getting Started
1️⃣ **Clone Repository**  
``` 
git clone https://github.com/emiloetting/TurnUpTheSpeakers
```  

2️⃣ **Setup Environment**  
I highly recommend using [uv](https://docs.astral.sh/uv/) for managing your virtual environment.  
This will automatically create a virtual environment and install the required python version as well as sourcecode dependancies.  
Using uv, setup is fairly simple.    
```
cd TurnUpTheSpeakers
uv sync
```

> [!Important]
> This project requires an installation of PortAudio.
> Currently, this dependancy is automatically installed on Windows and MacOS.
> If you run this on a different OS, ensure PortAudio is installed

3️⃣ **Start App**  
Finally, all you have to do is start the application by running the main skript.
```
uv run main.py
``` 

## Default Settings
As for now, all main settings are set within file `main.py`.
| Setting               | Default       | Description|
|--------               |-------:        |------------|
| SINE_FREQ             |  25 [Hz]      | Frequency to be played in order to reactivate speakers   |
| PLAY_DURATION         |   5 [sec]     | How long sine frequency is to be played each time        |
| PLAY_EVERY            | 600 [sec]     | Interval between 2 audio outputs                         |
| STATE_JSON            | states.json  | Location of file to keep track of the current default audio output |
| UPDATE_INTERVAL       |   1 [s]       | How often to check current default audio output device |
