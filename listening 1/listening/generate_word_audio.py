import asyncio
import edge_tts
import os
import re

# Text for Listening 1 - Time Management
TEXT = (
    "Managing time effectively helps reduce pressure and improve daily performance. "
    "In the beginning, many people struggle to organize tasks and priorities. "
    "Writing simple to-do lists can bring clarity and direction. "
    "Setting clear deadlines helps avoid last-minute stress. "
    "Breaks are also important to maintain focus and energy. "
    "Overloading schedules often leads to frustration and exhaustion. "
    "Learning to say no protects mental health and productivity. "
    "Digital calendars provide reminders and structure for busy routines. "
    "With practice, planning becomes more natural and efficient. "
    "In the long run, good time management creates balance, confidence, and greater control over personal and professional life."
)

VOICE = "en-US-JennyNeural"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "audio")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def get_unique_words(text):
    # Normalize hyphenated words so generated filenames match player lookups
    cleaned = text.lower().replace('-', '')
    words = re.findall(r"\b[\w']+\b", cleaned)
    return sorted(list(set(words)))

async def main():
    words = get_unique_words(TEXT)
    print(f"Detected {len(words)} unique words.")
    
    for word in words:
        clean_word = word.replace("'", "") # Filename safety
        output_file = os.path.join(OUTPUT_DIR, f"word_{clean_word}.mp3")
        
        # Skip if exists? No, user wants update.
        print(f"Generating: {output_file} for word: '{word}'")
        communicate = edge_tts.Communicate(word, VOICE)
        await communicate.save(output_file)
        
    print("All word audio files generated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
