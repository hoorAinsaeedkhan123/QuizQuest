import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from datetime import datetime

from quiz_logic import (
    POINTS_PER_QUESTION, add_score, clean_questions, clean_scores,
    load_json, make_score_entry, pick_round, save_json,
)

ROOT = Path(__file__).parent
QUESTIONS_FILE = ROOT / "data" / "questions.json"
SCORES_FILE = ROOT / "data" / "scores.json"

COLORS = {
    "bg": "#101827", "panel": "#1b2940", "panel2": "#243650",
    "text": "#f4f7fb", "muted": "#a9b8cc", "accent": "#70e1c1",
    "yellow": "#ffd166", "red": "#ff758f"
}

class QuizQuest:
    def __init__(self, root):
        self.root = root
        self.root.title("QuizQuest | Learn. Play. Level Up.")
        self.root.geometry("820x620")
        self.root.minsize(720, 560)
        self.root.configure(bg=COLORS["bg"])
        self.questions = clean_questions(load_json(QUESTIONS_FILE, []))
        self.scores = clean_scores(load_json(SCORES_FILE, []))
        self.current_questions = []
        self.index = 0
        self.score = 0
        self.player = "Player"
        self.category = "All"
        self.selected = tk.StringVar()
        self.build_home()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def panel(self, parent=None):
        return tk.Frame(parent or self.root, bg=COLORS["panel"], padx=26, pady=22)

    def heading(self, parent, title, subtitle=""):
        tk.Label(parent, text=title, bg=COLORS["panel"], fg=COLORS["text"],
                 font=("Segoe UI", 25, "bold")).pack(anchor="w")
        if subtitle:
            tk.Label(parent, text=subtitle, bg=COLORS["panel"], fg=COLORS["muted"],
                     font=("Segoe UI", 10)).pack(anchor="w", pady=(5, 16))

    def build_home(self):
        self.clear()
        outer = tk.Frame(self.root, bg=COLORS["bg"], padx=42, pady=28)
        outer.pack(fill="both", expand=True)
        tk.Label(outer, text="✦ QUIZQUEST", bg=COLORS["bg"], fg=COLORS["accent"],
                 font=("Segoe UI", 13, "bold")).pack(anchor="w")
        tk.Label(outer, text="Turn knowledge into\n your next high score.",
                 bg=COLORS["bg"], fg=COLORS["text"], justify="left",
                 font=("Segoe UI", 30, "bold")).pack(anchor="w", pady=(18, 8))
        tk.Label(outer, text="A little challenge. A little learning. A lot of progress.",
                 bg=COLORS["bg"], fg=COLORS["muted"], font=("Segoe UI", 11)).pack(anchor="w", pady=(0, 22))

        card = self.panel(outer)
        card.pack(fill="x")
        self.heading(card, "Ready, player?", "Choose a name and a topic. You get up to 10 questions per round.")
        tk.Label(card, text="PLAYER NAME", bg=COLORS["panel"], fg=COLORS["muted"],
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.name_entry = tk.Entry(card, font=("Segoe UI", 12), bg=COLORS["panel2"],
                                   fg=COLORS["text"], insertbackground="white", relief="flat")
        self.name_entry.insert(0, "Player")
        self.name_entry.pack(fill="x", ipady=9, pady=(5, 15))
        tk.Label(card, text="CHOOSE A CATEGORY", bg=COLORS["panel"], fg=COLORS["muted"],
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        categories = ["All"] + sorted({q["category"] for q in self.questions})
        self.category_box = ttk.Combobox(card, values=categories, state="readonly", font=("Segoe UI", 11))
        self.category_box.set("All")
        self.category_box.pack(fill="x", ipady=5, pady=(5, 18))
        self.style_button(card, "START QUIZ  →", self.start_quiz, COLORS["accent"], "#10231f").pack(fill="x", ipady=8)
        row = tk.Frame(outer, bg=COLORS["bg"])
        row.pack(fill="x", pady=18)
        self.style_button(row, "🏆  Leaderboard", self.show_leaderboard, COLORS["panel2"]).pack(side="left", expand=True, fill="x", padx=(0, 7))
        self.style_button(row, "ℹ  How to play", self.show_help, COLORS["panel2"]).pack(side="left", expand=True, fill="x", padx=(7, 0))
        tk.Label(outer, text="QUIZQUEST • Built with Python + Tkinter • Your scores stay on this device",
                 bg=COLORS["bg"], fg="#71839b", font=("Segoe UI", 8)).pack(side="bottom", pady=(10, 0))

    def style_button(self, parent, text, command, bg=None, fg=None):
        return tk.Button(parent, text=text, command=command, bg=bg or COLORS["panel2"],
                         fg=fg or COLORS["text"], activebackground=COLORS["accent"],
                         activeforeground="#10231f", relief="flat", bd=0,
                         font=("Segoe UI", 10, "bold"), cursor="hand2", padx=14, pady=10)

    def show_help(self):
        messagebox.showinfo("How to play", "1. Choose a player name and category.\n2. Answer up to 10 multiple-choice questions.\n3. Correct answers earn 10 points.\n4. Your best rounds are saved in the leaderboard.\n\nTip: You can replay a category to improve your score!")

    def start_quiz(self):
        name = self.name_entry.get().strip()
        self.player = name[:20] if name else "Player"
        self.category = self.category_box.get()
        if self.category != "All" and not any(q["category"] == self.category for q in self.questions):
            messagebox.showerror("No questions", "There are no questions in this category yet.")
            return
        if not self.questions:
            messagebox.showerror("No questions", "No valid questions found in data/questions.json.")
            return
        self.current_questions = pick_round(self.questions, self.category)
        self.index, self.score = 0, 0
        self.show_question()

    def show_question(self):
        self.clear()
        q = self.current_questions[self.index]
        outer = tk.Frame(self.root, bg=COLORS["bg"], padx=38, pady=28)
        outer.pack(fill="both", expand=True)
        top = tk.Frame(outer, bg=COLORS["bg"])
        top.pack(fill="x")
        tk.Label(top, text="✦ QUIZQUEST", bg=COLORS["bg"], fg=COLORS["accent"],
                 font=("Segoe UI", 11, "bold")).pack(side="left")
        tk.Label(top, text=f"QUESTION {self.index + 1}/{len(self.current_questions)}",
                 bg=COLORS["bg"], fg=COLORS["muted"], font=("Segoe UI", 10, "bold")).pack(side="right")
        progress = ttk.Progressbar(outer, maximum=len(self.current_questions), value=self.index)
        progress.pack(fill="x", pady=(16, 22))
        card = self.panel(outer)
        card.pack(fill="both", expand=True)
        tk.Label(card, text=q["category"].upper(), bg=COLORS["panel"], fg=COLORS["accent"],
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(card, text=q["question"], bg=COLORS["panel"], fg=COLORS["text"],
                 font=("Segoe UI", 19, "bold"), wraplength=650, justify="left").pack(anchor="w", pady=(12, 22))
        self.selected = tk.StringVar(value="")
        for option in q["options"]:
            rb = tk.Radiobutton(card, text=option, variable=self.selected, value=option,
                                bg=COLORS["panel2"], fg=COLORS["text"], selectcolor="#314964",
                                activebackground=COLORS["panel2"], activeforeground=COLORS["text"],
                                font=("Segoe UI", 11), anchor="w", padx=14, pady=11,
                                indicatoron=False, relief="flat", cursor="hand2")
            rb.pack(fill="x", pady=5)
        bottom = tk.Frame(outer, bg=COLORS["bg"])
        bottom.pack(fill="x", pady=(16, 0))
        tk.Label(bottom, text=f"SCORE  {self.score}", bg=COLORS["bg"], fg=COLORS["yellow"],
                 font=("Segoe UI", 11, "bold")).pack(side="left")
        self.style_button(bottom, "SUBMIT ANSWER  →", self.submit_answer, COLORS["accent"], "#10231f").pack(side="right")

    def submit_answer(self):
        answer = self.selected.get()
        if not answer:
            messagebox.showwarning("Choose an answer", "Select one option before continuing.")
            return
        q = self.current_questions[self.index]
        correct = answer == q["answer"]
        if correct:
            self.score += POINTS_PER_QUESTION
        self.show_feedback(correct, q)

    def show_feedback(self, correct, q):
        self.clear()
        outer = tk.Frame(self.root, bg=COLORS["bg"], padx=45, pady=45)
        outer.pack(fill="both", expand=True)
        card = self.panel(outer)
        card.pack(fill="both", expand=True)
        title = "Correct! +10 points 🎉" if correct else "Not quite — keep going!"
        color = COLORS["accent"] if correct else COLORS["yellow"]
        tk.Label(card, text=title, bg=COLORS["panel"], fg=color,
                 font=("Segoe UI", 24, "bold")).pack(anchor="w", pady=(10, 16))
        tk.Label(card, text=f"The correct answer is: {q['answer']}", bg=COLORS["panel"],
                 fg=COLORS["text"], font=("Segoe UI", 13, "bold")).pack(anchor="w")
        tk.Label(card, text=q["explanation"], bg=COLORS["panel"], fg=COLORS["muted"],
                 font=("Segoe UI", 11), wraplength=620, justify="left").pack(anchor="w", pady=(12, 30))
        label = "SEE RESULTS  →" if self.index == len(self.current_questions) - 1 else "NEXT QUESTION  →"
        self.style_button(card, label, self.next_question, COLORS["accent"], "#10231f").pack(anchor="e", fill="x", ipady=6)

    def next_question(self):
        self.index += 1
        if self.index >= len(self.current_questions):
            self.finish_quiz()
        else:
            self.show_question()

    def finish_quiz(self):
        total = len(self.current_questions) * POINTS_PER_QUESTION
        entry = make_score_entry(self.player, self.category, self.score, total,
                                 datetime.now().strftime("%Y-%m-%d %H:%M"))
        percent = entry["percent"]
        self.scores = add_score(self.scores, entry)
        try:
            save_json(SCORES_FILE, self.scores)
        except OSError:
            messagebox.showwarning("Score not saved", "Could not save your score to disk.")
        self.clear()
        outer = tk.Frame(self.root, bg=COLORS["bg"], padx=45, pady=38)
        outer.pack(fill="both", expand=True)
        card = self.panel(outer)
        card.pack(fill="both", expand=True)
        tk.Label(card, text="ROUND COMPLETE", bg=COLORS["panel"], fg=COLORS["accent"],
                 font=("Segoe UI", 11, "bold")).pack(anchor="w")
        tk.Label(card, text=f"Well played, {self.player}!", bg=COLORS["panel"], fg=COLORS["text"],
                 font=("Segoe UI", 26, "bold")).pack(anchor="w", pady=(12, 5))
        tk.Label(card, text=f"{self.score} / {total}", bg=COLORS["panel"], fg=COLORS["yellow"],
                 font=("Segoe UI", 36, "bold")).pack(anchor="w", pady=(10, 0))
        tk.Label(card, text=f"You got {percent}% of the points.", bg=COLORS["panel"],
                 fg=COLORS["muted"], font=("Segoe UI", 12)).pack(anchor="w", pady=(2, 20))
        if percent == 100:
            message = "Perfect round! You're a QuizQuest champion."
        elif percent >= 70:
            message = "Great work! Your knowledge is leveling up."
        elif percent >= 40:
            message = "Nice effort. A replay can help you beat this score."
        else:
            message = "Every round is practice. Give it another try!"
        tk.Label(card, text=message, bg=COLORS["panel"], fg=COLORS["text"],
                 font=("Segoe UI", 11), wraplength=600).pack(anchor="w", pady=(0, 24))
        self.style_button(card, "PLAY AGAIN", self.build_home, COLORS["accent"], "#10231f").pack(fill="x", ipady=5)
        self.style_button(card, "VIEW LEADERBOARD", self.show_leaderboard).pack(fill="x", pady=(9, 0), ipady=5)

    def show_leaderboard(self):
        self.clear()
        outer = tk.Frame(self.root, bg=COLORS["bg"], padx=38, pady=28)
        outer.pack(fill="both", expand=True)
        card = self.panel(outer)
        card.pack(fill="both", expand=True)
        self.heading(card, "🏆 Leaderboard", "Top 10 rounds (ranked by percentage) saved on this computer")
        if not self.scores:
            tk.Label(card, text="No scores yet. Play your first round!", bg=COLORS["panel"],
                     fg=COLORS["muted"], font=("Segoe UI", 12)).pack(anchor="w", pady=20)
        else:
            for rank, item in enumerate(self.scores[:10], start=1):
                line = tk.Frame(card, bg=COLORS["panel2"], padx=12, pady=9)
                line.pack(fill="x", pady=4)
                tk.Label(line, text=f"#{rank}", bg=COLORS["panel2"], fg=COLORS["yellow"],
                         font=("Segoe UI", 10, "bold"), width=4).pack(side="left")
                tk.Label(line, text=f"{item['name']}  •  {item['category']}", bg=COLORS["panel2"],
                         fg=COLORS["text"], font=("Segoe UI", 10)).pack(side="left")
                tk.Label(line, text=f"{item['score']}/{item['total']}", bg=COLORS["panel2"],
                         fg=COLORS["accent"], font=("Segoe UI", 10, "bold")).pack(side="right")
        self.style_button(card, "← BACK HOME", self.build_home).pack(fill="x", pady=(18, 0), ipady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizQuest(root)
    root.mainloop()
