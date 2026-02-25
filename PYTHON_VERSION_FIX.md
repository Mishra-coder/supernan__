# TTS Installation Error Fix

## Problem
```
ERROR: Could not find a version that satisfies the requirement TTS
ERROR: No matching distribution found for TTS
```

## Root Cause
Coqui TTS library Python 3.12 ko support nahi karti. Ye Python 3.9, 3.10, ya 3.11 chahiye.

## Check Your Python Version
```python
import sys
print(sys.version)
```

---

## Solutions

### Solution 1: Conda Environment (Best for Colab)

```python
# Step 1: Install condacolab
!pip install -q condacolab
import condacolab
condacolab.install_mambaforge()
# Runtime will restart automatically

# Step 2: Create Python 3.11 environment
!mamba create -n py311 python=3.11 -y

# Step 3: Install requirements
!mamba run -n py311 pip install -r requirements.txt

# Step 4: Run your script
!mamba run -n py311 python dub_video.py --config config.yaml
```

### Solution 2: Manual Python 3.11 Install

```bash
# Install Python 3.11
!sudo apt-get update -y
!sudo apt-get install -y python3.11 python3.11-venv python3.11-dev

# Create virtual environment
!python3.11 -m venv /content/py311env

# Install dependencies
!/content/py311env/bin/pip install -r requirements.txt

# Run script
!/content/py311env/bin/python dub_video.py --config config.yaml
```

### Solution 3: Use Different Colab Runtime

1. Runtime > Disconnect and delete runtime
2. Runtime > Change runtime type
3. Try different GPU (sometimes different GPUs have different Python versions)

---

## Verification

After installation, verify TTS is working:

```python
# If using conda
!mamba run -n py311 python -c "from TTS.api import TTS; print('✅ TTS imported successfully!')"

# If using venv
!/content/py311env/bin/python -c "from TTS.api import TTS; print('✅ TTS imported successfully!')"
```

---

## Alternative: Use Different TTS Library

Agar upar ke solutions kaam nahi kar rahe, toh TTS ki jagah alternative use kar sakte ho:

```python
# Install gTTS (simpler but less features)
!pip install gtts

# Or use pyttsx3 (offline)
!pip install pyttsx3
```

Lekin note karo: Ye alternatives voice cloning support nahi karte, sirf basic text-to-speech dete hain.
