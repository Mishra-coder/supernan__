import argparse
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.pipeline.audio_extractor import AudioExtractor
from src.pipeline.transcriber import Transcriber
from src.pipeline.translator import TextTranslator
from src.pipeline.voice_cloner import VoiceCloner
from src.pipeline.lip_syncer import LipSyncer

def process_segment(pipeline, start, end):
    print(f"\n--- Processing {start} to {end} ---")
    
    pipeline['extractor'].start_time, pipeline['extractor'].end_time = start, end
    pipeline['syncer'].start_time, pipeline['syncer'].end_time = start, end
    
    pipeline['extractor'].extract_audio_chunk()
    vocal_path = pipeline['extractor'].isolate_vocals()
    
    pipeline['transcriber'].transcribe_audio(vocal_path)
    
    pipeline['translator'].translate_transcription(pipeline['transcriber'].transcription_path)
    
    pipeline['cloner'].clone_and_sync_audio()
    
    return pipeline['syncer'].generate_lip_sync()

def main():
    parser = argparse.ArgumentParser(description="Supernan Hindi Dubbing Pipeline")
    parser.add_argument("--config", type=str, default="config.yaml")
    parser.add_argument("--full-video", action="store_true", help="Process full video in batches")
    args = parser.parse_args()
    
    if not os.path.exists(args.config):
        print(f"Error: {args.config} missing")
        return

    pipeline = {
        'extractor': AudioExtractor(args.config),
        'transcriber': Transcriber(args.config),
        'translator': TextTranslator(args.config),
        'cloner': VoiceCloner(args.config),
        'syncer': LipSyncer(args.config)
    }

    if args.full_video:
        print("[Scale Mode] Demonstrating full video processing via memory-safe batching.")
        chunks = [("00:00:00", "00:00:15"), ("00:00:15", "00:00:30")]
        
        for start, end in chunks:
            process_segment(pipeline, start, end)
        print("Batch processing complete! Next step: use ffmpeg to concatenate chunks.")
        
    else:
        print("[Intern Challenge Mode] Processing single 15-second snippet.")
        start, end = pipeline['extractor'].start_time, pipeline['extractor'].end_time
        final_vid = process_segment(pipeline, start, end)
        print(f"\nPipeline Complete! Final Output Video: {final_vid}")

if __name__ == "__main__":
    main()
