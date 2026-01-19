#!/usr/bin/env python3
import os
import re
import asyncio
import edge_tts
from pathlib import Path

# Change to audio directory
audio_dir = Path(__file__).parent / "listening 1" / "listening" / "audio"
os.chdir(audio_dir)

TEXT = 'Knowing another language makes communication easier. At first, many people feel nervous about making errors, but native speakers usually appreciate your attempts to speak. When words fail, body language helps convey meaning. Reading newspapers is a great way to gradually improve vocabulary and cultural understanding. Grammar rules often seem complicated at first glance, however, practice transforms these difficult concepts into natural habits. Joining conversation groups provides valuable real world experience. Today, technology offers countless resources for independent learners, such as podcasts that teach authentic pronunciation. Keep a journal to track your improvement every week. Ultimately, mastering multiple linguistic systems increases your cognitive flexibility.'

# Extract unique words
words = re.findall(r'\b[\w\']+\b', TEXT)
unique_words = sorted(set([w.lower() for w in words]))

print(f'Found {len(unique_words)} unique words')
print('Generating word audios with Eric neural voice...\n')

async def generate_with_edge():
    voice = 'en-US-EricNeural'
    count = 0
    for i, word in enumerate(unique_words, 1):
        file = f'{word}.mp3'
        if os.path.exists(file):
            continue
        try:
            communicate = edge_tts.Communicate(word, voice=voice)
            await communicate.save(file)
            print(f'[{i}/{len(unique_words)}] ✓ {file}')
            count += 1
        except Exception as e:
            print(f'[{i}/{len(unique_words)}] ✗ Failed: {word} - {str(e)}')
    return count

count = asyncio.run(generate_with_edge())
print(f'\n✅ Generation complete! Generated {count} word audio files with Eric neural voice.')
