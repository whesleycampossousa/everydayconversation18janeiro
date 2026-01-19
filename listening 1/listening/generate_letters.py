import argparse
import asyncio
import edge_tts
import os

VOICE = "en-US-JennyNeural"
LETTERS = [chr(code) for code in range(ord("A"), ord("Z") + 1)]


async def synthesize(letter: str, path: str) -> None:
    communicate = edge_tts.Communicate(letter, VOICE)
    await communicate.save(path)


async def main(output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    print(f"Generating letters to {output_dir}")
    for letter in LETTERS:
        filename = os.path.join(output_dir, f"letter_{letter.lower()}.mp3")
        if os.path.exists(filename):
            os.remove(filename)
        print(f"  • {filename}")
        await synthesize(letter, filename)
    print("Letter audio generation complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate letter audio files (A-Z).")
    parser.add_argument(
        "--output",
        "-o",
        default="audio",
        help="Directory where the letter audio files should be saved."
    )
    args = parser.parse_args()
    asyncio.run(main(args.output))
