import os
import subprocess
import yaml

class AudioExtractor:
    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
            
        self.input_video = self.config['pipeline']['input_video']
        self.output_dir = self.config['pipeline']['output_dir']
        self.start_time = self.config['pipeline']['start_time']
        self.end_time = self.config['pipeline']['end_time']
        
        self.temp_audio_path = os.path.join(self.output_dir, "extracted_audio.wav")
        self.vocal_path = os.path.join(self.output_dir, "htdemucs", "extracted_audio", "vocals.wav")
        
        os.makedirs(self.output_dir, exist_ok=True)

    def extract_audio_chunk(self):
        print(f"Extracting audio segment from {self.start_time} to {self.end_time}...")
        
        command = [
            'ffmpeg',
            '-y',
            '-i', self.input_video,
            '-ss', self.start_time,
            '-to', self.end_time,
            '-q:a', '0',
            '-map', 'a',
            self.temp_audio_path
        ]
        
        try:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("Audio extraction successful.")
            return self.temp_audio_path
        except subprocess.CalledProcessError as e:
            print(f"Error extracting audio: {e}")
            raise

    def isolate_vocals(self):
        print("Isolating vocals using Demucs (this may take a moment)...")
        
        command = [
            'demucs',
            '-n', self.config['audio_processing']['vocal_isolation_model'],
            '--out', self.output_dir,
            self.temp_audio_path
        ]
        
        try:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Vocal isolation complete. Isolated vocals saved at {self.vocal_path}")
            return self.vocal_path
        except subprocess.CalledProcessError as e:
            print(f"Error isolating vocals: {e}")
            raise

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extract and isolate vocals from video.")
    parser.add_argument("--config", type=str, default="config.yaml", help="Path to configuration file")
    args = parser.parse_args()
    
    extractor = AudioExtractor(args.config)
    try:
        extractor.extract_audio_chunk()
        extractor.isolate_vocals()
    except Exception as e:
        print(f"Pipeline failed at audio extraction phase: {e}")
