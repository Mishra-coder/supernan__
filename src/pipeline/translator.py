import os
import yaml
import json
from groq import Groq

class TextTranslator:
    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
            
        self.output_dir = self.config['pipeline']['output_dir']
        self.translation_path = os.path.join(self.output_dir, "translation.json")
        
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set. Please set it to use the translator.")
        self.client = Groq(api_key=self.api_key)

    def translate_transcription(self, transcription_path):
        print(f"Loading transcription from {transcription_path}...")
        with open(transcription_path, 'r', encoding='utf-8') as f:
            transcription = json.load(f)
            
        translated_segments = []
        
        print("Translating segments to Hindi using Groq (Context-Aware)...")
        for segment in transcription.get("segments", []):
            original_text = segment.get("text", "").strip()
            if not original_text:
                continue
                
            prompt = (
                "You are an expert English to Hindi translator. "
                "Translate the following spoken English sentence into natural, "
                "context-aware conversational Hindi suitable for a nanny or child-caretaker context. "
                "Only return the Hindi translation, no extra text, explanations, or quotes.\n\n"
                f"English: {original_text}"
            )
            
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a precise and fluent English to Hindi translator."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model="llama3-8b-8192",
                    temperature=0.3,
                )
                hindi_text = chat_completion.choices[0].message.content.strip()
                
                translated_segments.append({
                    "start": segment.get("start"),
                    "end": segment.get("end"),
                    "original_text": original_text,
                    "translated_text": hindi_text
                })
                print(f"Translated: '{original_text}' -> '{hindi_text}'")
                
            except Exception as e:
                print(f"Translation failed for segment '{original_text}': {e}")
                translated_segments.append({
                    "start": segment.get("start"),
                    "end": segment.get("end"),
                    "original_text": original_text,
                    "translated_text": "[TRANSLATION ERROR]"
                })
                
        with open(self.translation_path, 'w', encoding='utf-8') as f:
            json.dump(translated_segments, f, ensure_ascii=False, indent=4)
            
        print(f"Translation complete. Saved to {self.translation_path}")
        return self.translation_path

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Translate English transcription to Hindi.")
    parser.add_argument("--transcription", type=str, required=True, help="Path to transcription JSON")
    parser.add_argument("--config", type=str, default="config.yaml")
    args = parser.parse_args()
    
    translator = TextTranslator(args.config)
    translator.translate_transcription(args.transcription)
