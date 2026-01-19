import asyncio
import edge_tts
import os
import re

# Voice Configuration
VOICE = "en-US-EricNeural"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "audio")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def extract_tokens_from_index():
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    if not os.path.exists(index_path):
        print("Error: index.html not found.")
        return []
    
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Simple regex to find tokens in the englishWordData structure
    # Look for "token": "word"
    # This assumes the format used in index.html
    tokens = re.findall(r'"token":\s*"([^"]+)"', content)
    
    # We want to filter out the Portugues data if it matches the same pattern, 
    # but englishWordData usually comes first or we can better target it.
    # Actually, the file has both englishWordData and portugueseWordData.
    # Let's extract only the englishWordData block first.
    
    match = re.search(r'const englishWordData = \[(.*?)\];', content, re.DOTALL)
    if match:
        block = match.group(1)
        tokens = re.findall(r'"token":\s*"([^"]+)"', block)
        return tokens
    else:
        print("Could not find englishWordData block.")
        return []

def get_unique_words(tokens):
    # Filter out punctuation/symbols if needed, but the tokens might be words.
    words = []
    for t in tokens:
        # Simple cleanup
        w = re.sub(r'[^\w\']', '', t.lower())
        if w and not w.isdigit():
            words.append(w)
    return sorted(list(set(words)))

async def main():
    tokens = extract_tokens_from_index()
    if not tokens:
        print("No tokens found.")
        return

    words = get_unique_words(tokens)
    print(f"Found {len(words)} unique words.")
    
    for word in words:
        clean_word = word.replace("'", "")
        output_file = os.path.join(OUTPUT_DIR, f"word_{clean_word}.mp3")
        
        if os.path.exists(output_file):
            continue
            
        print(f"Generating Word: {output_file}...")
        try:
            communicate = edge_tts.Communicate(word, VOICE)
            await communicate.save(output_file)
        except Exception as e:
            print(f"Error generating {word}: {e}")

    print("Listening 2 Audio generation complete!")

if __name__ == "__main__":
    asyncio.run(main())
