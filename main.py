import tkinter as tk
from tkinter import messagebox
import random


class Flashcards:

    def __init__(self, filename):
        self.cards = []

        self.turn = 0
        self.a = ""
        self.b = ""
        with open(filename, encoding="utf-8") as f:
            for line in f:
                if self.turn == 0:
                    self.a = line.strip()
                    self.turn+=1
                elif self.turn == 1:
                    self.b = line.strip()
                    self.cards.append((self.a, self.b))
                    self.turn = 0


        random.shuffle(self.cards)

        self.current = None
        self.answer_visible = False

        self.good = 0
        self.bad = 0

        self.root = tk.Tk()
        self.root.title("Fiszki")
        self.root.geometry("900x500")

        self.label = tk.Label(
            self.root,
            text="",
            wraplength=850,
            font=("Arial", 18),
            justify="center"
        )
        self.label.pack(expand=True)

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        self.show_btn = tk.Button(
            frame,
            text="Pokaż odpowiedź",
            command=self.show_answer,
            width=20
        )
        self.show_btn.grid(row=0, column=0, padx=5)

        self.good_btn = tk.Button(
            frame,
            text="✔ Wiedziałem",
            command=self.good_answer,
            width=15,
            state="disabled"
        )
        self.good_btn.grid(row=0, column=1)

        self.bad_btn = tk.Button(
            frame,
            text="✘ Nie wiedziałem",
            command=self.bad_answer,
            width=15,
            state="disabled"
        )
        self.bad_btn.grid(row=0, column=2)

        self.stats = tk.Label(
            self.root,
            text="Poprawne: 0    Błędne: 0",
            font=("Arial", 12)
        )
        self.stats.pack()

        self.next_card()

        self.root.mainloop()

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
                 "\n\n----------------------\n\n" +
                 self.current[1]
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


Flashcards("fiszki.txt")