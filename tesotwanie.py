import tkinter as tk
from tkinter import messagebox
import random


class Flashcards:

    def __init__(self, filename):
        self.cards = []

        self.turn = 0
        self.q = ""
        self.a = ""
        self.b = ""
        self.c = ""
        self.d = ""
        self.odp = ""

        with open(filename, encoding="utf-8") as f:
            for line in f:
                if self.turn == 0:
                    self.q = line.strip()
                    self.turn += 1
                elif self.turn == 1:
                    self.a = line.strip()
                    self.turn += 1
                elif self.turn == 2:
                    self.b = line.strip()
                    self.turn += 1
                elif self.turn == 3:
                    self.c = line.strip()
                    self.turn += 1
                elif self.turn == 4:
                    self.d = line.strip()
                    self.turn += 1
                elif self.turn == 5:
                    self.odp = line.strip()
                    full_text = f"{self.q}\n\n {self.a}\n {self.b}\n {self.c}\n {self.d}"
                    self.cards.append((full_text, self.odp))
                    self.turn = 0

        random.shuffle(self.cards)

        self.current = None
        self.answer_visible = False
        self.good = 0
        self.bad = 0

        # ==================== TWORZENIE GUI ====================
        self.root = tk.Tk()
        self.root.title("Fiszki - Tryb Ciemny")
        self.root.geometry("1000x650")
        self.root.configure(bg="#1e1e1e")          # <-- ciemne tło okna

        # Główna etykieta z pytaniem
        self.label = tk.Label(
            self.root,
            text="",
            wraplength=950,
            font=("Arial", 18),
            justify="left",
            bg="#1e1e1e",           # tło etykiety
            fg="#ffffff",           # biały tekst
            padx=20,
            pady=20
        )
        self.label.pack(expand=True, fill="both")

        # Ramka na przyciski
        frame = tk.Frame(self.root, bg="#1e1e1e")
        frame.pack(pady=20)

        # Przyciski
        btn_style = {"font": ("Arial", 12), "width": 20, "pady": 8}

        self.show_btn = tk.Button(
            frame,
            text="Pokaż odpowiedź",
            command=self.show_answer,
            **btn_style,
            bg="#333333",
            fg="#ffffff",
            activebackground="#555555"
        )
        self.show_btn.grid(row=0, column=0, padx=10)

        self.good_btn = tk.Button(
            frame,
            text="✔ Wiedziałem",
            command=self.good_answer,
            **btn_style,
            bg="#006400",           # ciemna zieleń
            fg="#ffffff",
            activebackground="#008000",
            state="disabled"
        )
        self.good_btn.grid(row=0, column=1, padx=10)

        self.bad_btn = tk.Button(
            frame,
            text="✘ Nie wiedziałem",
            command=self.bad_answer,
            **btn_style,
            bg="#8B0000",           # ciemna czerwień
            fg="#ffffff",
            activebackground="#B22222",
            state="disabled"
        )
        self.bad_btn.grid(row=0, column=2, padx=10)

        # Statystyki
        self.stats = tk.Label(
            self.root,
            text="Poprawne: 0    Błędne: 0",
            font=("Arial", 14),
            bg="#1e1e1e",
            fg="#00ffcc"            # ładny cyjan
        )
        self.stats.pack(pady=15)

        self.next_card()
        self.root.mainloop()

    # ------------------- Pozostałe metody bez zmian -------------------
    def next_card(self):
        if len(self.cards) == 0:
            messagebox.showinfo(
                "Koniec",
                f"Koniec fiszek!\n\n"
                f"Poprawne: {self.good}\n"
                f"Błędne: {self.bad}"
            )
            self.root.destroy()
            return

        self.current = self.cards.pop()
        self.answer_visible = False

        self.label.config(text=self.current[0])

        self.show_btn.config(state="normal")
        self.good_btn.config(state="disabled")
        self.bad_btn.config(state="disabled")

    def show_answer(self):
        self.label.config(
            text=self.current[0] +
                 "\n\n" + "═"*60 + "\n\n" +
                 f"Poprawna odpowiedź →  {self.current[1]}"
        )

        self.show_btn.config(state="disabled")
        self.good_btn.config(state="normal")
        self.bad_btn.config(state="normal")

    def good_answer(self):
        self.good += 1
        self.update_stats()
        self.next_card()

    def bad_answer(self):
        self.bad += 1
        self.cards.insert(0, self.current)
        self.update_stats()
        self.next_card()

    def update_stats(self):
        self.stats.config(
            text=f"Poprawne: {self.good}    Błędne: {self.bad}"
        )


Flashcards("fiszki_testowanie.txt")