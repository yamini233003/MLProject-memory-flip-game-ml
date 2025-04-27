
import tkinter as tk
import random
import time

class MemoryFlipGame:
    def __init__(self, root, grid_size=4):
        self.root = root
        self.root.title("Memory Flip Game")
        self.grid_size = grid_size
        self.symbols = list(range(1, (grid_size*grid_size)//2 + 1)) * 2
        random.shuffle(self.symbols)
        self.buttons = {}
        self.first_card = None
        self.second_card = None
        self.mistakes = 0
        self.start_time = time.time()
        self.create_widgets()

    def create_widgets(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                btn = tk.Button(self.root, text="", width=6, height=3, command=lambda r=r, c=c: self.reveal(r, c))
                btn.grid(row=r, column=c)
                self.buttons[(r, c)] = btn
        self.status = tk.Label(self.root, text="Mistakes: 0")
        self.status.grid(row=self.grid_size, column=0, columnspan=self.grid_size)

    def reveal(self, r, c):
        btn = self.buttons[(r, c)]
        idx = r * self.grid_size + c
        btn.config(text=str(self.symbols[idx]), state="disabled")

        if not self.first_card:
            self.first_card = (r, c)
        elif not self.second_card:
            self.second_card = (r, c)
            self.root.after(500, self.check_match)

    def check_match(self):
        r1, c1 = self.first_card
        r2, c2 = self.second_card
        idx1 = r1 * self.grid_size + c1
        idx2 = r2 * self.grid_size + c2

        if self.symbols[idx1] != self.symbols[idx2]:
            self.buttons[(r1, c1)].config(text="", state="normal")
            self.buttons[(r2, c2)].config(text="", state="normal")
            self.mistakes += 1
            self.status.config(text=f"Mistakes: {self.mistakes}")

        self.first_card = None
        self.second_card = None

        if all(btn['state'] == 'disabled' for btn in self.buttons.values()):
            self.end_game()

    def end_game(self):
        total_time = round(time.time() - self.start_time)
        tk.messagebox.showinfo("Game Over", f"You completed the game in {total_time} seconds with {self.mistakes} mistakes!")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryFlipGame(root)
    root.mainloop()
