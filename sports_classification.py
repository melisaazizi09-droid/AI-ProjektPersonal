from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from sports import predict_sport


# ================= COLORS =================

BG = "#0B1220"
CARD = "#17243A"
CARD2 = "#1D2D46"
ACCENT = "#22D3EE"
WHITE = "#F8FAFC"
MUTED = "#94A3B8"
GREEN = "#34D399"
RED = "#FB7185"

SPORTS = [
    "Football",
    "Basketball",
    "Tennis",
    "Volleyball",
    "Baseball",
    "Golf"
]

FACTS = {
    "Football": "Football is played by two teams of 11 players.",
    "Basketball": "Basketball was invented in 1891.",
    "Tennis": "Tennis can be played in singles or doubles.",
    "Volleyball": "Volleyball was invented in 1895.",
    "Baseball": "Baseball is popular in the USA and Japan.",
    "Golf": "Golf is played by hitting a ball into holes."
}


# ================= APPLICATION =================

class SportsApp:

    def __init__(self, root):

        self.root = root
        self.root.title("SPORTIFY AI")
        self.root.geometry("1000x780")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.image_path = None
        self.photo = None
        self.score = 0
        self.rounds = 0
        self.answered = False

        self.answer = tk.StringVar(
            value="Select a sport"
        )

        self.build_ui()

    # ================= HELPERS =================

    def label(self, parent, text, size=11,
              color=WHITE, bold=False, bg=CARD):

        return tk.Label(
            parent,
            text=text,
            font=("Segoe UI", size,
                  "bold" if bold else "normal"),
            fg=color,
            bg=bg
        )

    def card(self, parent, bg=CARD):

        return tk.Frame(
            parent,
            bg=bg,
            highlightbackground="#293B55",
            highlightthickness=1
        )

    def button(self, parent, text, command):

        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 11, "bold"),
            bg=ACCENT,
            fg=BG,
            activebackground="#67E8F9",
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=12
        )

    # ================= INTERFACE =================

    def build_ui(self):

        # HEADER

        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=30, pady=22)

        tk.Label(
            header,
            text="SPORTIFY",
            font=("Segoe UI", 27, "bold"),
            fg=ACCENT,
            bg=BG
        ).pack(side="left")

        tk.Label(
            header,
            text="AI SPORTS BALL CLASSIFIER",
            font=("Segoe UI", 10, "bold"),
            fg=MUTED,
            bg=BG
        ).pack(side="left", padx=15, pady=12)

        tk.Label(
            header,
            text="● AI SYSTEM ONLINE",
            font=("Segoe UI", 10, "bold"),
            fg=GREEN,
            bg=BG
        ).pack(side="right", pady=12)

        # STATISTICS

        stats = tk.Frame(self.root, bg=BG)
        stats.pack(fill="x", padx=30, pady=(0, 20))

        self.score_var = tk.StringVar(value="0")
        self.round_var = tk.StringVar(value="0")
        self.accuracy_var = tk.StringVar(value="0%")

        self.stat_card(stats, "🏆", "TOTAL SCORE",
                       self.score_var)

        self.stat_card(stats, "🎯", "ROUNDS PLAYED",
                       self.round_var)

        self.stat_card(stats, "📊", "ACCURACY",
                       self.accuracy_var)

        # MAIN CONTENT

        content = tk.Frame(self.root, bg=BG)
        content.pack(fill="both", expand=True, padx=30)

        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)

        # IMAGE PANEL

        left = self.card(content)
        left.grid(
            row=0, column=0,
            sticky="nsew", padx=(0, 10)
        )

        self.label(
            left, "IMAGE ANALYSIS", 15, WHITE, True
        ).pack(anchor="w", padx=20, pady=(20, 5))

        self.label(
            left, "Upload your favorite sports ball",
            10, MUTED
        ).pack(anchor="w", padx=20, pady=(0, 15))

        image_box = tk.Frame(
            left, bg=CARD2,
            width=430, height=300
        )

        image_box.pack(padx=18, pady=5)
        image_box.pack_propagate(False)

        self.image_label = tk.Label(
            image_box,
            text="⚽\n\nNO IMAGE SELECTED\nUpload a sports ball",
            font=("Segoe UI", 15),
            fg=MUTED,
            bg=CARD2
        )

        self.image_label.pack(
            expand=True,
            fill="both"
        )

        self.upload_btn = self.button(
            left,
            "＋  UPLOAD IMAGE",
            self.choose_image
        )

        self.upload_btn.pack(
            padx=20, pady=20, fill="x"
        )

        self.file_label = self.label(
            left, "JPG • PNG • JPEG • WEBP",
            9, MUTED
        )

        self.file_label.pack(pady=(0, 15))

        # GAME PANEL

        right = self.card(content)

        right.grid(
            row=0, column=1,
            sticky="nsew", padx=(10, 0)
        )

        self.label(
            right, "GUESS THE BALL", 15, WHITE, True
        ).pack(anchor="w", padx=20, pady=(20, 5))

        self.label(
            right, "Can you identify the sport before AI?",
            10, MUTED
        ).pack(anchor="w", padx=20, pady=(0, 15))

        self.label(
            right, "🏀", 45, ACCENT
        ).pack(pady=5)

        self.label(
            right, "WHICH SPORT IS THIS BALL FROM?",
            11, WHITE, True
        ).pack(pady=12)

        self.menu = tk.OptionMenu(
            right, self.answer, *SPORTS
        )

        self.menu.config(
            bg=CARD2,
            fg=WHITE,
            activebackground=ACCENT,
            activeforeground=BG,
            font=("Segoe UI", 11),
            relief="flat",
            bd=0,
            highlightthickness=0,
            width=23,
            pady=8
        )

        self.menu["menu"].config(
            bg=CARD2,
            fg=WHITE,
            font=("Segoe UI", 10)
        )

        self.menu.pack(pady=8)

        self.check_btn = self.button(
            right,
            "CHECK MY ANSWER",
            self.check_answer
        )

        self.check_btn.pack(
            padx=25, pady=15, fill="x"
        )

        self.check_btn.config(state="disabled")

        # RESULT

        result_box = tk.Frame(
            right,
            bg=CARD2,
            padx=15,
            pady=15
        )

        result_box.pack(
            fill="x", padx=18, pady=10
        )

        self.label(
            result_box, "AI PREDICTION",
            9, MUTED, True, CARD2
        ).pack(anchor="w")

        self.result_label = self.label(
            result_box, "Waiting for image...",
            17, ACCENT, True, CARD2
        )

        self.result_label.pack(
            anchor="w", pady=8
        )

        self.confidence_label = self.label(
            result_box, "Confidence: --",
            10, MUTED, False, CARD2
        )

        self.confidence_label.pack(anchor="w")

        self.bar = tk.Canvas(
            result_box,
            height=10,
            bg="#334155",
            highlightthickness=0
        )

        self.bar.pack(fill="x", pady=(12, 0))

        self.feedback = self.label(
            right, "Upload an image to start playing!",
            10, MUTED
        )

        self.feedback.pack(pady=10)

        # FACT CARD

        fact = self.card(self.root)

        fact.pack(
            fill="x", padx=30, pady=20
        )

        self.label(
            fact, "💡  DID YOU KNOW?",
            12, ACCENT, True
        ).pack(anchor="w", padx=18, pady=(12, 5))

        self.fact_label = self.label(
            fact,
            "Interesting sports facts will appear here.",
            10, MUTED
        )

        self.fact_label.pack(
            anchor="w", padx=18, pady=(0, 14)
        )

        tk.Label(
            self.root,
            text="SPORTIFY AI  •  POWERED BY TENSORFLOW",
            font=("Segoe UI", 8),
            fg="#64748B",
            bg=BG
        ).pack(pady=(0, 8))

    # ================= STAT CARDS =================

    def stat_card(self, parent, icon, title, variable):

        box = self.card(parent)
        box.pack(
            side="left",
            expand=True,
            fill="x",
            padx=6
        )

        tk.Label(
            box,
            text=icon,
            font=("Segoe UI", 22),
            bg=CARD,
            fg=ACCENT
        ).pack(side="left", padx=15, pady=12)

        info = tk.Frame(box, bg=CARD)
        info.pack(side="left", pady=10)

        tk.Label(
            info,
            text=title,
            font=("Segoe UI", 8, "bold"),
            fg=MUTED,
            bg=CARD
        ).pack(anchor="w")

        tk.Label(
            info,
            textvariable=variable,
            font=("Segoe UI", 20, "bold"),
            fg=WHITE,
            bg=CARD
        ).pack(anchor="w")

    # ================= UPLOAD =================

    def choose_image(self):

        path = filedialog.askopenfilename(
            title="Choose Sports Ball Image",
            filetypes=[
                ("Images", "*.jpg *.jpeg *.png *.bmp *.webp")
            ]
        )

        if not path:
            return

        try:

            image = Image.open(path).convert("RGB")
            image.thumbnail((430, 300))

            self.photo = ImageTk.PhotoImage(image)

            self.image_label.config(
                image=self.photo,
                text=""
            )

            self.image_path = path
            self.answered = False

            self.file_label.config(
                text=Path(path).name,
                fg=ACCENT
            )

            self.answer.set("Select a sport")

            self.result_label.config(
                text="Waiting for your guess...",
                fg=ACCENT
            )

            self.confidence_label.config(
                text="Confidence: Hidden"
            )

            self.feedback.config(
                text="Choose your answer before AI reveals the result.",
                fg=MUTED
            )

            self.fact_label.config(
                text="Make your guess to discover a sports fact!"
            )

            self.bar.delete("all")

            self.check_btn.config(
                state="normal",
                text="CHECK MY ANSWER"
            )

        except Exception as error:

            messagebox.showerror(
                "Image Error", str(error)
            )

    # ================= AI PREDICTION =================

    def check_answer(self):

        if not self.image_path or self.answered:
            return

        guess = self.answer.get()

        if guess not in SPORTS:

            messagebox.showwarning(
                "Select Sport",
                "Please select a sport first!"
            )

            return

        self.check_btn.config(
            state="disabled",
            text="ANALYZING..."
        )

        self.root.update_idletasks()

        try:

            result = predict_sport(self.image_path)

            sport = result.get(
                "sport_class",
                result.get("sport")
            )

            confidence = float(result["confidence"])

            if not sport:
                raise ValueError("No sport detected.")

            self.rounds += 1
            self.answered = True

            if guess.lower() == sport.lower():

                self.score += 1

                self.result_label.config(
                    text=f"✓ {sport}",
                    fg=GREEN
                )

                self.feedback.config(
                    text="EXCELLENT! CORRECT ANSWER! +1 POINT",
                    fg=GREEN
                )

            else:

                self.result_label.config(
                    text=f"✗ {sport}",
                    fg=RED
                )

                self.feedback.config(
                    text=f"Not quite! Correct answer: {sport}",
                    fg=RED
                )

            confidence = max(0, min(1, confidence))

            self.confidence_label.config(
                text=f"AI Confidence: {confidence:.2%}"
            )

            self.bar.delete("all")

            self.bar.update_idletasks()

            width = self.bar.winfo_width()

            self.bar.create_rectangle(
                0, 0,
                width * confidence, 10,
                fill=GREEN if confidence >= 0.7 else ACCENT,
                outline=""
            )

            self.fact_label.config(
                text=FACTS.get(
                    sport,
                    "Discover more about sports!"
                )
            )

            self.score_var.set(str(self.score))
            self.round_var.set(str(self.rounds))

            accuracy = self.score / self.rounds * 100

            self.accuracy_var.set(
                f"{accuracy:.0f}%"
            )

        except Exception as error:

            messagebox.showerror(
                "Prediction Error", str(error)
            )

        finally:

            self.check_btn.config(
                text="CHECK MY ANSWER",
                state="disabled" if self.answered else "normal"
            )


# ================= MAIN =================

def main():

    root = tk.Tk()
    app = SportsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

