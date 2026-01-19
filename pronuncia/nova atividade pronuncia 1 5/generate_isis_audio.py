import asyncio
import edge_tts
import re
import os

# Text for Time Management (index.html content)
text_content = (
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

# Simple sentence splitting
sentences = re.findall(r'[^.!?]+[.!?]+', text_content)
if not sentences:
    sentences = [text_content]

sentences = [s.strip() for s in sentences]

VOICE = "en-US-GuyNeural"
OUTPUT_DIR = "audio"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

async def main():
    print(f"Detected {len(sentences)} sentences.")
    for i, sentence in enumerate(sentences):
        # Normal Speed - Prefix isis_
        output_file = os.path.join(OUTPUT_DIR, f"isis_sentence_{i}.mp3")
        print(f"Generating Normal: {output_file}...")
        communicate = edge_tts.Communicate(sentence, VOICE)
        await communicate.save(output_file)

        # Slow Speed - Prefix isis_
        output_file_slow = os.path.join(OUTPUT_DIR, f"isis_sentence_{i}_slow.mp3")
        print(f"Generating Slow: {output_file_slow}...")
        communicate_slow = edge_tts.Communicate(sentence, VOICE, rate="-25%") 
        await communicate_slow.save(output_file_slow)
    
    print("All audio files generated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
