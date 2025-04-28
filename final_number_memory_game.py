
import tkinter as tk
import random
from tkinter import messagebox, simpledialog

# Number set for cards (1-8, doubled for pairs)
numbers = list(range(1, 9)) * 2

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title('Number Memory Flip Game')
        self.root.configure(bg='#f0f0f5')  # Elegant light background

        # Ask username
        self.username = simpledialog.askstring('Welcome', 'Enter your name:')
        if not self.username:
            self.username = 'Player'

        self.buttons = []
        self.flipped = []
        self.matched = []
        self.score = 0
        self.chances = 20  # Total chances

        self.top_frame = tk.Frame(self.root, bg='#f0f0f5')
        self.top_frame.pack(pady=10)

        self.score_label = tk.Label(self.top_frame, text=f'Score: {self.score}', font=('Helvetica', 16, 'bold'), bg='#f0f0f5', fg='#333366')
        self.score_label.grid(row=0, column=0, padx=10)

        self.username_label = tk.Label(self.top_frame, text=f'Hello, {self.username}!', font=('Helvetica', 16, 'bold'), bg='#f0f0f5', fg='#666699')
        self.username_label.grid(row=0, column=1, padx=10)

        self.chances_label = tk.Label(self.top_frame, text=f'Chances Left: {self.chances}', font=('Helvetica', 16, 'bold'), bg='#f0f0f5', fg='#cc3300')
        self.chances_label.grid(row=0, column=2, padx=10)

        self.restart_button = tk.Button(self.root, text='Restart Game', font=('Helvetica', 12, 'bold'), bg='#333366', fg='white', command=self.restart)
        self.restart_button.pack(pady=5)

        self.frame = tk.Frame(self.root, bg='#f0f0f5')
        self.frame.pack(pady=20)

        self.setup()

    def setup(self):
        random.shuffle(numbers)
        for i in range(4):
            row = []
            for j in range(4):
                btn = tk.Button(self.frame, text='', width=6, height=3, font=('Helvetica', 20, 'bold'), bg='white', fg='#333366',
                                relief='raised', command=lambda i=i, j=j: self.flip(i, j))
                btn.grid(row=i, column=j, padx=10, pady=10)
                row.append(btn)
            self.buttons.append(row)

    def flip(self, i, j):
        if (i, j) in self.matched or (i, j) in self.flipped or self.chances <= 0:
            return

        self.buttons[i][j].config(text=str(numbers[i*4 + j]), bg='#ccddff')
        self.flipped.append((i, j))

        if len(self.flipped) == 2:
            self.root.after(700, self.check)

    def check(self):
        (i1, j1), (i2, j2) = self.flipped
        if numbers[i1*4 + j1] == numbers[i2*4 + j2]:
            self.matched.extend(self.flipped)
            self.score += 10
        else:
            self.buttons[i1][j1].config(text='', bg='white')
            self.buttons[i2][j2].config(text='', bg='white')

        self.chances -= 1
        self.flipped = []
        self.update_labels()

        if len(self.matched) == 16:
            messagebox.showinfo('Congratulations!', f'Great job, {self.username}!\nYour final score: {self.score}')
            self.restart()

        elif self.chances == 0:
            messagebox.showinfo('Game Over', f'Sorry {self.username}, you are out of chances!\nYour final score: {self.score}')
            self.restart()

    def update_labels(self):
        self.score_label.config(text=f'Score: {self.score}')
        self.chances_label.config(text=f'Chances Left: {self.chances}')

    def restart(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.buttons.clear()
        self.flipped.clear()
        self.matched.clear()
        self.score = 0
        self.chances = 20
        self.update_labels()
        self.setup()

if __name__ == '__main__':
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
