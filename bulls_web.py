# bulls_web.py (fixed: input buttons now use submit_button_text / cancel_button_text)
from pywebio.input import input, input_group, actions, TEXT
from pywebio.output import put_text, put_table, clear, put_buttons, toast, put_markdown
from pywebio.session import run_async
from pywebio import start_server
from datetime import datetime
import time
import os
from utils.validators import validate_username, validate_guess
from utils.storage import save_jsonl, read_jsonl
from leaderboard import get_leaderboard

DATA_DIR = "data"
GAMES_FILE = os.path.join(DATA_DIR, "games.jsonl")

# Entry point: main application menu
async def main_app():
    os.makedirs(DATA_DIR, exist_ok=True)

    while True:
        clear()
        put_markdown("## 🎲 Welcome to the *Bulls and Cows* Demo")
        put_markdown("""
### 🎯 Game Rules:
- Try to guess a 4-digit secret number composed of **unique digits from 0 to 5**.
- You have **10 attempts**.
- For each guess:
    - A **bull** means a correct digit in the correct place.
    - A **cow** means a correct digit in the wrong place.
- You win if you guess all 4 digits in the correct order within 10 turns.
- Your game results will be saved and reflected in the leaderboard.
        """)
        action = await actions("Choose an action:", buttons=[
            {"label": "🎮 Start Game", "value": "play"},
            {"label": "🏆 Leaderboard", "value": "leaderboard"},
            {"label": "🚪 Exit", "value": "exit"}
        ])

        if action == "play":
            await bulls_and_cows()
        elif action == "leaderboard":
            await leaderboard()
        else:
            clear()
            put_text("See you next time!")
            break

# Generate a random 4-digit number with unique digits (0–5)
def generate_secret_number():
    import random
    digits = list('012345')
    random.shuffle(digits)
    return ''.join(digits[:4])

# Calculate bulls and cows
def calculate_bulls_and_cows(secret, guess):
    bulls = sum(s == g for s, g in zip(secret, guess))
    cows = sum(min(secret.count(d), guess.count(d)) for d in set(guess)) - bulls
    return bulls, cows

# Main game logic
async def bulls_and_cows():
    clear()
    put_markdown("## 🎮 Game: Bulls and Cows")

    while True:
        username = await input("Enter your name (letters and digits, 3-20 characters):",
                              submit_button_text="Submit", cancel_button_text="Cancel")
        if not username or not isinstance(username, str) or not validate_username(username):
            toast("❌ Invalid name. Only letters and digits, 3-20 characters.", color='error')
            continue
        break

    toast(f"Welcome, {username}!")
    secret = generate_secret_number()
    history = []
    guesses = []
    max_turns = 10
    start_time = time.time()

    put_text("Guess the 4-digit number (digits 0 to 5, no repeats). You have 10 attempts.")

    for attempt in range(max_turns):
        put_markdown(f"### Attempt {attempt + 1} of {max_turns}")

        guess_input = await input("Enter your guess:", type=TEXT,
                                 submit_button_text="Submit", cancel_button_text="Reset")

        if not validate_guess(guess_input):
            toast("❌ Please enter exactly 4 unique digits from 0 to 5!", color='error')
            continue

        turn_start = time.time()
        bulls, cows = calculate_bulls_and_cows(secret, guess_input)
        turn_duration = time.time() - turn_start
        guesses.append({"value": guess_input, "bulls": bulls, "cows": cows, "time": round(turn_duration, 2)})
        history.append([guess_input, f"{bulls} Bulls", f"{cows} Cows"])

        clear()
        put_markdown(f"### Player: **{username}**")
        put_table([["Guess", "Bulls", "Cows"]] + history)

        if bulls == 4:
            status = "win"
            put_text("🎉 Congratulations! You guessed the number!")
            break
    else:
        status = "lose"
        put_text(f"😢 Game over. The secret number was: {secret}")

    duration = round(time.time() - start_time, 2)
    record = {
        "username": username,
        "timestamp": datetime.utcnow().isoformat(),
        "secret": secret,
        "guesses": guesses,
        "status": status,
        "duration_sec": duration
    }
    save_jsonl(GAMES_FILE, record)

    put_markdown("## 📜 Game History")
    games = [g for g in read_jsonl(GAMES_FILE) if g["username"] == username]
    rows = [[g["timestamp"].split("T")[0], g["status"], len(g["guesses"]), g["duration_sec"]] for g in games]
    put_table([["Date", "Result", "Turns", "Duration (sec)"]] + rows)

    await actions("Next: ", buttons=["🏠 Return to Menu"])

# Leaderboard page
async def leaderboard():
    clear()
    put_markdown("## 🏆 Leaderboard")
    leaderboard_data = get_leaderboard()
    if not leaderboard_data:
        put_text("No data available yet. Try playing some games first.")
        return

    rows = [[r["player"], r["games"], r["wins"], round(r["win_rate"] * 100, 1), round(r["avg_turns"], 2)] for r in leaderboard_data]
    put_table([["Player", "Games", "Wins", "% Win Rate", "Avg. Turns"]] + rows)
    await actions("Next:", buttons=["🏠 Return to Menu"])

# Start server
if __name__ == '__main__':
    start_server(main_app, port=8080, debug=True)
