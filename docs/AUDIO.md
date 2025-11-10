# Audio Module Documentation

## Overview

The `ThereminSynthesizer` class generates real-time audio based on hand positions. It implements virtual theremin synthesis using PyAudio.

## Theremin Operation

### Right Hand (Y-Axis) → Pitch/Frequency

```
Y Position: 0.0 (top)    → 2000 Hz (high pitch)
Y Position: 0.5 (middle) → 632 Hz  (mid pitch)
Y Position: 1.0 (bottom) → 200 Hz  (low pitch)
```

- Uses **logarithmic scale** for natural musical progression
- Automatic smoothing with average of 5 most recent values

### Left Hand (X-Axis) → Volume

```
X Position: 0.0 (left)   → 0%   (silence)
X Position: 0.5 (center) → 35%  (mid volume)
X Position: 1.0 (right)  → 100% (maximum)
```

- Uses smooth curve (exponent 1.5)
- Automatic smoothing with average of 3 most recent values

## Components

### theremin_synthesizer.py

Main class implementing:
- Real-time audio synthesis
- 4 waveform types: sine, square, sawtooth, triangle
- Automatic transition smoothing
- Musical note name calculation
- Thread-safe with locks
- Sub-50ms latency

### audio_video_integration.py

Integration functions:
- `integrate_audio_with_tracking()`: Connects HandPositionCalculator with ThereminSynthesizer
- `draw_audio_info()`: Visualizes audio information on frame
- `draw_theremin_guide()`: Draws visual theremin guides

## Waveform Types

| Type | Description | Characteristic |
|------|-------------|-----------------|
| **Sine** | Pure smooth tone | Melodic, classical |
| **Square** | Bright electronic tone | Synthesizer classic |
| **Sawtooth** | Rich full spectrum | Powerful bass |
| **Triangle** | Smooth with body | Intermediate |

## Mathematical Formulas

### Frequency Calculation

```python
# Logarithmic scale for natural musical progression
normalized_pitch = 1.0 - right_hand_y  # Invert Y axis
log_min = log(200)
log_max = log(2000)
log_freq = log_min + normalized_pitch * (log_max - log_min)
frequency = exp(log_freq)
```

### Volume Calculation

```python
# Smooth volume curve
volume = left_hand_x ** 1.5
```

### Waveform Generation

```python
phase_increment = 2π * frequency / sample_rate
phases = current_phase + arange(num_samples) * phase_increment

if wave_type == 'sine':
    wave = sin(phases)
elif wave_type == 'square':
    wave = sign(sin(phases))
elif wave_type == 'sawtooth':
    wave = 2 * (phases/(2π) - floor(phases/(2π) + 0.5))
elif wave_type == 'triangle':
    wave = 2 * abs(2 * (phases/(2π) - floor(phases/(2π) + 0.5))) - 1
```

## Technical Configuration

### PyAudio Stream

```python
format: paFloat32        # 32-bit floating point audio
channels: 1              # Mono
rate: 44100              # 44.1 kHz (CD quality)
frames_per_buffer: 1024  # Balance between latency and stability
```

### Clipping Prevention

```python
audio_data = wave * volume * 0.3  # 0.3 factor prevents saturation
```

## Programmatic Usage

```python
from theremin_synthesizer import ThereminSynthesizer

# Create synthesizer
synth = ThereminSynthesizer(
    sample_rate=44100,
    min_frequency=200.0,
    max_frequency=2000.0,
    wave_type='sine',
    buffer_size=1024
)

# Start audio
synth.start()

# In your main loop
right_y = get_hand_position_y()
left_x = get_hand_position_x()
synth.update_position(right_y, left_x)

# Get current state
info = synth.get_info()
print(f"Note: {info['note']}, Frequency: {info['frequency']:.2f} Hz")

# Cleanup
synth.cleanup()
```

## Technical Specifications

- **Latency**: < 50ms
- **Precision**: 32-bit float
- **Thread-safe**: Yes (with locks)
- **Smoothing**: Automatic
- **Frequency Range**: 200-2000 Hz (configurable)

## Troubleshooting

### Audio is choppy

- Increase `buffer_size` (e.g., 2048)
- Close other applications
- Reduce CPU load

### No audio output

- Verify PyAudio installation
- Check system volume level
- Verify speakers are connected

### High latency

- Reduce `buffer_size` (e.g., 512)
- Use low-latency audio system

---

For complete implementation details, see source code in theremin_synthesizer.py
