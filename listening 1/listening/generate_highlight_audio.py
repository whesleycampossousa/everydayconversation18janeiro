#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerar arquivos de audio highlight com Eric voice (velocidades diferentes)
"""
import asyncio
import edge_tts
import os

# Texto completo de Atividade 1/Listening 1
full_text = (
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

VOICE = "en-US-EricNeural"  # Eric voice (male)
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "audio")

async def generate_highlight_audio():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    print(f"Gerando arquivos de highlight audio com {VOICE}...\n")
    
    # Gerar highlight_1_0x.mp3 (velocidade normal)
    print("[1/2] Gerando highlight_1_0x.mp3 (velocidade normal)...")
    output_file_1x = os.path.join(OUTPUT_DIR, "highlight_1_0x.mp3")
    communicate_1x = edge_tts.Communicate(full_text, VOICE, rate="+0%")
    await communicate_1x.save(output_file_1x)
    size_1x = os.path.getsize(output_file_1x)
    print(f"✓ {output_file_1x} ({size_1x} bytes)\n")
    
    # Gerar highlight_0_8x.mp3 (velocidade lenta: -20%)
    print("[2/2] Gerando highlight_0_8x.mp3 (velocidade lenta)...")
    output_file_0_8x = os.path.join(OUTPUT_DIR, "highlight_0_8x.mp3")
    communicate_0_8x = edge_tts.Communicate(full_text, VOICE, rate="-20%")
    await communicate_0_8x.save(output_file_0_8x)
    size_0_8x = os.path.getsize(output_file_0_8x)
    print(f"✓ {output_file_0_8x} ({size_0_8x} bytes)\n")
    
    print("✅ Arquivos de highlight audio gerados com sucesso!")
    print(f"\nArquivos criados:")
    print(f"  - highlight_1_0x.mp3: {size_1x} bytes (velocidade normal)")
    print(f"  - highlight_0_8x.mp3: {size_0_8x} bytes (velocidade lenta)")

if __name__ == "__main__":
    asyncio.run(generate_highlight_audio())
