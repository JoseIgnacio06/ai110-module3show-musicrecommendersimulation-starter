# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.
 
- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
  genre, mood, energy, tempo, valence, danceability, acousticness.
- What information does your `UserProfile` store
A profile captures a single listener's taste as a small set of target values:

favorite_genre: the style they gravitate toward most, i.e. "lofi"
favorite_mood: the emotional feel they want right now, i.e. "chill"
target_energy: their preferred intensity level, i.e. 0.40 for calm background music
target_acousticness: whether they prefer organic sound (0.80) or produced/electronic (0.10)
target_valence: their preferred emotional brightness, i.e. 0.60 for neutral-to-warm
target_tempo_bpm: their preferred speed, i.e. 80 BPM for unhurried music
likes_acoustic: a simple true/false flag that complements the acousticness target
The profile does not store any history, skips, or plays; it is a static snapshot of declared preference, not learned behavior.

- How does your `Recommender` compute a score for each song
Every song is given a score between 0.0 and 1.0 that represents how well it fits the user's profile. The score is a weighted sum of five individual sub-scores:

total score =
  35% × mood match
+ 25% × energy match
+ 20% × genre match
+ 15% × acousticness match
+  5% × tempo match

- How do you choose which songs to recommend
The recommender runs in two stages:

Stage 1: Score every song. The scoring formula runs once for each song in the catalog, producing a scored list of all 20 songs.

Stage 2: Rank and return the top k. The list is sorted from highest to lowest score. The top k songs (default: 5) are returned as the final recommendations.

Songs that match on both mood and genre rise to the top. Songs that share only one of those two drop to the middle. Songs that match on nothing are buried at the bottom regardless of their numeric features.

You can include a simple diagram or bullet list if helpful.
Some prompts to answer:

-

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

---These questions below are already answered in model_card.md---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

