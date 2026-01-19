import edge_tts
import asyncio
import os
import re

# Pronuncia full text (from index.html)
text = (
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

# Extract unique words
def get_unique_words(text):
    # Remove punctuation and convert to lowercase
    clean_text = re.sub(r'[^\w\s]', '', text.lower().replace('-', ''))
    words = clean_text.split()
    return sorted(list(set(words)))

unique_words = get_unique_words(text)

VOICE = "en-US-JennyNeural"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "audio")

async def generate_audio(text, filename):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(filename)

async def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"Detected {len(unique_words)} unique words.")
    
    for word in unique_words:
        # Safety for filename
        clean_word = word.replace("'", "")
        filename = os.path.join(OUTPUT_DIR, f"word_{clean_word}.mp3")
        # Ensure we generate all, even if exists, to key matches
        print(f"Generating: {filename}...")
        await generate_audio(word, filename)
    
    print("All word audio files generated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
