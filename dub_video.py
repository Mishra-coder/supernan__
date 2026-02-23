import argparse
import os
import sys

# Append current dir to sys.path so we can import src modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.pipeline.audio_extractor import AudioExtractor
from src.pipeline.transcriber import Transcriber
from src.pipeline.translator import TextTranslator
from src.pipeline.voice_cloner import VoiceCloner
from src.pipeline.lip_syncer import LipSyncer

def main():
    parser = argparse.ArgumentParser(description="Supernan Hindi Dubbing Pipeline (15-sec chunk)")
    parser.add_argument("--config", type=str, default="config.yaml", help="Path to config.yaml")
    args = parser.parse_args()
    
    config_path = args.config
    if not os.path.exists(config_path):
        print(f"Error: Configuration file {config_path} not found.")
        return

    print("==============================================")
    print("  Supernan Hindi Dubbing Pipeline Initialized ")
    print("==============================================\n")

    # Step 1: Extract Audio & Isolate Vocals
    print("\n--- Phase 1: Audio Extraction & Vocal Isolation ---")
    extractor = AudioExtractor(config_path)
    audio_path = extractor.extract_audio_chunk()
    vocal_path = extractor.isolate_vocals()
    
    # Step 2: Transcribe (Word-Level)
    print("\n--- Phase 2: High-Precision Transcription (WhisperX) ---")
    transcriber = Transcriber(config_path)
    # Note: we transcribe the isolated vocals for better accuracy
    transcription_result = transcriber.transcribe_audio(vocal_path)
    
    # Step 3: Translate
    print("\n--- Phase 3: Context-Aware Hindi Translation (Groq/Llama3) ---")
    translator = TextTranslator(config_path)
    translator.translate_transcription(transcriber.transcription_path)
    
    # Step 4: Voice Cloning & Audio Synching
    print("\n--- Phase 4: Voice Cloning & Pacing Sync (XTTS v2) ---")
    cloner = VoiceCloner(config_path)
    final_audio_path = cloner.clone_and_sync_audio()
    
    # Step 5: Lip Syncing
    print("\n--- Phase 5: High-Fidelity Lip Sync (VideoReTalking / GFPGAN) ---")
    syncer = LipSyncer(config_path)
    final_video_path = syncer.generate_lip_sync()
    
    print("\n==============================================")
    print(f" PIPELINE COMPLETE! ")
    print(f" Output saved at: {final_video_path}")
    print("==============================================\n")

if __name__ == "__main__":
    main()
