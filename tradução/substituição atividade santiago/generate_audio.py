import asyncio
import edge_tts
import os
import re

# Sentences for Tradução - Time Management
sentences = [
    "Managing time effectively helps reduce pressure and improve daily performance.",
    "In the beginning, many people struggle to organize tasks and priorities.",
    "Writing simple to-do lists can bring clarity and direction.",
    "Setting clear deadlines helps avoid last-minute stress.",
    "Breaks are also important to maintain focus and energy.",
    "Overloading schedules often leads to frustration and exhaustion.",
    "Learning to say no protects mental health and productivity.",
    "Digital calendars provide reminders and structure for busy routines.",
    "With practice, planning becomes more natural and efficient.",
    "In the long run, good time management creates balance, confidence, and greater control over personal and professional life."
]

VOICE = "en-US-EricNeural"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "audio")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def get_unique_words(text):
    cleaned = text.lower().replace('-', '')
    words = re.findall(r"\b[\w']+\b", cleaned)
    return sorted(list(set(words)))

async def main():
    print(f"Detected {len(sentences)} sentences.")
    for i, sentence in enumerate(sentences):
        # Normal Speed
        output_file = os.path.join(OUTPUT_DIR, f"sentence_{i}.mp3")
        print(f"Generating Normal: {output_file}...")
        communicate = edge_tts.Communicate(sentence, VOICE)
        await communicate.save(output_file)

        # Slow Speed
        output_file_slow = os.path.join(OUTPUT_DIR, f"sentence_{i}_slow.mp3")
        print(f"Generating Slow: {output_file_slow}...")
        communicate_slow = edge_tts.Communicate(sentence, VOICE, rate="-25%") 
        await communicate_slow.save(output_file_slow)

    # Word Audio Generation (Added for consistency)
    full_text = " ".join(sentences)
    words = get_unique_words(full_text)
    print(f"Generating audio for {len(words)} unique words...")
    
    for word in words:
        clean_word = word.replace("'", "")
        output_file = os.path.join(OUTPUT_DIR, f"word_{clean_word}.mp3")
        print(f"Generating Word: {output_file}...")
        communicate = edge_tts.Communicate(word, VOICE)
        await communicate.save(output_file)
        
    print("All audio files generated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
