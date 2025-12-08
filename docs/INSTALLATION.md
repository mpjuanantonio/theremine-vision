# Installation Guide

## Table of Contents

- [System Requirements](#system-requirements)
- [Quick installation](#quick-installation)
  - [Linux Installation](#linux-installation)
  - [Windows Installation](#windows-installation)
- [Step-by-Step Installation (Linux)](#step-by-step-installation-linux)
- [Step-by-Step Installation (Windows)](#step-by-step-installation-windows)
- [Activate Virtual Environment](#activate-virtual-environment)
- [Deactivate Virtual Environment](#deactivate-virtual-environment)
- [Installation Troubleshooting](#installation-troubleshooting)
- [System Verification](#system-verification)
- [Complete Uninstallation](#complete-uninstallation)
- [Clean Project Reinstallation](#clean-project-reinstallation)
- [Additional Troubleshooting](#additional-troubleshooting)
- [Next Steps](#next-steps)

---

## System Requirements

### Operating System
- **Linux**: Ubuntu 22.04 or later recommended (other distributions compatible with apt-get)
- **Windows**: Windows 10/11

### Python Version
| Version | Status | Recommendation |
|---------|--------|-----------------|
| Python 3.10 | Supported | Works |
| **Python 3.11** | **Recommended** | **Use this** |
| Python 3.12 | Supported | Works |

### Hardware
- Functional webcam
- Audio output device (speakers)
- Microphone NOT required

---

## Quick Installation

### Linux Installation

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

### Windows Installation

#### Quick Installation (5 minutes)

```cmd
REM 1. Clone repository
git clone https://github.com/mpjuanantonio/theremine-vision.git
cd theremine-vision

REM 2. Create virtual environment
python -m venv .venv

REM 3. Install dependencies
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

REM 4. Run the program
.\.venv\Scripts\python.exe main_module/theremin_main.py
```

**Note for Windows**: System dependencies like PortAudio are included in the PyAudio wheel package, so no additional system installations are required.

---

## Step-by-Step Installation (Linux)

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

### Step 7: Run the Program

```bash
python main_module/theremin_main.py
```

---

## Step-by-Step Installation (Windows)

### Step 1: Verify Python Version

Open Command Prompt (cmd) or PowerShell and check:

```cmd
python --version
REM Should display 3.10.x, 3.11.x or 3.12.x
```

If Python is not installed, download and install it from [python.org](https://www.python.org/downloads/).

### Step 2: Clone Repository

```cmd
git clone https://github.com/mpjuanantonio/theremine-vision.git
cd theremine-vision
```

### Step 3: Create Virtual Environment

```cmd
python -m venv .venv
```

### Step 4: Install Python Dependencies

```cmd
.\.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**Dependencies that will be installed:**

- `opencv-python`: Video capture and processing
- `numpy`: Numerical computations
- `mediapipe`: Hand detection and tracking
- `pyaudio`: Real-time audio synthesis (includes PortAudio binaries)

### Step 5: Verify Installation

```cmd
.\.venv\Scripts\python.exe -c "import cv2, numpy, mediapipe, pyaudio; print('All libraries installed successfully')"
```

If you see "All libraries installed successfully", you are ready to go!

### Step 6: Run the Program

```cmd
.\.venv\Scripts\python.exe main_module\theremin_main.py
```

---

## Activate Virtual Environment

### Linux

```bash
cd ~/theremine-vision
source .venv/bin/activate
```

**Indicator**: Your prompt should show `(.venv)` at the beginning.

### Windows

```cmd
cd theremine-vision
.\.venv\Scripts\activate.bat
```

**Indicator**: Your prompt should show `(.venv)` at the beginning.

---

## Deactivate Virtual Environment

```bash
deactivate
```

This works on both Linux and Windows.

---

## Installation Troubleshooting

### Linux-specific Issues

#### Error: `Python.h: No such file or directory`

**Cause**: Python headers are missing

**Solution**:
```bash
sudo apt-get install python3.11-dev
```

#### Error: `portaudio.h: No such file or directory`

**Cause**: PortAudio libraries are missing

**Solution**:
```bash
sudo apt-get install portaudio19-dev
```

#### Error: `command not found: python3.11`

**Cause**: Python 3.11 not installed

**Solution**:
```bash
sudo apt-get install python3.11
```

#### Error: `No module named 'tkinter'`

**Cause**: Tkinter not installed (needed for fullscreen detection)

**Solution**:
```bash
sudo apt-get install python3-tk
```

### Windows-specific Issues

#### Error: `python: command not found`

**Cause**: Python not added to PATH during installation

**Solution**: Reinstall Python and check "Add Python to PATH" option, or add it manually to system environment variables.

#### Error: PyAudio installation fails

**Cause**: Missing Visual C++ compiler (rare, as wheels are pre-built)

**Solution**: Install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) or try installing a pre-built wheel:
```cmd
pip install pipwin
pipwin install pyaudio
```

### Common Issues (All Platforms)

#### Error: `No module named 'cv2'` or similar

**Cause**: Virtual environment not activated or dependencies not installed

**Solution**:

**Linux:**
```bash
# Verify activation
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Windows:**
```cmd
REM Verify activation
.\.venv\Scripts\activate.bat

REM Reinstall dependencies
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## System Verification

Before running the application, verify:

**Linux:**
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

**Windows:**
```cmd
REM 1. Correct Python version
python --version

REM 2. Virtual environment activated (check prompt for .venv)

REM 3. Libraries installed
.\.venv\Scripts\python.exe -m pip list | findstr "opencv numpy mediapipe pyaudio"

REM 4. Audio functional
.\.venv\Scripts\python.exe -c "import pyaudio; print('Audio functional')"
```

---

## Complete Uninstallation

If you need to start fresh:

**Linux:**
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

**Windows:**
```cmd
REM Remove virtual environment
rmdir /s /q .venv

REM Remove Python cache
for /d /r %i in (__pycache__) do @rmdir /s /q "%i" 2>nul
del /s /q *.pyc 2>nul

REM Reinstall
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## Clean Project Reinstallation

**Linux:**
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

**Windows:**
```cmd
REM Go to parent directory
cd ..

REM Remove previous installation
rmdir /s /q theremine-vision

REM Clone again
git clone https://github.com/mpjuanantonio/theremine-vision.git
cd theremine-vision

REM Install
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## Additional Troubleshooting

### Application runs but camera not detected

**Linux:**
```bash
# Check available cameras
ls -la /dev/video*

# Try another camera if available
python main_module/theremin_main.py --source 1
```

**Windows:**
```cmd
REM Try another camera if available
.\.venv\Scripts\python.exe main_module\theremin_main.py --source 1
```

### No audio output

**Linux:**
```bash
# Verify audio
python -c "import pyaudio; print(pyaudio.PyAudio().get_device_count())"

# Check system volume
alsamixer
```

**Windows:**
```cmd
REM Verify audio
.\.venv\Scripts\python.exe -c "import pyaudio; print(pyaudio.PyAudio().get_device_count())"

REM Check system volume in Windows settings
```

### Unstable or choppy values

- Improve camera lighting
- Close other CPU-intensive applications
- Increase buffer_size in configuration

### Fullscreen not working

**Linux:**
```bash
# Verify tkinter is installed
python -c "import tkinter; print('Tkinter OK')"

# Run with custom resolution if needed
python main_module/theremin_main.py --width 1280 --height 720
```

**Windows:**
```cmd
REM Tkinter is included with Python on Windows

REM Run with custom resolution if needed
.\.venv\Scripts\python.exe main_module\theremin_main.py --width 1280 --height 720
```

---

## Next Steps

1. Installation completed
2. Read [README.md](../README.md) for usage instructions
3. Run `python main_module/theremin_main.py`
4. Consult [docs/](../docs/) for additional documentation
