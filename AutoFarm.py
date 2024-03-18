import tkinter as tk
from tkinter import ttk
import threading
import time
import win32gui
import pyautogui
import pydirectinput

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Farmer")
        
        self.interval_label = ttk.Label(root, text="Interval between clicks (seconds):")
        self.interval_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.interval_entry = ttk.Entry(root, width=10)
        self.interval_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        self.letter_interval_label = ttk.Label(root, text="Interval between letters (seconds):")
        self.letter_interval_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.letter_interval_entry = ttk.Entry(root, width=10)
        self.letter_interval_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        self.key_label = ttk.Label(root, text="Key(s) to press automatically:")
        self.key_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        self.key_entry_frame = ttk.Frame(root)
        self.key_entry_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        self.key_entry = ttk.Entry(self.key_entry_frame, width=10)
        self.key_entry.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.add_button = ttk.Button(self.key_entry_frame, text="Add Key", command=self.add_key)
        self.add_button.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        self.key_entries = [self.key_entry]
        
        self.auto_click_var = tk.BooleanVar()
        self.auto_click_check = ttk.Checkbutton(root, text="Auto Click", variable=self.auto_click_var)
        self.auto_click_check.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        self.auto_letter_var = tk.BooleanVar()
        self.auto_letter_check = ttk.Checkbutton(root, text="Auto Type", variable=self.auto_letter_var)
        self.auto_letter_check.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        self.choose_location_button = ttk.Button(root, text="Choose Location of Clicks", command=self.choose_location)
        self.choose_location_button.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        
        self.start_button = ttk.Button(root, text="Start", command=self.start_auto)
        self.start_button.grid(row=6, column=1, padx=10, pady=5)
        
        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_auto)
        self.stop_button.grid(row=6, column=2, padx=10, pady=5)
        self.stop_button.configure(state="disabled")
        
        self.running = False
        self.auto_click_coordinates = None

    def add_key(self):
        key_entry = ttk.Entry(self.key_entry_frame, width=10)
        key_entry.grid(row=len(self.key_entries), column=0, padx=10, pady=5, sticky="w")
        self.key_entries.append(key_entry)

    def start_auto(self):
        if not self.running:
            interval = float(self.interval_entry.get())
            letter_interval = float(self.letter_interval_entry.get())
            keys = [entry.get() for entry in self.key_entry_frame.winfo_children() if isinstance(entry, ttk.Entry) and entry.get()]
            auto_click = self.auto_click_var.get()
            auto_letter = self.auto_letter_var.get()
            if not keys:
                print("No keys specified. Please add keys to press automatically.")
                return  # Don't start if no keys are specified
            print("Starting auto tasks...")
            self.running = True
            self.stop_button.configure(state="normal")
            self.start_button.configure(state="disabled")
            threading.Thread(target=self.auto_tasks, args=(interval, letter_interval, keys, auto_click, auto_letter), daemon=True).start()

    def stop_auto(self):
        if self.running:
            print("Stopping auto tasks...")
            self.running = False
            self.stop_button.configure(state="disabled")
            self.start_button.configure(state="normal")
            for entry in self.key_entries[1:]:
                entry.grid_remove()
            self.key_entries = [self.key_entries[0]]

    def auto_click(self, interval):
        while self.running:
            if self.auto_click_coordinates:
                pyautogui.click(x=self.auto_click_coordinates[0], y=self.auto_click_coordinates[1])
                print("Clicked at coordinates:", self.auto_click_coordinates)
            time.sleep(interval)

    def auto_letter(self, keys, letter_interval):
        while self.running:
            for key in keys:
                pydirectinput.press(key)
                print("Pressed key:", key)
                time.sleep(0.1)  # Adjust the delay between keystrokes if needed
            time.sleep(letter_interval)

    def auto_tasks(self, interval, letter_interval, keys, auto_click, auto_letter):
        if auto_click:
            print("Auto clicking enabled.")
            threading.Thread(target=self.auto_click, args=(interval,), daemon=True).start()
        if auto_letter:
            print("Auto typing enabled.")
            threading.Thread(target=self.auto_letter, args=(keys, letter_interval), daemon=True).start()

    def choose_location(self):
        self.root.config(cursor="crosshair")
        self.root.bind('<Button-1>', self.on_click)

    def on_click(self, event):
        self.auto_click_coordinates = (event.x_root, event.y_root)
        self.root.config(cursor="")

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()
