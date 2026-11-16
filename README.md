# ✦ QuizQuest — Learn. Play. Level Up.

QuizQuest is a desktop multiple-choice quiz game built with Python and Tkinter. Pick a category, answer a 10-question round, collect points, and try to climb the local leaderboard.

## Features

- Clean dark-themed desktop interface
- Four question categories: Python, AI & ML, Tech Trivia, and General Knowledge
- Random 10-question rounds with shuffled answer options (the correct answer is not always in the same spot)
- 40 built-in questions (10 per category)
- Instant feedback with a short explanation after each answer
- Points and percentage score at the end of each round
- Local leaderboard saved between sessions using JSON
- Easy-to-edit question bank, validated on load so a bad entry can't crash the app
- Leaderboard ranked by percentage, so rounds of different lengths compare fairly
- Unit tests for the quiz logic

## Tech used

- Python 3
- Tkinter for the graphical user interface
- JSON for question and score storage
- `random` for selecting questions
- `datetime` for score timestamps
- Object-oriented programming, functions, lists, dictionaries, loops, and file handling

## Requirements

- Python 3.9 or newer
- Tkinter (included with most standard Python installations)

No third-party Python packages are needed.

## Run on Windows

1. Download and extract this project ZIP.
2. Open the extracted `quizquest` folder.
3. Click the folder address bar, type `cmd`, and press Enter.
4. Run:

```bash
py main.py
```

If `py` does not work, try:

```bash
python main.py
```

## Run on macOS / Linux

Open a terminal in the project folder and run:

```bash
python3 main.py
```

If Tkinter is missing on Linux, install your distribution's Tkinter package (often named `python3-tk`).

## Project structure

```text
quizquest/
├── main.py            # Tkinter interface
├── quiz_logic.py      # GUI-free logic (loading, validation, scoring)
├── tests/
│   └── test_quiz_logic.py
├── requirements.txt
├── README.md
└── data/
    ├── questions.json
    └── scores.json   # created automatically after your first round
```

## Add your own questions

Open `data/questions.json` and add another question object using this format:

```json
{
  "category": "Your Category",
  "question": "Your question?",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "answer": "Option B",
  "explanation": "A short explanation of why this is correct."
}
```

Make sure the answer exactly matches one of the options.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Concepts demonstrated

- **OOP:** `QuizQuest` class keeps the app's data and behaviour together.
- **Separation of concerns:** UI code lives in `main.py`, testable logic in `quiz_logic.py`.
- **Testing:** `unittest` covers validation, round selection, ranking and file handling.
- **GUI programming:** Tkinter widgets build the desktop interface.
- **File handling:** JSON files store questions and leaderboard scores.
- **Data structures:** Lists and dictionaries organize questions and results.
- **Randomization:** Each round gets a different selection of questions.
- **Validation:** The app asks the player to select an answer before continuing.

## Future improvements

- Add difficulty levels and timed rounds
- Let users create custom question sets
- Add badges for achievements
- Add a chart showing score progress over time

## Portfolio description

**QuizQuest** is a Python desktop quiz application featuring category-based randomized quizzes, instant answer explanations, score tracking, and a persistent JSON leaderboard. It demonstrates object-oriented programming, GUI development with Tkinter, data structures, randomization, and file handling.

---
Made as a beginner-to-intermediate Python portfolio project.
