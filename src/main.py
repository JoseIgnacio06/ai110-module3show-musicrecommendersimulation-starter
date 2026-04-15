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


def print_header(user_prefs: dict) -> None:
    """Prints the profile banner shown above the results."""
    print("=" * WIDTH)
    print("  MUSIC RECOMMENDER — TOP PICKS FOR YOU")
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

    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "acousticness": 0.20,
        "tempo_bpm": 120,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_header(user_prefs)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print_recommendation(rank, song, score, explanation)

    print(f"\n{'=' * WIDTH}")


if __name__ == "__main__":
    main()
