import tkinter as tk
import random
import time
from tkinter import messagebox

class MemoryFlipApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Flip")
        self.root.geometry("800x600")
        self.root.configure(bg="#a8ddf0")

        self.player_name = tk.StringVar()
        self.levels_unlocked = 1

        self.show_start_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_start_screen(self):
        self.clear_screen()

        title = tk.Label(self.root, text="Memory Flip", font=("Comic Sans MS", 48, "bold"), bg="#a8ddf0", fg="black")
        title.pack(pady=(120, 40))

        start_btn = tk.Button(self.root, text="START", font=("Comic Sans MS", 20, "bold"), bg="#00c897", fg="white",
                              padx=30, pady=10, relief="flat", activebackground="#00a67e",
                              command=self.show_name_screen)
        start_btn.pack()

    def show_name_screen(self):
        self.clear_screen()

        label = tk.Label(self.root, text="Enter Your Name:", font=("Comic Sans MS", 18), bg="#a8ddf0", fg="black")
        label.pack(pady=(150, 10))

        name_entry = tk.Entry(self.root, textvariable=self.player_name, font=("Comic Sans MS", 16), width=24,
                              justify="center", bg="white", bd=2, relief="solid")
        name_entry.pack(pady=(0, 20), ipady=6)

        play_btn = tk.Button(self.root, text="Play", font=("Comic Sans MS", 18, "bold"), bg="#00c897", fg="white",
                             padx=20, pady=8, relief="flat", command=self.show_level_select_screen)
        play_btn.pack()

    def show_level_select_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Select Level", font=("Comic Sans MS", 36, "bold"), fg="black", bg="#a8ddf0")\
            .pack(pady=(20, 10))

        main_frame = tk.Frame(self.root, bg="#a8ddf0")
        main_frame.pack(expand=True, fill="both", pady=5)

        canvas = tk.Canvas(main_frame, bg="#a8ddf0", highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        scroll_frame = tk.Frame(canvas, bg="#a8ddf0")
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scroll_frame.bind("<Configure>", on_frame_configure)

        total_levels = 15
        for level in range(1, total_levels + 1):
            row = (level - 1) // 4
            col = (level - 1) % 4
            is_unlocked = level <= self.levels_unlocked

            if is_unlocked:
                btn = tk.Button(scroll_frame, text=f"Level {level}", font=("Comic Sans MS", 16, "bold"),
                                bg="#00c897", fg="white", width=12, height=2, relief="flat",
                                command=lambda l=level: self.start_game_screen(l))
            else:
                btn = tk.Button(scroll_frame, text="🔒", font=("Comic Sans MS", 16, "bold"), bg="#cccccc", fg="white",
                                width=12, height=2, relief="flat", state=tk.DISABLED)

            btn.grid(row=row, column=col, padx=20, pady=15)

        # Back button pinned below scroll area
        back_btn = tk.Button(self.root, text="← Back", font=("Comic Sans MS", 14), bg="#9999ff", fg="white",
                            padx=20, pady=5, relief="flat", command=self.show_name_screen)
        back_btn.pack(pady=10)


    def start_game_screen(self, level):
        self.clear_screen()
        GameScreen(self, level)

    def unlock_next_level(self, level_completed):
        if level_completed >= self.levels_unlocked and level_completed < 6:
            self.levels_unlocked = level_completed + 1
        self.show_level_select_screen()


class GameScreen:
    def __init__(self, app, level):
        self.app = app
        self.root = app.root
        self.level = level
        self.player_name = app.player_name.get()

        self.frame = tk.Frame(self.root, bg="#a8ddf0")
        self.frame.pack(expand=True, fill="both")

        self.score = 0
        self.matched = []
        self.flipped = []
        self.locked = False
        self.start_time = time.time()

        self.grid_size = 2 + (level - 1)
        self.total_tiles = self.grid_size ** 2
        if self.total_tiles % 2 != 0:
            self.total_tiles -= 1
        self.chances = self.total_tiles + 2

        self.card_values = list(range(1, self.total_tiles // 2 + 1)) * 2
        random.shuffle(self.card_values)

        self.create_ui()

    def create_ui(self):
        top = tk.Frame(self.frame, bg="#a8ddf0")
        top.pack(pady=10)

        tk.Label(top, text=f"Player: {self.player_name}", font=("Comic Sans MS", 14, "bold"),
                 bg="#a8ddf0", fg="black").pack(side="left", padx=20)

        self.score_label = tk.Label(top, text=f"Score: {self.score}", font=("Comic Sans MS", 14, "bold"),
                                    bg="#a8ddf0", fg="black")
        self.score_label.pack(side="left", padx=20)

        self.chances_label = tk.Label(top, text=f"Chances: {self.chances}", font=("Comic Sans MS", 14, "bold"),
                                      bg="#a8ddf0", fg="black")
        self.chances_label.pack(side="left", padx=20)

        self.tile_frame = tk.Frame(self.frame, bg="#a8ddf0")
        self.tile_frame.pack(pady=30)

        self.buttons = []
        index = 0
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                if index >= self.total_tiles:
                    break
                btn = tk.Button(self.tile_frame, text="", width=6, height=3,
                                font=("Comic Sans MS", 20, "bold"), bg="white", fg="black",
                                relief="raised", command=lambda i=i, j=j: self.flip_tile(i, j))
                btn.grid(row=i, column=j, padx=10, pady=10)
                row.append(btn)
                index += 1
            self.buttons.append(row)

    def flip_tile(self, i, j):
        if self.locked or (i, j) in self.matched or (i, j) in self.flipped or self.chances == 0:
            return
        idx = i * self.grid_size + j
        try:
            value = self.card_values[idx]
        except IndexError:
            return
        self.buttons[i][j].config(text=str(value), bg="#d6eaff")
        self.flipped.append((i, j))

        if len(self.flipped) == 2:
            self.locked = True
            self.root.after(800, self.check_match)

    def check_match(self):
        (i1, j1), (i2, j2) = self.flipped
        idx1 = i1 * self.grid_size + j1
        idx2 = i2 * self.grid_size + j2

        if self.card_values[idx1] == self.card_values[idx2]:
            self.matched.extend(self.flipped)
            self.score += 10
        else:
            self.buttons[i1][j1].config(text="", bg="white")
            self.buttons[i2][j2].config(text="", bg="white")

        self.flipped = []
        self.chances -= 1
        self.locked = False
        self.update_labels()

        if len(self.matched) == self.total_tiles:
            self.show_win_screen()
        elif self.chances == 0:
            messagebox.showinfo("Game Over", "You're out of chances!")
            self.app.show_level_select_screen()

    def update_labels(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.chances_label.config(text=f"Chances: {self.chances}")

    def show_win_screen(self):
        time_taken = round(time.time() - self.start_time, 2)
        print(f"[LOG] Player '{self.player_name}' completed Level {self.level} in {time_taken} seconds "
            f"with score {self.score} and {self.chances} chances left.")

        self.app.unlock_next_level(self.level)

        win_popup = tk.Toplevel(self.root)
        win_popup.title("Level Complete")
        win_popup.geometry("300x200")
        win_popup.configure(bg="#a8ddf0")

        tk.Label(win_popup, text=f"Well done, {self.player_name}!", font=("Comic Sans MS", 14, "bold"),
                bg="#a8ddf0", fg="black").pack(pady=20)
        tk.Label(win_popup, text=f"Score: {self.score}", font=("Comic Sans MS", 12), bg="#a8ddf0", fg="black").pack()
        tk.Label(win_popup, text=f"Time: {time_taken} seconds", font=("Comic Sans MS", 12), bg="#a8ddf0", fg="black").pack()

        tk.Button(win_popup, text="Next Level", font=("Comic Sans MS", 12, "bold"), bg="#00c897", fg="white",
                command=lambda: self.complete_level(win_popup)).pack(pady=10)

        tk.Button(win_popup, text="Main Menu", font=("Comic Sans MS", 10), bg="#cccccc",
                command=lambda: self.back_to_menu(win_popup)).pack(pady=5)


    def complete_level(self, popup):
        popup.destroy()
        next_level = self.level + 1
        if next_level <= 6:
            self.app.start_game_screen(next_level)
        else:
            self.app.show_level_select_screen()


    def back_to_menu(self, popup):
        popup.destroy()
        self.app.show_level_select_screen()


if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryFlipApp(root)
    root.mainloop()
