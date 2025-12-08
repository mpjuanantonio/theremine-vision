# Audio Module Documentation

## Overview

The `ThereminSynthesizer` class generates real-time audio based on hand positions. It implements virtual theremin synthesis using PyAudio with vibrato, reverb, and harmonics support.

## Theremin Operation

### Right Hand → Pitch & Vibrato

#### Y-Axis → Pitch/Frequency

```
Y Position: 0.0 (top)    → 2000 Hz (high pitch)
Y Position: 0.5 (middle) → 632 Hz  (mid pitch)
Y Position: 1.0 (bottom) → 200 Hz  (low pitch)
```

- Uses **logarithmic scale** for natural musical progression
- Automatic smoothing with average of 5 most recent values

#### Pinch Gesture → Vibrato Depth

```
Pinch: 0.02 (fingers together) → 0.001 (minimal vibrato)
Pinch: 0.15 (fingers apart)    → 0.025 (maximum vibrato)
```

- Vibrato rate fixed at 5.0 Hz (LFO frequency)
- Modulates frequency by ±vibrato_depth percentage

### Left Hand → Volume & Reverb

#### X-Axis → Volume

```
X Position: 0.0 (left)   → 0%   (silence)
X Position: 0.5 (center) → 100% (maximum)
```

- Volume zone limited to left half of screen (LEFT_ZONE_LIMIT = 0.5)
- Uses smooth curve (exponent 1.5)
- Automatic smoothing with average of 3 most recent values

#### Y-Axis → Reverb

```
Y Position: 0.30 (top)    → 0.8s delay (maximum reverb)
Y Position: 0.85 (bottom) → 0.1s delay (minimum reverb)
```

- Useful zone: 30% to 85% of screen height
- Delay buffer resizes dynamically

## Components

### theremin_synthesizer.py

Main class implementing:
- Real-time audio synthesis
- 4 waveform types: sine, square, sawtooth, triangle
- **Harmonics synthesis** for enriched sine waves
- **Vibrato effect** via LFO (Low Frequency Oscillator)
- **Reverb effect** via delay buffer with feedback
- Automatic transition smoothing
- Musical note name calculation
- Thread-safe with locks
- Sub-50ms latency

### audio_video_integration.py

Integration functions and configuration constants:
- `integrate_audio_with_tracking()`: Connects HandPositionCalculator with ThereminSynthesizer
- `draw_audio_info()`: Visualizes audio information on frame
- `draw_theremin_guide()`: Draws visual theremin guides

**Configuration Constants:**
```python
# Volume
LEFT_ZONE_LIMIT = 0.5    # Volume control limited to left half

# Vibrato
PINCH_MIN = 0.02         # Minimum pinch distance
PINCH_MAX = 0.15         # Maximum pinch distance
VIBRATO_MIN = 0.001      # Minimum vibrato depth
VIBRATO_MAX = 0.02       # Maximum vibrato depth

# Reverb
REVERB_TOP = 0.30        # Y position for max reverb
REVERB_BOTTOM = 0.85     # Y position for min reverb
DELAY_MAX = 0.8          # Maximum delay in seconds
DELAY_MIN = 0.1          # Minimum delay in seconds
```

## Waveform Types

| Type | Description | Characteristic | Harmonics |
|------|-------------|----------------|-----------|
| **Sine** | Pure smooth tone | Melodic, classical | Additive synthesis |
| **Square** | Bright electronic tone | Synthesizer classic | Natural odd harmonics |
| **Sawtooth** | Rich full spectrum | Powerful bass | Natural all harmonics |
| **Triangle** | Smooth with body | Intermediate | Natural odd harmonics |

## Audio Effects

### Harmonics (Sine Wave Only)

Additive synthesis enriches the sine wave with overtones:

```python
harmonics = [1.0, 0.5, 0.25, 0.125]  # Fundamental, 2nd, 3rd, 4th

# Each harmonic is a multiple of the fundamental frequency
for i, amp in enumerate(harmonics):
    harmonic_mult = i + 1  # 1, 2, 3, 4
    wave += amp * sin(phases * harmonic_mult)
```

| Harmonic | Multiple | Amplitude | Example (440Hz) |
|----------|----------|-----------|-----------------|
| 1st (Fundamental) | 1× | 100% | 440 Hz |
| 2nd | 2× | 50% | 880 Hz |
| 3rd | 3× | 25% | 1320 Hz |
| 4th | 4× | 12.5% | 1760 Hz |

### Vibrato

Frequency modulation using a Low Frequency Oscillator (LFO):

```python
vibrato_rate = 5.0  # Hz (oscillations per second)
vibrato_depth = 0.001 to 0.021  # Controlled by pinch gesture

# LFO generates sine wave
lfo = sin(lfo_phases)

# Modulate frequency
freq_modulation = 1.0 + (vibrato_depth * lfo)
instantaneous_freq = frequency * freq_modulation
```

### Reverb (Delay Effect)

Circular buffer stores audio and plays it back with delay:

```python
delay_seconds = 0.1 to 0.8  # Controlled by left hand Y
delay_feedback = 0.4        # Echo intensity (40%)
delay_mix = 0.3             # Wet/dry mix (30%)

# Read delayed signal from buffer
delayed_signal = delay_buffer[indices]

# Mix dry and wet signals
output = dry_signal + delayed_signal * delay_mix

# Feedback for echo repetition
feedback = dry_signal + delayed_signal * delay_feedback
delay_buffer[indices] = feedback
```

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
# Smooth volume curve with zone limit
if left_hand_x <= LEFT_ZONE_LIMIT:
    mapped_x = left_hand_x / LEFT_ZONE_LIMIT
else:
    mapped_x = 1.0
volume = mapped_x ** 1.5
```

### Vibrato Calculation

```python
# Normalize pinch to vibrato depth
norm_pinch = (pinch - PINCH_MIN) / (PINCH_MAX - PINCH_MIN)
norm_pinch = clamp(norm_pinch, 0.0, 1.0)
vibrato_depth = VIBRATO_MIN + (norm_pinch * VIBRATO_MAX)
```

### Reverb Calculation

```python
# Normalize Y position to delay time
normalized_y = (left_y - REVERB_TOP) / (REVERB_BOTTOM - REVERB_TOP)
normalized_y = clamp(normalized_y, 0.0, 1.0)
delay_seconds = DELAY_MAX - (normalized_y * (DELAY_MAX - DELAY_MIN))
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

## Technical Specifications

- **Latency**: < 50ms
- **Precision**: 32-bit float
- **Thread-safe**: Yes (with locks)
- **Smoothing**: Automatic (frequency: 5 samples, volume: 3 samples)
- **Frequency Range**: 200-2000 Hz (configurable)
- **Vibrato Rate**: 5.0 Hz (fixed LFO frequency)
- **Vibrato Depth**: 0.001-0.021 (gesture controlled)
- **Reverb Delay**: 0.1-0.8 seconds (gesture controlled)
- **Reverb Feedback**: 0.4 (40%)
- **Reverb Mix**: 0.3 (30%)
- **Harmonics**: [1.0, 0.5, 0.25, 0.125] (configurable)

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

### Vibrato sounds choppy

- Check pinch detection is working correctly
- Ensure smooth hand movements

### Reverb creates artifacts

- Reduce `delay_feedback` value
- Check buffer size is adequate for delay time

---

For complete implementation details, see source code in `audio_module/theremin_synthesizer.py`
