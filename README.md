# Supernan AI Dubbing Pipeline - The Golden 15 Seconds

This repository contains a professional-grade Python pipeline designed to take a 15-second English training video and produce a high-fidelity Hindi-dubbed version. 

Built with a focus on resourcefulness and quality over simple API calling.

## Submission Links
- **Output Video**: [Link to Google Drive / YouTube with 15-30s output]
- **Loom Walkthrough**: [Link to 5-min Loom explanatory video]

## The "Resourceful" Architecture
Instead of using a basic `Whisper -> Google Translate -> TTS -> Wav2Lip` chain, this pipeline uses specific, advanced open-source models to guarantee high fidelity:

1. **Vocal Isolation (Demucs)**: Before cloning the voice or transcribing, we isolate the vocals from background noise. XTTS voice cloning works significantly better with clean vocal references.
2. **Exact Timestamping (WhisperX)**: Standard Whisper hallucinates timestamps. We use `WhisperX` to get exact word-level audio timestamps so lip-syncing remains tight.
3. **Contextual Translation (Llama 3 via Groq)**: Instead of literal translations (Google Translate), we use Llama 3 to translate into natural, conversational Hindi fitting for a nanny context.
4. **Time-Stretching (PyDub)**: Hindi translations often take longer to speak than English. We dynamically compress/stretch the generated XTTS audio to perfectly match the original English utterance duration. **This prevents audio drift.**
5. **High-Fidelity Lip Syncing (VideoReTalking + GFPGAN)**: Wav2Lip blurs the face. We utilize VideoReTalking paired with GFPGAN face restoration to ensure the mouth remains sharp, natural, and expressive.

## 🛠 Setup & Execution (Google Colab Recommended)
Because models like XTTS and VideoReTalking require significant VRAM, this pipeline is intended to be run on **Google Colab (T4 Free Tier)**. 

### Local Setup
If you have a machine with an Nvidia GPU (min 16GB VRAM):
```bash
git clone https://github.com/Mishra-coder/supernan__.git
cd supernan__
pip install -r requirements.txt
# Requires installing Demucs, WhisperX, TTS, and VideoReTalking environments separately.
```

### Running the Pipeline
You can configure the specific start/end timestamps and models in `config.yaml`.
First, download the source video:
```bash
pip install gdown
mkdir -p data/input
gdown 1urRXU3HGjL30lXxQakqK_5rVjbH9XW3O -O data/input/supernan_training.mp4
```

Then execute the dubbing script:
```bash
export GROQ_API_KEY="your_api_key"
python dub_video.py --config config.yaml
```

## Cost Analysis at Scale
If scaling this to **500 hours** of video overnight on a budget:

**Estimated Cost Per Minute of Video:**
At scale using standard cloud GPU instances (e.g. RTX 4090/A6000 at ~$0.80/hour):
- Processing 1 minute of video takes ~3 minutes of GPU time.
- **Cost per minute of video** = ~$0.04 (approx. ₹3.30)

**Current Free/Open Source Setup:**
- Translation (Groq Free Tier): $0
- Transcription (WhisperX on Colab): $0
- Voice Cloning (XTTS on Colab): $0
- Lip Sync (VideoReTalking on Colab): $0
- **Total:** ₹0 

**Enterprise Scaling (500 Hours Overnight):**
To process 500 hours overnight, we cannot rely on a single Colab notebook. We need a cluster of GPUs.
- **Compute:** We would rent 10x RTX 4090 or A6000 instances on standard cloud providers (RunPod/Vast.ai) costing roughly $0.50 - $0.80 per hour per GPU. 
- **Time/Cost:** Processing 1 hour of video through this heavy pipeline takes ~3 hours of GPU time.
  - 500 hours video = 1500 hours GPU compute.
  - 1500 hours * $0.80 = **$1,200 total compute cost.**
  - At 10 GPUs running in parallel, it would take **6 days**, or we scale horizontally to **50 GPUs** to do it overnight (1500 / 50 = 30 hours).
- **Optimization for Scale**: To reduce this cost, I would drop VideoReTalking (which is extremely heavy) and switch to a TensorRT optimized version of Wav2Lip, slicing the compute time and cost by 70%.

## Known Limitations
- The VideoReTalking model is exceptionally slow on free-tier hardware.
- XTTS sometimes introduces slight artifacts if the isolated Demucs vocal track still contains heavy breathing.

## What I'd Improve With More Time
1. Implement a Gradio Web UI for easier timestamp selection and prompt engineering.
2. Add automated background noise re-mixing (after dubbing the voice, layer the original background music back over the video).
3. Dockerize the entire environment so users don't have to fiddle with `ffmpeg` and CUDA versions.
