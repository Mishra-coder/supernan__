import whisperx
import yaml
import os
import json

class Transcriber:
    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
            
        self.output_dir = self.config['pipeline']['output_dir']
        self.model_size = self.config['models']['transcription']
        self.device = "cuda" if whisperx.utils.get_device() == "cuda" else "cpu"
        self.compute_type = "float16" if self.device == "cuda" else "int8"
        
        self.transcription_path = os.path.join(self.output_dir, "transcription.json")

    def transcribe_audio(self, audio_path, language="kn"):
        print(f"Loading WhisperX model ({self.model_size}) on {self.device}...")
        try:
            model = whisperx.load_model(self.model_size, self.device, compute_type=self.compute_type)
            
            print("Loading audio...")
            audio = whisperx.load_audio(audio_path)
            
            print(f"Transcribing audio in {language} (Kannada)...")
            result = model.transcribe(audio, batch_size=16, language=language)
            
            print("Aligning transcription with whisperx...")
            model_a, metadata = whisperx.load_align_model(language_code=language, device=self.device)
            result = whisperx.align(result["segments"], model_a, metadata, audio, self.device, return_char_alignments=False)
            
            with open(self.transcription_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=4)
                
            print(f"Transcription complete. Saved to {self.transcription_path}")
            return result
        except Exception as e:
            print(f"Error during transcription: {e}")
            raise

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", type=str, required=True, help="Path to input audio file")
    parser.add_argument("--config", type=str, default="config.yaml")
    parser.add_argument("--language", type=str, default="kn", help="Language code (kn for Kannada)")
    args = parser.parse_args()
    
    transcriber = Transcriber(args.config)
    transcriber.transcribe_audio(args.audio, language=args.language)
