# Google Colab Par Kaise Run Karein

## ⚠️ IMPORTANT: Python Version Issue

**Problem:** TTS library Python 3.12 support nahi karti (requires Python 3.9-3.11)  
**Solution:** Neeche diye gaye steps follow karo

---

## Quick Start (Agar Python 3.10/3.11 hai)

Agar tumhara Colab Python 3.10 ya 3.11 use kar raha hai, seedha Step 1 se shuru karo.

## Python 3.12 Fix (Agar error aa raha hai)

Agar `ERROR: Could not find a version that satisfies the requirement TTS` aa raha hai, toh yeh karo:

### Option A: Conda Environment (Recommended)
```python
# Cell 1: Conda install karo
!pip install -q condacolab
import condacolab
condacolab.install_mambaforge()
# ⚠️ Runtime restart hoga, phir neeche wale cells run karo

# Cell 2: Python 3.11 environment banao
!mamba create -n py311 python=3.11 -y

# Cell 3: Dependencies install karo
!mamba run -n py311 pip install -r requirements.txt

# Baaki saare cells mein !python ki jagah !mamba run -n py311 python use karo
```

### Option B: Manual Python 3.11 Install
```python
!sudo apt-get update -y
!sudo apt-get install -y python3.11 python3.11-venv python3.11-dev
!python3.11 -m venv /content/py311
!/content/py311/bin/pip install -r requirements.txt

# Baaki cells mein !/content/py311/bin/python use karo
```

---

## Step 1: GitHub Par Upload Karo
```bash
cd supernan_dubbing_pipeline
git add .
git commit -m "Complete dubbing pipeline"
git push origin main
```

## Step 2: Google Colab Open Karo
1. https://colab.research.google.com par jao
2. File > Upload notebook
3. `RUN_ON_COLAB.ipynb` upload karo

## Step 3: GPU Enable Karo
1. Runtime > Change runtime type
2. Hardware accelerator > T4 GPU
3. Save

## Step 4: Cells Run Karo (Order Mein)

### Cell 1: GPU Check
```python
!nvidia-smi
!apt-get update && apt-get install -y ffmpeg
```

### Cell 2: Repo Clone
```python
!git clone https://github.com/YOUR_USERNAME/supernan_dubbing_pipeline.git
%cd supernan_dubbing_pipeline
```
**Note:** Apna GitHub username daal do

### Cell 3: Dependencies Install
```python
# Pehle Python version check karo
import sys
print(f"Python version: {sys.version}")

if sys.version_info >= (3, 12):
    print("⚠️ Python 3.12 detected! See 'Python 3.12 Fix' section above")
else:
    !pip install -q -r requirements.txt
    print("✅ Installation complete!")
```
**Note:** Agar error aaye toh upar "Python 3.12 Fix" section dekho

### Cell 4: Video Download
```python
!pip install -q gdown
!gdown 1urRXU3HGjL30lXxQakqK_5rVjbH9XW3O -O data/input/supernan_training.mp4
!ls -lh data/input/
```

### Cell 5: VideoReTalking Setup
```python
!git clone https://github.com/OpenTalker/video-retalking.git
%cd video-retalking
!pip install -q -r requirements.txt
!mkdir -p checkpoints
%cd checkpoints
```

### Cell 6: Models Download
```python
!wget -q https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth
!wget -q https://github.com/xinntao/facexlib/releases/download/v0.2.2/parsing_parsenet.pth
!wget -q https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth
!wget -q https://github.com/Rudrabha/Wav2Lip/releases/download/v1.0/wav2lip.pth
!wget -q https://github.com/OpenTalker/video-retalking/releases/download/v0.0.1/DNet.pt
!wget -q https://github.com/OpenTalker/video-retalking/releases/download/v0.0.1/ENet.pth
!wget -q https://github.com/OpenTalker/video-retalking/releases/download/v0.0.1/LNet.pth
!ls -lh
%cd ../..
```

### Cell 7: API Key Set Karo
```python
import os
os.environ['GROQ_API_KEY'] = 'YOUR_KEY_HERE'
```
**Note:** https://console.groq.com se free API key lo

### Cell 8: Pipeline Run Karo
```python
!python dub_video.py --config config.yaml
# Agar Python 3.11 environment use kar rahe ho:
# !mamba run -n py311 python dub_video.py --config config.yaml
# Ya: !/content/py311/bin/python dub_video.py --config config.yaml
```
**Time:** 15-20 minutes lagenge

### Cell 9: Output Check Karo
```python
!ls -lh data/output/
```
**Dekho:** `supernan_hindi_dub_15s.mp4` file bani hai ya nahi

### Cell 10: Video Play Karo
```python
from IPython.display import Video
Video('data/output/supernan_hindi_dub_15s.mp4', width=640)
```

### Cell 11: Video Download Karo
```python
from google.colab import files
files.download('data/output/supernan_hindi_dub_15s.mp4')
```

## Output Kahan Milega?

**Colab Mein:**
- Path: `data/output/supernan_hindi_dub_15s.mp4`
- Cell 10 se directly play kar sakte ho
- Cell 11 se download kar sakte ho

**Local Machine Par:**
- Cell 11 run karne ke baad browser automatically download karega

## Agar Error Aaye?

### Out of Memory
```python
import torch
torch.cuda.empty_cache()
```
Phir Cell 8 dobara run karo

### FFmpeg Not Found
Cell 1 dobara run karo

### GROQ API Error
- API key check karo
- https://console.groq.com par quota check karo

### VideoReTalking Error
- Cell 5 aur 6 dobara run karo
- Sab models download hue hain check karo

## Total Time
- Setup (Cell 1-7): 10 minutes
- Pipeline (Cell 8): 20 minutes
- Total: 30 minutes

## Success Check
Agar ye sab dikhe to success:
1. Cell 9 mein `supernan_hindi_dub_15s.mp4` file dikhe
2. Cell 10 mein video play ho
3. File size ~5-10 MB ho
4. Duration exactly 15 seconds ho
