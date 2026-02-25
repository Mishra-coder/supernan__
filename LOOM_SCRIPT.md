# 🎬 Loom Video Script - Kannada to Hindi Dubbing Pipeline

## **[0:00 - 0:30] Opening**

**[Screen: GitHub repo]**

> "Hi everyone! Aaj main apna AI Video Dubbing Pipeline demonstrate karunga. 
> Yeh pipeline **Kannada videos ko automatically Hindi mein dub karta hai** - 
> voice cloning aur lip-sync ke saath. 
> 
> Yeh especially useful hai South Indian content ko North Indian audience tak pahunchane ke liye. 
> Chaliye dekhte hain kaise kaam karta hai."

---

## **[0:30 - 1:30] Project Overview**

**[Screen: VS Code - folder structure]**

> "Yeh hai mera project structure. Main files hain:
> 
> - **dub_video.py** - Main pipeline orchestrator
> - **config.yaml** - Configuration file
> - **src/pipeline/** - 5 modules jo step-by-step processing karte hain
> 
> Chaliye config file dekhte hain..."

**[Open config.yaml]**

> "Config mein dekho:
> - **source_language: kn** - Kannada input
> - **target_language: hi** - Hindi output
> - Input video path aur output directory
> - Models ke names - WhisperX for transcription, GROQ for translation, Coqui TTS for voice cloning"

---

## **[1:30 - 3:00] Pipeline Architecture**

**[Screen: dub_video.py - imports section]**

> "Ab pipeline explain karta hoon. Yeh 5 steps hain:
> 
> **Step 1: AudioExtractor** - Video se audio nikalta hai aur Demucs use karke vocals isolate karta hai. 
> Background music aur noise remove ho jata hai.
> 
> **Step 2: Transcriber** - WhisperX use karke Kannada audio ko text mein convert karta hai. 
> Timestamps bhi save hote hain har word ke liye.
> 
> **Step 3: TextTranslator** - GROQ API use karke Kannada text ko Hindi mein translate karta hai. 
> Context-aware translation hoti hai.
> 
> **Step 4: VoiceCloner** - Coqui TTS use karke Hindi audio generate karta hai. 
> Original speaker ki voice clone hoti hai.
> 
> **Step 5: LipSyncer** - VideoReTalking use karke lip movements ko Hindi audio se sync karta hai."

**[Scroll to main function]**

> "Main function mein dekho - sabhi modules initialize hote hain, 
> phir process_segment function mein ek-ek karke execute hote hain. 
> Simple aur clean pipeline flow."

---

## **[3:00 - 4:00] Key Code - Transcriber & Translator**

**[Screen: transcriber.py]**

> "Pehle Transcriber dekhte hain. 
> 
> Line 14 mein dekho - **language='kn'** specify kiya hai for Kannada.
> 
> WhisperX model Kannada audio ko accurately transcribe karta hai with timestamps."

**[Screen: translator.py]**

> "Ab Translator. Yeh sabse important part hai.
> 
> Line 30 mein dekho - GROQ API ko prompt diya hai:
> 'You are an expert Kannada to Hindi translator'
> 
> Har segment individually translate hota hai context ke saath.
> 
> Line 45 mein - Agar translation fail ho toh error handling hai."

---

## **[4:00 - 5:00] Live Demo**

**[Screen: Google Colab]**

> "Ab live demo dekhte hain. Main Google Colab use kar raha hoon.
> 
> Important note: TTS library Python 3.12 support nahi karti, 
> isliye maine Python 3.11 environment setup kiya using Conda.
> 
> Ab main pipeline run karta hoon..."

**[Run command]**

```python
!mamba run -n py311 python dub_video.py --config config.yaml
```

> "Processing start ho gayi. Yeh 15-20 minutes lega:
> - Audio extraction
> - Kannada transcription
> - Kannada to Hindi translation
> - Voice cloning with Hindi text
> - Lip-sync generation"

**[Show output]**

> "Yeh hai final output. 
> 
> **Original:** Kannada audio with original lip movements
> 
> **Dubbed:** Hindi audio with synced lip movements
> 
> Dekho - voice quality maintain hai aur lips perfectly sync hain!"

---

## **[5:00 - 5:30] Closing**

**[Screen: GitHub repo]**

> "Toh yeh tha mera Kannada to Hindi AI Dubbing Pipeline. 
> 
> Key features:
> - Automatic transcription aur translation
> - Voice cloning - original speaker ki voice maintain hoti hai
> - Lip-sync - mouth movements match hoti hain
> - Scalable - batches mein process kar sakte ho
> 
> Saara code GitHub pe available hai. 
> Future mein main more Indian languages add karunga - Tamil, Telugu, Malayalam.
> 
> Thank you for watching!"

---

## 📋 Files to Show (In Order)

1. ✅ GitHub repo (5 sec)
2. ✅ Folder structure (10 sec)
3. ✅ `config.yaml` - show source_language: kn, target_language: hi (20 sec)
4. ✅ `dub_video.py` - imports and main function (40 sec)
5. ✅ `transcriber.py` - language='kn' parameter (20 sec)
6. ✅ `translator.py` - GROQ prompt for Kannada to Hindi (30 sec)
7. ✅ Google Colab - running command (30 sec)
8. ✅ Output comparison - Original Kannada vs Dubbed Hindi (30 sec)

---

## 🎯 Key Points to Say

1. **"Kannada to Hindi dubbing - South to North content bridge"**
2. **"5-step pipeline: Extract → Transcribe → Translate → Clone → Sync"**
3. **"WhisperX for Kannada transcription with timestamps"**
4. **"GROQ API for context-aware Kannada-Hindi translation"**
5. **"Voice cloning maintains original speaker's voice quality"**
6. **"Python 3.11 required for TTS library compatibility"**

---

## ⚡ Quick Tips

- Speak clearly and confidently
- Pause 2-3 seconds when switching screens
- Show code for 5 seconds before explaining
- Keep energy high throughout
- Smile when talking!

Total Duration: 5-6 minutes
