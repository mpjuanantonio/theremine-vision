# Video Module Documentation

## Overview

The video module provides real-time hand tracking using MediaPipe, detecting 21 reference points (landmarks) per hand and calculating normalized positions.

## Components

### handPositionCalculator.py

Main class implementing:
- Hand position calculation using 6 key points
- Normalization to 0.0-1.0 values
- Separate handling for left and right hands
- Automatic reset when hands are not detected

### vision_stream.py

Visualization program displaying:
- Real-time hand tracking
- FPS and processing time
- Hand X, Y positions
- Video recording capability

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

### Position Mapping

#### Right Hand (Y-Axis) → Pitch

```
Normalized Y: 0.0 (top) → 1.0 (bottom)
Hand at top = High notes
Hand at bottom = Low notes
```

#### Left Hand (X-Axis) → Volume

```
Normalized X: 0.0 (left) → 1.0 (right)
Hand at left = Silence
Hand at right = Maximum volume
```

## Programmatic Usage

```python
from handPositionCalculator import HandPositionCalculator
import mediapipe as mp

# Initialize
calculator = HandPositionCalculator(frame_width=1440, frame_height=810)

# In detection loop
for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
    hand_label = results.multi_handedness[hand_idx].classification[0].label
    calculator.update_hand_position(hand_landmarks, hand_label)

# Get values
right_y = calculator.get_right_hand_y()  # float: 0.0-1.0 or None
left_x = calculator.get_left_hand_x()    # float: 0.0-1.0 or None

# Reset when no hands detected
calculator.reset()
```

## HandPositionCalculator API

### Methods

#### `__init__(frame_width, frame_height)`

Initializes calculator with frame dimensions.

```python
calc = HandPositionCalculator(1440, 810)
```

#### `update_hand_position(hand_landmarks, hand_label)`

Updates position based on MediaPipe landmarks.

```python
calc.update_hand_position(hand_landmarks, 'Right')
calc.update_hand_position(hand_landmarks, 'Left')
```

#### `get_right_hand_y()` → float | None

Returns normalized Y position of right hand.

```python
y = calc.get_right_hand_y()  # 0.0-1.0 or None
```

#### `get_left_hand_x()` → float | None

Returns normalized X position of left hand.

```python
x = calc.get_left_hand_x()   # 0.0-1.0 or None
```

#### `reset()`

Resets both positions to None.

```python
calc.reset()
```

## Visualization

### On-Screen Display

```
┌─────────────────────────────────────┐
│ FPS: XX                             │
│ Time: XX.Xms                        │
│ Right Hand Y: 0.XXXX (magenta)      │
│ Left Hand X: 0.XXXX (cyan)          │
│                                     │
│ [Hand landmarks drawn on frame]     │
└─────────────────────────────────────┘
```

### Display Colors

- **Magenta** (230, 66, 245): Right hand and Y-axis
- **Cyan** (66, 245, 230): Left hand and X-axis
- **Green** (0, 255, 0): Hand labels
- **White**: Landmark points

## Technical Specifications

- **Framework**: MediaPipe Hands
- **Landmarks**: 21 per hand
- **Precision**: 0.0001 in normalized positions
- **FPS**: 30-60 (hardware dependent)
- **Latency**: ~33ms at 30 FPS

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

### Unstable hand detection

- Already uses 6-point averaging
- Increase minimum confidence in MediaPipe
- Improve frontal lighting

### Oscillating values

- Normal for points near frame edges
- Smoothed in audio module with averages
- Can be improved with additional Kalman filter

---

For complete implementation details, see source code in handPositionCalculator.py
