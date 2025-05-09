import tkinter as tk
import random
from tkinter import messagebox

class PacmanMemoryFlip:
    def __init__(self, root):
        self.root = root
        self.root.title("Pac-Man Memory Flip")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        self.player_name = tk.StringVar()
        self.levels_unlocked = 1

        self.show_start_screen()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_start_screen(self):
        self.clear()
        shadow = tk.Label(self.root, text="MEMORY FLIP",
                          font=("Courier New", 48, "bold"), fg="black", bg="black")
        shadow.place(relx=0.5, rely=0.2, anchor="center", x=3, y=3)

        title = tk.Label(self.root, text="MEMORY FLIP",
                         font=("Courier New", 48, "bold"), fg="#FFFF00", bg="black")
        title.place(relx=0.5, rely=0.2, anchor="center")

        start_btn = tk.Button(self.root, text="START",
                              font=("Courier New", 20, "bold"),
                              bg="#00FF00", fg="black",
                              activebackground="#00CC00",
                              relief="flat", padx=30, pady=10,
                              command=self.show_name_screen)
        start_btn.place(relx=0.5, rely=0.5, anchor="center")

    def show_name_screen(self):
        self.clear()

        tk.Label(self.root, text="ENTER YOUR NAME",
                 font=("Courier New", 22, "bold"),
                 fg="#39FF14", bg="black").pack(pady=(120, 10))

        name_entry = tk.Entry(self.root, textvariable=self.player_name,
                              font=("Courier New", 20), width=24,
                              bg="black", fg="cyan", insertbackground="white",
                              relief="solid", bd=2, justify="center")
        name_entry.pack(ipady=10)

        play_btn = tk.Button(self.root, text="PLAY",
                             font=("Courier New", 18, "bold"),
                             bg="#FF3131", fg="white",
                             relief="flat", padx=30, pady=8,
                             activebackground="#CC0000",
                             command=self.show_level_select)
        play_btn.pack(pady=30)

    def show_level_select(self):
        self.clear()

        tk.Label(self.root, text="SELECT LEVEL",
                 font=("Courier New", 36, "bold"),
                 fg="#FFFF00", bg="black").pack(pady=(40, 20))

        grid_frame = tk.Frame(self.root, bg="black")
        grid_frame.pack(pady=20)

        for level in range(1, 7):
            row = (level - 1) // 3
            col = (level - 1) % 3
            is_unlocked = level <= self.levels_unlocked

            if is_unlocked:
                btn = tk.Button(grid_frame, text=f"LEVEL {level}",
                                font=("Courier New", 16, "bold"),
                                bg="#00FF00", fg="black",
                                width=14, height=2,
                                relief="flat",
                                activebackground="#00CC00",
                                command=lambda l=level: self.launch_game_screen(l))
            else:
                btn = tk.Button(grid_frame, text="🔒",
                                font=("Courier New", 16, "bold"),
                                bg="#444444", fg="white",
                                width=14, height=2,
                                relief="flat", state=tk.DISABLED)

            btn.grid(row=row, column=col, padx=25, pady=15)

        back_btn = tk.Button(self.root, text="← BACK",
                             font=("Courier New", 14),
                             bg="#FF3131", fg="white",
                             padx=20, pady=5, relief="flat",
                             activebackground="#CC0000",
                             command=self.show_name_screen)
        back_btn.pack(pady=30)

    def launch_game_screen(self, level):
        self.clear()
        self.current_level = level
        self.score = 0
        self.chances = 6
        self.matched = []
        self.flipped = []
        self.locked = False

        # Title
        tk.Label(self.root, text=f"LEVEL {level}",
                 font=("Courier New", 36, "bold"),
                 fg="#FFFF00", bg="black").pack(pady=(30, 10))

        # Pac-Man dots
        tk.Label(self.root, text="· " * 30,
                 font=("Courier New", 14), fg="#FFFF00", bg="black").pack()

        # Info Panel
        tk.Label(self.root, text=f"PLAYER: {self.player_name.get()}",
                 font=("Courier New", 14, "bold"),
                 fg="white", bg="black").pack(pady=(5, 0))

        self.score_label = tk.Label(self.root, text=f"SCORE: {self.score}",
                                    font=("Courier New", 14, "bold"), fg="white", bg="black")
        self.score_label.pack()

        self.chances_label = tk.Label(self.root, text=f"CHANCES: {self.chances}",
                                      font=("Courier New", 14, "bold"), fg="red", bg="black")
        self.chances_label.pack(pady=(0, 10))

        # Card setup
        values = [1, 1, 2, 2]
        random.shuffle(values)
        self.card_values = values
        self.tiles = {}

        grid_frame = tk.Frame(self.root, bg="black")
        grid_frame.pack(pady=20)

        idx = 0
        for i in range(2):
            for j in range(2):
                btn = tk.Button(grid_frame, text="?", width=6, height=3,
                                font=("Courier New", 20, "bold"),
                                bg="#1E90FF", fg="white", relief="ridge", bd=4,
                                command=lambda i=i, j=j: self.flip_tile(i, j))
                btn.grid(row=i, column=j, padx=20, pady=20)
                self.tiles[(i, j)] = {"btn": btn, "val": values[idx]}
                idx += 1

        tk.Label(self.root, text="· " * 30,
                 font=("Courier New", 14), fg="#FFFF00", bg="black").pack(side="bottom", pady=(0, 20))

    def flip_tile(self, i, j):
        if self.locked or (i, j) in self.matched or (i, j) in self.flipped:
            return

        val = self.tiles[(i, j)]["val"]
        btn = self.tiles[(i, j)]["btn"]
        btn.config(text=str(val), bg="#FFD700")  # Gold

        self.flipped.append((i, j))

        if len(self.flipped) == 2:
            self.locked = True
            self.root.after(800, self.check_match)

    def check_match(self):
        (i1, j1), (i2, j2) = self.flipped
        v1 = self.tiles[(i1, j1)]["val"]
        v2 = self.tiles[(i2, j2)]["val"]

        if v1 == v2:
            self.matched.extend(self.flipped)
            self.score += 10
        else:
            for i, j in self.flipped:
                self.tiles[(i, j)]["btn"].config(text="?", bg="#1E90FF")
            self.chances -= 1

        self.flipped = []
        self.locked = False
        self.update_labels()

        if len(self.matched) == 4:
            self.show_pacman_win_popup()
        elif self.chances == 0:
            self.show_pacman_game_over()

    def update_labels(self):
        self.score_label.config(text=f"SCORE: {self.score}")
        self.chances_label.config(text=f"CHANCES: {self.chances}")

    def show_pacman_win_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Level Complete")
        popup.geometry("320x200")
        popup.configure(bg="black")

        tk.Label(popup, text="LEVEL COMPLETE!",
                 font=("Courier New", 18, "bold"), fg="#FFFF00", bg="black").pack(pady=20)
        tk.Label(popup, text=f"SCORE: {self.score}",
                 font=("Courier New", 14), fg="white", bg="black").pack()

        tk.Button(popup, text="NEXT LEVEL", font=("Courier New", 12, "bold"),
                  bg="#00FF00", fg="black",
                  command=lambda: self.advance_level(popup)).pack(pady=10)

    def show_pacman_game_over(self):
        messagebox.showinfo("GAME OVER", "You're out of chances!")
        self.show_level_select()

    def advance_level(self, popup):
        popup.destroy()
        if self.current_level == self.levels_unlocked:
            self.levels_unlocked += 1
        next_level = self.current_level + 1
        if next_level <= 6:
            self.launch_game_screen(next_level)
        else:
            self.show_level_select()

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    app = PacmanMemoryFlip(root)
    root.mainloop()
