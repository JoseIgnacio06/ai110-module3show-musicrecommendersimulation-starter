"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from pathlib import Path
from recommender import load_songs, recommend_songs

# Resolve the data file relative to this script, not the working directory.
# Works whether you run from the project root or from inside src/.
DATA_PATH = Path(__file__).parent.parent / "data" / "songs.csv"

WIDTH = 60

# ---------------------------------------------------------------------------
# User profiles — each dict describes one listener's taste.
# Add or edit entries here to test different preference combinations.
# Keys used by the scoring function: genre, mood, energy, acousticness, tempo_bpm
# ---------------------------------------------------------------------------
PROFILES = [
    {
        "name": "High-Energy Pop",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "acousticness": 0.10,
        "tempo_bpm": 125,
    },
    {
        "name": "Chill Lofi",
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "acousticness": 0.80,
        "tempo_bpm": 78,
    },
    {
        "name": "Deep Intense Rock",
        "genre": "rock",
        "mood": "intense",
        "energy": 0.92,
        "acousticness": 0.08,
        "tempo_bpm": 155,
    },
    {
        "name": "Late Night Jazz",
        "genre": "jazz",
        "mood": "relaxed",
        "energy": 0.37,
        "acousticness": 0.88,
        "tempo_bpm": 88,
    },
]


def print_header(user_prefs: dict) -> None:
    """Prints the profile banner shown above the results."""
    name = user_prefs.get("name", "Custom Profile")
    print("=" * WIDTH)
    print(f"  {name.upper()}")
    print("=" * WIDTH)
    profile_line = (
        f"  Genre: {user_prefs.get('genre', '—')}  |  "
        f"Mood: {user_prefs.get('mood', '—')}  |  "
        f"Energy: {user_prefs.get('energy', '—')}"
    )
    print(profile_line)
    print("=" * WIDTH)


def print_recommendation(rank: int, song: dict, score: float, explanation: str) -> None:
    """Prints one ranked result with its score and scoring breakdown."""
    print(f"\n#{rank}  {song['title']}  —  {song['artist']}")
    print(f"    Genre: {song['genre']}  |  Mood: {song['mood']}  |  Score: {score:.2f} pts")
    print("    Why this song:")
    for reason in explanation.split(" | "):
        print(f"      · {reason}")


def main() -> None:
    songs = load_songs(str(DATA_PATH))
    print(f"Loaded {len(songs)} songs from catalog.\n")

    for profile in PROFILES:
        recommendations = recommend_songs(profile, songs, k=3)
        print_header(profile)
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print_recommendation(rank, song, score, explanation)
        print(f"\n{'=' * WIDTH}\n")


if __name__ == "__main__":
    main()
