# Video Module Documentation

## Overview

The video module provides real-time hand tracking using MediaPipe, detecting 21 reference points (landmarks) per hand and calculating normalized positions. It also detects pinch gestures for vibrato control and waveform switching.

## Components

### video_processor.py

Main class encapsulating video capture and hand tracking:
- Video capture initialization with configurable resolution
- MediaPipe Hands integration
- Frame processing and hand detection
- FPS calculation
- Automatic fullscreen resolution detection

### handPositionCalculator.py

Position and gesture calculation class:
- Hand position calculation using 6 key points
- **Pinch gesture detection** for vibrato control with right hand
- **"Ok gesture" detection** for toggle the waveform type with left hand
- Normalization to 0.0-1.0 values
- Separate handling for left and right hands
- Automatic reset when hands are not detected

## Hand Tracking Operation

### MediaPipe Landmarks

MediaPipe detects **21 landmarks per hand**:
- **Wrist** (landmark 0)
- **Thumb** (landmarks 1-4)
- **Index finger** (landmarks 5-8)
- **Middle finger** (landmarks 9-12)
- **Ring finger** (landmarks 13-16)
- **Pinky** (landmarks 17-20)

### Position Averaging Method

Instead of using a single point, **6 key points** are averaged:

```
0:  Wrist (WRIST)
4:  Thumb tip (THUMB_TIP)
8:  Index finger tip (INDEX_FINGER_TIP)
12: Middle finger tip (MIDDLE_FINGER_TIP)
16: Ring finger tip (RING_FINGER_TIP)
20: Pinky tip (PINKY_TIP)
```

**Formula:**
```python
avg_x = (x₀ + x₄ + x₈ + x₁₂ + x₁₆ + x₂₀) / 6
avg_y = (y₀ + y₄ + y₈ + y₁₂ + y₁₆ + y₂₀) / 6
```

**Advantages:**
- Greater stability (reduced jitter)
- Improved accuracy
- More robust to occlusions
- Better control for user

### Pinch Gesture Detection

For vibrato control, the system detects the distance between thumb and index finger:

```python
# Landmarks used for pinch detection
THUMB_TIP = 4
INDEX_FINGER_TIP = 8

# Calculate Euclidean distance
dx = thumb_x - index_x
dy = thumb_y - index_y
pinch_distance = sqrt(dx² + dy²)
```

**Pinch Mapping:**
```
Distance: 0.02 (fingers together) → Minimal vibrato
Distance: 0.15 (fingers apart)    → Maximum vibrato
```

### Left Hand Pinch Gesture (Waveform Toggle)

The left hand pinch gesture is used to cycle through waveform types:

```python
# Same landmarks as right hand pinch
THUMB_TIP = 4
INDEX_FINGER_TIP = 8

# Pinch threshold for activation
PINCH_THRESHOLD = 0.05  # Fingers must be very close
```

**Waveform Cycle:**
```
Pinch detected → Toggle to next waveform:
sine → square → saw → triangle → sine → ...
```

**Debounce:** The system includes a cooldown to prevent multiple toggles from a single pinch gesture.

### Position Mapping

#### Right Hand → Pitch & Vibrato

**Y-Axis → Pitch:**
```
Normalized Y: 0.0 (top) → 1.0 (bottom)
Hand at top = High notes
Hand at bottom = Low notes
```

**Pinch → Vibrato:**
```
Pinch distance controls vibrato depth
Fingers together = No vibrato
Fingers apart = Maximum vibrato
```

#### Left Hand → Volume, Reverb & Waveform

**X-Axis → Volume:**
```
Normalized X: 0.0 (left) → 0.5 (center)
Hand at left = Silence
Hand at center = Maximum volume
(Right half of screen ignored for volume)
```

**Y-Axis → Reverb:**
```
Normalized Y: 0.30 (top zone) → 0.85 (bottom zone)
Hand at top = Maximum reverb (0.8s delay)
Hand at bottom = Minimum reverb (0.1s delay)
```

**Pinch → Waveform Toggle:**
```
Pinch gesture (thumb + index together) = Cycle waveform
sine → square → saw → triangle → sine
```



## Technical Specifications

- **Framework**: MediaPipe Hands
- **Landmarks**: 21 per hand
- **Precision**: 0.0001 in normalized positions
- **FPS**: 30-60 (hardware dependent)
- **Latency**: ~33ms at 30 FPS
- **Pinch Detection**: Thumb-Index distance (landmarks 4 and 8)
- **Position Averaging**: 6-point method for stability
- **Screen Detection**: Automatic via tkinter

## Fullscreen Resolution

The system automatically detects screen resolution using tkinter:

```python
import tkinter as tk

def get_screen_resolution():
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    return width, height
```

## Limitations

- Requires good lighting conditions
- Works best with fully visible hands
- Maximum 2 hands detected simultaneously
- Requires functional camera

## Troubleshooting

### Hands not detected

- Improve lighting conditions
- Keep hands within frame
- Use contrasting background
- You can also change variables at `video_procesor.py` -> `min_detection_confidence` and `min_tracking_confidence` for find your better config.

### Unstable hand detection

- Already uses 6-point averaging
- Increase minimum confidence in MediaPipe
- Improve frontal lighting

### Oscillating values

- Normal for points near frame edges
- Smoothed in audio module with averages

### Pinch detection unreliable

- Ensure good lighting on hands
- Keep fingers visible to camera
- Adjust PINCH_MIN/PINCH_MAX thresholds if needed

---

For complete implementation details, see source code in `video_module/handPositionCalculator.py` and `video_module/video_processor.py`
