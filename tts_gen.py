#!/usr/bin/env python3
"""Generate TTS audio files using ElevenLabs API via urllib (no deps)."""
import urllib.request, json, os, sys, time

# Load env
env_file = os.path.expanduser("~/.config/secrets/.env")
with open(env_file) as f:
    for line in f:
        if line.startswith("export "):
            k, v = line.replace("export ", "").strip().split("=", 1)
            os.environ[k] = v.strip('"')

API_KEY = os.environ["ELEVENLABS_API_KEY"]
BASE = "/Users/brani/myApps/KidSkillBooster/SpellingBee/audio"

VOICES = {
    "main": "767pDqDBO3o8czWnMxD5",
    "hype": "Qls9lm4Ivt5eJHamqhd5",
    "narrator": "3y2UWiwEs8zqDEdnBeaq",
}

def tts(text, voice_id, output_path, model="eleven_v3"):
    if os.path.exists(output_path) and os.path.getsize(output_path) > 100:
        return True
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    data = json.dumps({"text": text, "model_id": model}).encode()
    req = urllib.request.Request(url, data=data, headers={
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    })
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        with open(output_path, "wb") as f:
            f.write(resp.read())
        size = os.path.getsize(output_path)
        if size < 100:
            os.remove(output_path)
            return False
        return True
    except Exception as e:
        print(f"  ERROR: {e}", file=sys.stderr)
        return False

def main():
    for d in ["letters", "words", "reactions", "narrator"]:
        os.makedirs(os.path.join(BASE, d), exist_ok=True)

    # Letters
    print("=== Letters ===")
    for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        path = os.path.join(BASE, "letters", f"{ch}.mp3")
        ok = tts(ch, VOICES["main"], path)
        print(f"  {ch}: {'OK' if ok else 'FAIL'}")
        time.sleep(0.3)

    # Words
    print("=== Words ===")
    words = [
        "bat","bed","big","hot","bug","map","pet","sit","mop","cup",
        "stamp","blast","swept","crisp","stomp","clap","spell","trick","block",
        "craft","sketch","strict","shrunk",
        "chat","ship","thin","whip","chop","shut","them","when","chin","shop",
        "church","shrimp","think","whale","cheese","shadow","throne","white","shield",
        "chapter","shoulder","thousand","chocolate",
        "flag","tree","skip","snow","swim","glad","plan","drop","frog","sled",
        "planet","brave","crown","dream","freeze","glow","splash","string",
        "struggle","scratch","sprinkle","squirrel","strength",
        "car","bird","star","turn","fern","dirt","born",
        "garden","corner","perfect","thirty","turtle","morning","circle","surprise",
        "important","different","hamburger",
        "rain","play","boat","moon","day","read","grow","food","seed",
        "explain","between","teacher","rainbow","cartoon","follow",
        "freedom","sneaker","mushroom",
        "boy","coin","cow","loud","saw","toy","down","out","draw",
        "enjoy","flower","mountain","awesome","destroy","choice","tower","around","crawl",
        "cake","bike","home","cute","name","time","bone","huge","lake","five",
        "escape","invite","explore","costume","mistake","sunshine","excuse","complete",
        "back","ring","pink","catch","edge","duck","song","match","bridge",
        "attack","belong","kitchen","knowledge","unlock","amazing","blanket","fridge",
        "city","giant","phone","knee","write","center","gentle","dolphin","knight","wrong",
        "celebrate","imagine","photograph","wrinkle",
        "creeper","diamond","potion","village","enchant","survive",
        "challenge","treasure","monster","adventure",
    ]
    for w in words:
        path = os.path.join(BASE, "words", f"{w}.mp3")
        ok = tts(w, VOICES["main"], path)
        print(f"  {w}: {'OK' if ok else 'FAIL'}")
        time.sleep(0.3)

    # Reactions (hype voice)
    print("=== Reactions ===")
    reactions = {
        "correct1": "Yes! You got it!",
        "correct2": "That's right! Nice one!",
        "correct3": "Boom! Perfect spelling!",
        "correct4": "You're on fire!",
        "correct5": "Absolutely nailed it!",
        "streak3": "Three in a row! Keep going!",
        "streak5": "Five streak! You're unstoppable!",
        "streak10": "TEN IN A ROW! You're a spelling legend!",
        "skip": "No worries, let's try another one.",
        "wrong": "Almost! Give it another shot.",
        "tryagain": "So close! Listen again carefully.",
    }
    for key, text in reactions.items():
        path = os.path.join(BASE, "reactions", f"{key}.mp3")
        ok = tts(text, VOICES["hype"], path)
        print(f"  {key}: {'OK' if ok else 'FAIL'}")
        time.sleep(0.3)

    # Narrator (Squid Game voice)
    print("=== Narrator ===")
    narration = {
        "round1": "Round one. Let the game begin.",
        "round2": "Round two. It's getting harder.",
        "round3": "Round three. Stay focused.",
        "round4": "Round four. Only the best survive.",
        "round5": "Round five. Almost there.",
        "round6": "Final round. This is it. Show me what you've got.",
        "complete": "Congratulations. You survived.",
        "eliminated": "Eliminated. Just kidding. Try again!",
        "welcome": "Welcome to the Spelling Bee Squid Game. Spell or be eliminated.",
    }
    for key, text in narration.items():
        path = os.path.join(BASE, "narrator", f"{key}.mp3")
        ok = tts(text, VOICES["narrator"], path)
        print(f"  {key}: {'OK' if ok else 'FAIL'}")
        time.sleep(0.3)

    # Count
    total = sum(len(os.listdir(os.path.join(BASE, d))) for d in ["letters","words","reactions","narrator"] if os.path.isdir(os.path.join(BASE, d)))
    print(f"\n=== DONE: {total} files ===")

if __name__ == "__main__":
    main()
