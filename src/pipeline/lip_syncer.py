import os
import yaml
import subprocess

class LipSyncer:
    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
            
        self.input_video = self.config['pipeline']['input_video']
        self.output_dir = self.config['pipeline']['output_dir']
        
        self.cropped_video_path = os.path.join(self.output_dir, "cropped_input.mp4")
        self.final_audio_path = os.path.join(self.output_dir, "final_dubbed_audio.wav")
        self.final_video_path = os.path.join(self.output_dir, "supernan_hindi_dub_15s.mp4")
        
        self.start_time = self.config['pipeline']['start_time']
        self.end_time = self.config['pipeline']['end_time']

    def crop_input_video(self):
        print(f"Cropping original video from {self.start_time} to {self.end_time}...")
        command = [
            'ffmpeg',
            '-y',
            '-i', self.input_video,
            '-ss', self.start_time,
            '-to', self.end_time,
            '-c:v', 'libx264',
            '-c:a', 'aac',
            self.cropped_video_path
        ]
        
        try:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Video cropped successfully to {self.cropped_video_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error cropping video: {e}")
            raise

    def generate_lip_sync(self):
        if not os.path.exists(self.cropped_video_path):
            self.crop_input_video()
            
        if not os.path.exists(self.final_audio_path):
            raise FileNotFoundError(f"Final dubbed audio not found at {self.final_audio_path}. Run voice cloning first.")
            
        print("Starting VideoReTalking for high-fidelity lip sync...")
        print("Note: This assumes the VideoReTalking repository and environment are set up.")
        
        # Command assumes we are calling the inference script of VideoReTalking
        # which usually looks something like this:
        command = [
            'python', 'inference.py', 
            '--face', self.cropped_video_path, 
            '--audio', self.final_audio_path, 
            '--outfile', self.final_video_path
        ]
        
        try:
            # We don't suppress stdout here so the user can see the progress of the heavy model
            subprocess.run(command, check=True)
            print(f"\n=========================================")
            print(f"SUCCESS! Final Hindi Dubbed Video Generated at: {self.final_video_path}")
            print(f"=========================================\n")
            return self.final_video_path
        except subprocess.CalledProcessError as e:
            print(f"Error during VideoReTalking lip-sync: {e}")
            raise

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Lip-sync generated audio to the source video.")
    parser.add_argument("--config", type=str, default="config.yaml")
    args = parser.parse_args()
    
    syncer = LipSyncer(args.config)
    syncer.generate_lip_sync()
