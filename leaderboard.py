# leaderboard.py (updated: sorted by win_rate, then games and avg_turns)
import os
import collections
from utils.storage import read_jsonl

DATA_DIR = "data"
GAMES_FILE = os.path.join(DATA_DIR, "games.jsonl")

# Generate leaderboard: all players sorted by win_rate, then number of games, then avg_turns
def get_leaderboard():
    records = read_jsonl(GAMES_FILE)
    if not records:
        return []

    stats = collections.defaultdict(lambda: {
        "games": 0,
        "wins": 0,
        "total_turns": 0,
        "total_time": 0.0
    })

    for r in records:
        username = r.get("username")
        stats[username]["games"] += 1
        stats[username]["total_turns"] += len(r.get("guesses", []))
        stats[username]["total_time"] += r.get("duration_sec", 0)
        if r.get("status") == "win":
            stats[username]["wins"] += 1

    leaderboard = []
    for player, s in stats.items():
        games = s["games"]
        wins = s["wins"]
        win_rate = wins / games if games else 0
        leaderboard.append({
            "player": player,
            "games": games,
            "wins": wins,
            "avg_turns": s["total_turns"] / games if games else 0,
            "avg_time": s["total_time"] / games if games else 0,
            "win_rate": win_rate
        })

    leaderboard.sort(key=lambda x: (-x["win_rate"], -x["games"], x["avg_turns"]))
    return leaderboard
