# Installation Guide

## System Requirements

### Operating System
- Linux (Ubuntu 22.04 or later recommended)
- Other Linux distributions compatible with apt-get

### Python Version
| Version | Status | Recommendation |
|---------|--------|-----------------|
| Python 3.10 | Supported | Works |
| **Python 3.11** | **Recommended** | **Use this** |
| Python 3.12 | Supported | Works |

### Hardware
- Functional webcam
- Audio output device (speakers)
- Microphone not required

---

## Quick Installation (5 minutes)

### Option 1: Automated Script (Recommended)

```bash
# Clone repository
git clone https://github.com/mpjuanantonio/theremine-vision.git
cd theremine-vision

# Run installation script
bash setup.sh
```

### Option 2: Manual Commands

```bash
# 1. Install system dependencies
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv python3.11-dev portaudio19-dev python3-tk

# 2. Clone repository
git clone https://github.com/mpjuanantonio/theremine-vision.git
cd theremine-vision

# 3. Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# 4. Install Python dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# 5. Verify installation
python -c "import cv2, numpy, mediapipe, pyaudio; print('Installation successful')"

# 6. Run!
python main_module/theremin_main.py
```

---

## Step-by-Step Installation

### Step 1: Verify Python Version

```bash
python3 --version
# Should display 3.10.x, 3.11.x or 3.12.x
```

If you do not have Python 3.11 installed:

```bash
sudo apt-get install python3.11
```

### Step 2: Install System Dependencies

Required for PyAudio compilation and screen detection:

```bash
sudo apt-get update
sudo apt-get install python3.11-dev python3.11-venv portaudio19-dev python3-tk
```

**What gets installed:**
- `python3.11-dev`: Python headers for compiling extensions
- `python3.11-venv`: Virtual environment tool
- `portaudio19-dev`: Audio libraries for PyAudio
- `python3-tk`: Tkinter for screen resolution detection

### Step 3: Clone Repository

```bash
git clone https://github.com/mpjuanantonio/theremine-vision.git
cd theremine-vision
```

### Step 4: Create Virtual Environment

```bash
# Create
python3.11 -m venv .venv

# Activate
source .venv/bin/activate
```

**Verify activation**: Your prompt should show `(.venv)` at the beginning.

```bash
# Example:
(.venv) user@computer:~/theremine-vision$
```

### Step 5: Install Python Dependencies

```bash
# Update tools
pip install --upgrade pip setuptools wheel

# Install project dependencies
pip install -r requirements.txt
```

**Dependencies that will be installed:**
- `opencv-python`: Video capture and processing
- `numpy`: Numerical computations
- `mediapipe`: Hand detection and tracking
- `pyaudio`: Real-time audio synthesis

**Note**: `tkinter` is installed via system package (`python3-tk`), not pip.

### Step 6: Verify Installation

```bash
python -c "import cv2, numpy, mediapipe, pyaudio; print('All libraries installed successfully')"
```

If you see "All libraries installed successfully", you are ready to go!

---

## Activate/Deactivate Virtual Environment

### Activate (required each time you open a new terminal)

```bash
cd ~/theremine-vision
source .venv/bin/activate
```

**Indicator**: Your prompt should show `(.venv)` at the beginning.

### Deactivate (when finished)

```bash
deactivate
```

---

## Installation Troubleshooting

### Error: `Python.h: No such file or directory`

**Cause**: Python headers are missing

**Solution**:
```bash
sudo apt-get install python3.11-dev
```

### Error: `portaudio.h: No such file or directory`

**Cause**: PortAudio libraries are missing

**Solution**:
```bash
sudo apt-get install portaudio19-dev
```

### Error: `No module named 'cv2'` or similar

**Cause**: Virtual environment not activated or dependencies not installed

**Solution**:
```bash
# Verify activation
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Error: `command not found: python3.11`

**Cause**: Python 3.11 not installed

**Solution**:
```bash
sudo apt-get install python3.11
```

### Error: "Permission denied" when running setup.sh

**Cause**: Script is not executable

**Solution**:
```bash
chmod +x setup.sh
bash setup.sh
```

### PyAudio compilation fails

**Cause**: Missing development tools

**Solution**:
```bash
sudo apt-get install build-essential python3.11-dev portaudio19-dev
pip install --no-cache-dir pyaudio
```

### Error: `No module named 'tkinter'`

**Cause**: Tkinter not installed (needed for fullscreen detection)

**Solution**:
```bash
sudo apt-get install python3-tk
```

---

## System Verification

Before running the application, verify:

```bash
# 1. Correct Python version
python --version

# 2. Virtual environment activated
echo $VIRTUAL_ENV

# 3. Libraries installed
pip list | grep -E "opencv|numpy|mediapipe|pyaudio"

# 4. Camera available
ls -la /dev/video*

# 5. Audio functional
python -c "import pyaudio; print('Audio functional')"
```

---

## Complete Uninstallation

If you need to start fresh:

```bash
# Remove virtual environment
rm -rf .venv

# Remove Python cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null

# Reinstall
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Clean Project Reinstallation

```bash
# Go to parent directory
cd ~

# Remove previous installation
rm -rf theremine-vision

# Clone again
git clone https://github.com/mpjuanantonio/theremine-vision.git
cd theremine-vision

# Install
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Additional Troubleshooting

### Application runs but camera not detected

```bash
# Check available cameras
ls -la /dev/video*

# Try another camera if available
python main_module/theremin_main.py --source 1
```

### No audio output

```bash
# Verify audio
python -c "import pyaudio; print(pyaudio.PyAudio().get_device_count())"

# Check system volume
alsamixer
```

### Unstable or choppy values

- Improve camera lighting
- Close other CPU-intensive applications
- Increase buffer_size in configuration

### Fullscreen not working

```bash
# Verify tkinter is installed
python -c "import tkinter; print('Tkinter OK')"

# Run with custom resolution if needed
python main_module/theremin_main.py --width 1280 --height 720
```

---

## Next Steps

1. Installation completed
2. Read [README.md](../README.md) for usage instructions
3. Run `python main_module/theremin_main.py`
4. Consult [docs/](../docs/) for additional documentation

---

**Need help?** Consult the Troubleshooting section above or review the other documents in the `docs/` folder.
