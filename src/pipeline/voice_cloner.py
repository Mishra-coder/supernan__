import os
import yaml
import json
import torch
from TTS.api import TTS
from pydub import AudioSegment

class VoiceCloner:
    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
            
        self.output_dir = self.config['pipeline']['output_dir']
        self.reference_audio = os.path.join(self.output_dir, "htdemucs", "extracted_audio", "vocals.wav")
        self.translation_path = os.path.join(self.output_dir, "translation.json")
        self.final_audio_path = os.path.join(self.output_dir, "final_dubbed_audio.wav")
        
        self.model_name = self.config['models']['voice_cloning']
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def match_audio_duration(self, audio_segment, target_duration_ms):
        current_duration_ms = len(audio_segment)
        if current_duration_ms == 0:
            return audio_segment
            
        ratio = current_duration_ms / target_duration_ms
        
        if 0.95 <= ratio <= 1.05:
            return audio_segment
            
        speedup_audio = audio_segment.speedup(playback_speed=ratio, chunk_size=150, crossfade=25)
        
        if len(speedup_audio) > target_duration_ms:
            speedup_audio = speedup_audio[:target_duration_ms]
        elif len(speedup_audio) < target_duration_ms:
            silence = AudioSegment.silent(duration=target_duration_ms - len(speedup_audio))
            speedup_audio = speedup_audio + silence
            
        return speedup_audio

    def clone_and_sync_audio(self):
        if not os.path.exists(self.reference_audio):
            raise FileNotFoundError(f"Reference vocal audio not found at {self.reference_audio}. Run audio extraction first.")
            
        if not os.path.exists(self.translation_path):
            raise FileNotFoundError(f"Translation JSON not found at {self.translation_path}. Run translation first.")
            
        print(f"Loading TTS Model ({self.model_name}) on {self.device}...")
        try:
            tts = TTS(model_name=self.model_name, progress_bar=False).to(self.device)
        except Exception as e:
            print(f"Failed to load TTS model: {e}")
            raise

        with open(self.translation_path, 'r', encoding='utf-8') as f:
            segments = json.load(f)

        final_audio = AudioSegment.silent(duration=0)
        current_time_ms = 0
        
        os.makedirs(os.path.join(self.output_dir, "temp_tts"), exist_ok=True)

        for i, segment in enumerate(segments):
            start_ms = int(segment['start'] * 1000)
            end_ms = int(segment['end'] * 1000)
            target_duration_ms = end_ms - start_ms
            hindi_text = segment['translated_text']
            
            if start_ms > current_time_ms:
                silence_gap = start_ms - current_time_ms
                final_audio += AudioSegment.silent(duration=silence_gap)
                current_time_ms = start_ms

            temp_wav = os.path.join(self.output_dir, "temp_tts", f"segment_{i}.wav")
            
            print(f"Synthesizing segment {i}: {hindi_text[:30]}...")
            try:
                tts.tts_to_file(
                    text=hindi_text,
                    file_path=temp_wav,
                    speaker_wav=self.reference_audio,
                    language="hi"
                )
                
                generated_segment = AudioSegment.from_wav(temp_wav)
                synced_segment = self.match_audio_duration(generated_segment, target_duration_ms)
                
                final_audio += synced_segment
                current_time_ms += len(synced_segment)
                
            except Exception as e:
                print(f"Failed to synthesize segment {i}: {e}")
                final_audio += AudioSegment.silent(duration=target_duration_ms)
                current_time_ms += target_duration_ms

        print("Exporting final synchronized dubbed audio...")
        final_audio.export(self.final_audio_path, format="wav")
        print(f"Success Sequence Saved to: {self.final_audio_path}")
        return self.final_audio_path

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Clone voice and match lip-sync pacing.")
    parser.add_argument("--config", type=str, default="config.yaml")
    args = parser.parse_args()
    
    cloner = VoiceCloner(args.config)
    cloner.clone_and_sync_audio()
