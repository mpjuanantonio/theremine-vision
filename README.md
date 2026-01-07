# Virtual Theremin - Real-Time Hand Tracking Audio Synthesis

A virtual system inspired by the Theremine that uses MediaPipe hand tracking to control audio synthesis in real time. Control pitch with your right hand and volume with your left hand, plus real-time vibrato and reverb effects.

## Features

- Real-time hand tracking using MediaPipe with sub-50ms latency
- Audio synthesis supporting four waveform types: sine, square, sawtooth, and triangle
- **Vibrato control**: Pinch gesture on right hand controls vibrato depth
- **Reverb control**: Left hand Y-axis controls reverb/delay intensity
- **Harmonics synthesis**: Enriched sine wave with configurable harmonics
- Intuitive theremin control: Right hand Y-axis controls pitch, left hand X-axis controls volume
- **Automatic fullscreen**: Detects screen resolution for optimal display
- Real-time visualization of hand positions and audio parameters
- Professional-grade audio with configurable frequency range (200-2000 Hz)
- Low-latency PyAudio integration for responsive audio generation
- **Modular architecture**: Organized in separate modules (audio, video, utils, main)

## Quick Start

Requirements: Python 3.10+, webcam with audio output

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main_module/theremin_main.py

# Run with different waveform
python main_module/theremin_main.py --wave square

# Run with custom resolution
python main_module/theremin_main.py --width 1280 --height 720
```

## Documentation

- [Installation Guide](docs/INSTALLATION.md) - Setup instructions with troubleshooting
- [Audio Module](docs/AUDIO.md) - Audio synthesis documentation
- [Video Module](docs/VIDEO.md) - Hand tracking documentation

## Controls

| Key | Action |
|-----|--------|
| `s` | Toggle waveform type |
| `q` / `ESC` | Exit application |

## Hand Control Mapping

### Right Hand - Pitch & Vibrato

#### Y-Axis → Pitch Control

- **Top position** (Y = 0.0) → High pitch (~2000 Hz)
- **Middle position** (Y = 0.5) → Mid pitch (~632 Hz)
- **Bottom position** (Y = 1.0) → Low pitch (~200 Hz)

#### Pinch Gesture → Vibrato Control

- **Fingers together** (pinch ≤ 0.02) → Minimal vibrato
- **Fingers apart** (pinch ≥ 0.15) → Maximum vibrato depth

### Left Hand - Volume, Reverb & Wave Shape

#### X-Axis → Volume Control

- **Left position** (X = 0.0) → Silence (0%)
- **Center position** (X = 0.5) → Maximum volume (100%)
- Volume zone limited to left half of screen

#### Y-Axis → Reverb Control

- **Top position** (Y ≤ 0.30) → Maximum reverb (0.8s delay)
- **Bottom position** (Y ≥ 0.85) → Minimum reverb (0.1s delay)

#### Pinch Gesture → Toggle Waveform Type

- Do the OK gesture to change the waveform type instead of using key "s"

## System Requirements

- Python 3.10, 3.11, or 3.12 (3.11 recommended)
- Functional webcam and audio output
- Linux distro compatible with apt-get or Windows

## Project Structure

```
theremine-vision/
├── main_module/
│   ├── theremin_main.py          # Main application entry point
│   └── audio_video_integration.py # Audio-video parameter mapping
├── video_module/
│   ├── video_processor.py        # Video capture and hand tracking
│   └── handPositionCalculator.py # Position and gesture calculation
├── audio_module/
│   └── theremin_synthesizer.py   # Audio synthesis with effects
├── utils/
│   └── opencv_draw.py            # OpenCV drawing utilities
├── docs/
│   ├── INSTALLATION.md           # Installation guide
│   ├── AUDIO.md                  # Audio documentation
│   └── VIDEO.md                  # Video documentation
└── requirements.txt              # Python dependencies
```

## Basic Usage

```python
from video_module.video_processor import VideoProcessor
from video_module.handPositionCalculator import HandPositionCalculator
from audio_module.theremin_synthesizer import ThereminSynthesizer
from main_module.audio_video_integration import integrate_audio_with_tracking

# Initialize
synthesizer = ThereminSynthesizer(
    sample_rate=44100,
    min_frequency=200.0,
    max_frequency=2000.0,
    wave_type='sine'
)
video_processor = VideoProcessor(width=1920, height=1080)

# Start
synthesizer.start()

# Main loop
while True:
    frame, results = video_processor.process_frame()
    if frame is None:
        break
    
    # Update hand positions and audio parameters
    integrate_audio_with_tracking(video_processor.position_calculator, synthesizer)
    
    # Get info including vibrato and reverb
    info = synthesizer.get_info()
    print(f"Note: {info['note']}, Vibrato: {info['vibrato_depth']:.3f}, Reverb: {info['delay_seconds']:.2f}s")

# Cleanup
synthesizer.cleanup()
video_processor.cleanup()
info = synthesizer.get_info()
print(f"Frequency: {info['frequency']:.2f} Hz")
print(f"Vibrato: {info['vibrato_depth']:.3f}")
print(f"Reverb: {info['delay_seconds']:.2f}s")

# Cleanup
synthesizer.cleanup()
```

## Troubleshooting

- **No audio output**: Verify PyAudio installation (`pip list | grep pyaudio`)
- **Hands not detected**: Check lighting and webcam angle
- **Compilation errors**: See [Installation Guide](docs/INSTALLATION.md)

## Technical Specifications

- Audio Format: 32-bit float, mono, 44.1 kHz
- Latency: < 50ms
- Hand Detection: MediaPipe Hands (21 landmarks per hand)
- Position Averaging: 6-point averaging for stability
- Waveforms: Sine (with harmonics), Square, Sawtooth, Triangle
- Effects: Real-time vibrato (LFO modulation) and reverb (delay buffer)
- Harmonics: Configurable additive synthesis [1.0, 0.5, 0.25, 0.125]

## Installation

For complete installation instructions, see [Installation Guide](docs/INSTALLATION.md).

## License

Open-source project. Free to use and modify.
