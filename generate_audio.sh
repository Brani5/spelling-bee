#!/bin/bash
# Generate all Spelling Bee audio files using ElevenLabs via sag
# Usage: bash generate_audio.sh

set -e

# Load API keys
source /Users/brani/.config/secrets/.env

BASE="/Users/brani/myApps/KidSkillBooster/SpellingBee/audio"
mkdir -p "$BASE/letters" "$BASE/words" "$BASE/reactions" "$BASE/narrator"

# Voice IDs
MAIN="767pDqDBO3o8czWnMxD5"    # Custom gaming host (words + letters)
HYPE="Qls9lm4Ivt5eJHamqhd5"    # Raperský (correct reactions)
NARRATOR="3y2UWiwEs8zqDEdnBeaq"  # Drzý ženský (Squid Game narrator)

echo "=== Generating alphabet letters ==="
for letter in A B C D E F G H I J K L M N O P Q R S T U V W X Y Z; do
  if [ ! -f "$BASE/letters/${letter}.mp3" ]; then
    echo "  Letter: $letter"
    sag "$letter" --voice "$MAIN" --output "$BASE/letters/${letter}.mp3" --play=false 2>/dev/null || echo "  FAILED: $letter"
    sleep 0.3
  fi
done

echo "=== Generating word pronunciations ==="
WORDS=(
bat bed big hot bug map pet sit mop cup stamp blast swept crisp stomp clap spell trick block
craft sketch strict shrunk
chat ship thin whip chop shut them when chin shop church shrimp think whale cheese shadow throne
white shield chapter shoulder thousand chocolate
flag tree skip snow swim glad plan drop frog sled planet brave crown dream freeze glow splash
string struggle scratch sprinkle squirrel strength
car bird star turn fern dirt born garden corner perfect thirty turtle morning circle surprise
important different hamburger
rain play boat moon day read grow food seed explain between teacher rainbow cartoon follow
freedom sneaker mushroom
boy coin cow loud saw toy down out draw enjoy flower mountain awesome destroy choice tower
around crawl
cake bike home cute name time bone huge lake five escape invite explore costume mistake
sunshine excuse complete
back ring pink catch edge duck song match bridge attack belong kitchen knowledge unlock
amazing blanket fridge
city giant phone knee write center gentle dolphin knight wrong celebrate imagine photograph
wrinkle
creeper diamond potion village enchant survive challenge treasure monster adventure
)

for word in "${WORDS[@]}"; do
  if [ ! -f "$BASE/words/${word}.mp3" ]; then
    echo "  Word: $word"
    sag "$word" --voice "$MAIN" --output "$BASE/words/${word}.mp3" --play=false 2>/dev/null || echo "  FAILED: $word"
    sleep 0.3
  fi
done

echo "=== Generating hype reactions ==="
declare -A REACTIONS=(
  ["correct1"]="Yes! You got it!"
  ["correct2"]="That's right! Nice one!"
  ["correct3"]="Boom! Perfect spelling!"
  ["correct4"]="You're on fire!"
  ["correct5"]="Absolutely nailed it!"
  ["streak3"]="Three in a row! Keep going!"
  ["streak5"]="Five streak! You're unstoppable!"
  ["streak10"]="TEN IN A ROW! You're a spelling legend!"
  ["skip"]="No worries, let's try another one."
  ["wrong"]="Almost! Give it another shot."
  ["tryagain"]="So close! Listen again carefully."
)

for key in "${!REACTIONS[@]}"; do
  if [ ! -f "$BASE/reactions/${key}.mp3" ]; then
    echo "  Reaction: $key"
    sag "${REACTIONS[$key]}" --voice "$HYPE" --output "$BASE/reactions/${key}.mp3" --play=false 2>/dev/null || echo "  FAILED: $key"
    sleep 0.3
  fi
done

echo "=== Generating Squid Game narrator ==="
declare -A NARRATION=(
  ["round1"]="Round one. Let the game begin."
  ["round2"]="Round two. It's getting harder."
  ["round3"]="Round three. Stay focused."
  ["round4"]="Round four. Only the best survive."
  ["round5"]="Round five. Almost there."
  ["round6"]="Final round. This is it. Show me what you've got."
  ["complete"]="Congratulations. You survived."
  ["eliminated"]="Eliminated. Just kidding. Try again!"
  ["welcome"]="Welcome to the Spelling Bee Squid Game. Spell or be eliminated."
)

for key in "${!NARRATION[@]}"; do
  if [ ! -f "$BASE/narrator/${key}.mp3" ]; then
    echo "  Narrator: $key"
    sag "${NARRATION[$key]}" --voice "$NARRATOR" --output "$BASE/narrator/${key}.mp3" --play=false 2>/dev/null || echo "  FAILED: $key"
    sleep 0.3
  fi
done

echo "=== DONE ==="
echo "Total files:"
find "$BASE" -name "*.mp3" | wc -l
