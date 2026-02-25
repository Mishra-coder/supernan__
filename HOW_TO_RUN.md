# Google Colab Par Kaise Run Karein

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
!pip install -q -r requirements.txt
```

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
