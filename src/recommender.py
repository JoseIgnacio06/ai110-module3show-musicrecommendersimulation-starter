import csv
import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py

    Reads each row into a dictionary and converts numeric columns to the
    appropriate Python type so callers can do math without extra casting:
        id           → int
        energy       → float
        tempo_bpm    → float
        valence      → float
        danceability → float
        acousticness → float
    All other columns (title, artist, genre, mood) stay as strings.
    """
    numeric_float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            for field in numeric_float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Points awarded per feature (max 10.0 when all features are present):
        mood        +3.5   binary match
        energy      +2.5   Gaussian decay (sigma=0.20)
        genre       +2.0   binary match
        acousticness +1.5  Gaussian decay (sigma=0.20)
        tempo_bpm   +0.5   Gaussian decay on normalised BPM (sigma=0.20)

    Features absent from user_prefs are skipped — their points are simply
    not added, so the maximum score scales with what the profile provides.

    Returns:
        (score, reasons) where reasons is a list of human-readable strings
        explaining the contribution of each feature, e.g.:
            "mood match: chill (+3.50)"
            "energy near match: |0.42 - 0.40| = 0.02 (+2.48)"
            "genre mismatch: rock vs lofi (+0.00)"
    """
    SIGMA = 0.20
    TEMPO_MIN = 60.0
    TEMPO_MAX = 174.0

    score = 0.0
    reasons = []

    # --- Mood: binary match, worth 3.5 points ---
    if "mood" in user_prefs:
        if song["mood"] == user_prefs["mood"]:
            score += 3.5
            reasons.append(f"mood match: {song['mood']} (+3.50)")
        else:
            reasons.append(
                f"mood mismatch: {song['mood']} vs {user_prefs['mood']} (+0.00)"
            )

    # --- Genre: binary match, worth 2.0 points ---
    if "genre" in user_prefs:
        if song["genre"] == user_prefs["genre"]:
            score += 2.0
            reasons.append(f"genre match: {song['genre']} (+2.00)")
        else:
            reasons.append(
                f"genre mismatch: {song['genre']} vs {user_prefs['genre']} (+0.00)"
            )

    # --- Energy: Gaussian decay, worth up to 2.5 points ---
    if "energy" in user_prefs:
        distance = abs(song["energy"] - user_prefs["energy"])
        energy_points = 2.5 * math.exp(-(distance ** 2) / (2 * SIGMA ** 2))
        score += energy_points
        reasons.append(
            f"energy {'near match' if distance <= SIGMA else 'far match'}: "
            f"|{song['energy']:.2f} - {user_prefs['energy']:.2f}| = {distance:.2f} "
            f"(+{energy_points:.2f})"
        )

    # --- Acousticness: Gaussian decay, worth up to 1.5 points ---
    if "acousticness" in user_prefs:
        distance = abs(song["acousticness"] - user_prefs["acousticness"])
        acoustic_points = 1.5 * math.exp(-(distance ** 2) / (2 * SIGMA ** 2))
        score += acoustic_points
        reasons.append(
            f"acousticness {'near match' if distance <= SIGMA else 'far match'}: "
            f"|{song['acousticness']:.2f} - {user_prefs['acousticness']:.2f}| = {distance:.2f} "
            f"(+{acoustic_points:.2f})"
        )

    # --- Tempo: Gaussian decay on normalised BPM, worth up to 0.5 points ---
    if "tempo_bpm" in user_prefs:
        norm_song = (song["tempo_bpm"] - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
        norm_user = (user_prefs["tempo_bpm"] - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
        distance = abs(norm_song - norm_user)
        tempo_points = 0.5 * math.exp(-(distance ** 2) / (2 * SIGMA ** 2))
        score += tempo_points
        reasons.append(
            f"tempo {'near match' if distance <= SIGMA else 'far match'}: "
            f"|{song['tempo_bpm']:.0f} - {user_prefs['tempo_bpm']:.0f}| BPM "
            f"(+{tempo_points:.2f})"
        )

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Steps:
        1. Score every song using score_song() — produces (song, score, reasons)
        2. Sort by score descending with sorted() so the original list is unchanged
        3. Slice the top k results
        4. Join each song's reasons list into a single explanation string

    Returns a list of (song_dict, score, explanation) tuples, highest score first.
    """
    # Score every song — *score_song() unpacks (score, reasons) inline
    scored = [(song, *score_song(user_prefs, song)) for song in songs]

    # sorted() returns a new list; the original songs list is not mutated
    top_k = sorted(scored, key=lambda item: item[1], reverse=True)[:k]

    # Collapse the reasons list into one readable string per song
    return [(song, score, " | ".join(reasons)) for song, score, reasons in top_k]
