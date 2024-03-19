import tkinter as tk
from tkinter import ttk
import threading
import time
import pyautogui
import pydirectinput
import pygetwindow
from pynput import mouse

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Farmer")
    
        # Calculate the center position of the screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - 400) / 2  # Assuming the width of the window is 400
        y = (screen_height - 300) / 2  # Assuming the height of the window is 300
        root.geometry("+%d+%d" % (x - 150, y))  # Set the window position to the center
    
        self.interval_label = ttk.Label(root, text="Interval between clicks (seconds):")
        self.interval_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    
        self.interval_entry = ttk.Entry(root, width=10)
        self.interval_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    
        self.key_label = ttk.Label(root, text="Keys to press automatically:")
        self.key_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    
        self.key_entry_frame = ttk.Frame(root)
        self.key_entry_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")
    
        # Add label "Key:" for the first box
        self.key_label1 = ttk.Label(self.key_entry_frame, text="Key:")
        self.key_label1.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    
        self.key_entry = ttk.Entry(self.key_entry_frame, width=10)
        self.key_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    
        self.interval_label = ttk.Label(self.key_entry_frame, text="Interval (seconds):")
        self.interval_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")
    
        self.interval_entry = ttk.Entry(self.key_entry_frame, width=10)
        self.interval_entry.grid(row=0, column=3, padx=10, pady=5, sticky="w")
    
        self.add_button = ttk.Button(self.key_entry_frame, text="Add Key", command=self.add_key)
        self.add_button.grid(row=0, column=4, padx=10, pady=5, sticky="w")
    
        self.key_entries = [(self.key_entry, self.interval_entry)]
    
        self.auto_click_var = tk.BooleanVar()
        self.auto_click_check = ttk.Checkbutton(root, text="Auto Click", variable=self.auto_click_var)
        self.auto_click_check.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")
    
        self.auto_letter_var = tk.BooleanVar()
        self.auto_letter_check = ttk.Checkbutton(root, text="Auto Type", variable=self.auto_letter_var)
        self.auto_letter_check.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="w")
    
        self.choose_location_button = ttk.Button(root, text="Choose Location of Clicks", command=self.choose_location)
        self.choose_location_button.grid(row=5, column=0, padx=10, pady=5, sticky="w")
    
        self.start_button = ttk.Button(root, text="Start", command=self.start_auto)
        self.start_button.grid(row=5, column=1, padx=10, pady=5)
        self.start_button.configure(state="disabled")  # Disable start button initially
    
        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_auto)
        self.stop_button.grid(row=5, column=2, padx=10, pady=5)
        self.stop_button.configure(state="disabled")
    
        self.running = False
        self.auto_click_coordinates = None
        self.roblox_found_notification = False  # Flag to track if Roblox found notification shown
    
        self.roblox_window_check_interval = 5  # Check Roblox window every 5 seconds
        self.check_roblox_window()
    
        # Set up the middle mouse button click event handler using pynput
        self.mouse_listener = mouse.Listener(on_click=self.middle_mouse_click)
        self.mouse_listener.start()

    def middle_mouse_click(self, x, y, button, pressed):
        if button == mouse.Button.middle and pressed:
            if self.running:
                self.stop_auto()
            else:
                self.start_auto()

    def check_roblox_window(self):
        if self.find_roblox_window():
            if not self.roblox_found_notification:
                self.start_button.configure(state="normal")
                roblox_label = ttk.Label(self.root, text="Roblox Found")
                roblox_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
                self.roblox_found_notification = True
                # Remove the "Looking for Roblox..." label if it exists
                for widget in self.root.winfo_children():
                    if isinstance(widget, ttk.Label) and widget.cget("text") == "Looking for Roblox...":
                        widget.grid_remove()
        else:
            self.start_button.configure(state="disabled")
            self.roblox_found_notification = False
            looking_label = ttk.Label(self.root, text="Looking for Roblox...")
            looking_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.root.after(500 * self.roblox_window_check_interval, self.check_roblox_window)

    def find_roblox_window(self):
        # Check if the Roblox window is open
        for window in pygetwindow.getAllTitles():
            if "Roblox" in window:
                return True
        return False

    def add_key(self):
        key_label = ttk.Label(self.key_entry_frame, text="Key:")
        key_label.grid(row=len(self.key_entries), column=0, padx=10, pady=5, sticky="w")
        
        key_entry = ttk.Entry(self.key_entry_frame, width=10)
        key_entry.grid(row=len(self.key_entries), column=1, padx=10, pady=5, sticky="w")
        
        interval_label = ttk.Label(self.key_entry_frame, text="Interval (seconds):")
        interval_label.grid(row=len(self.key_entries), column=2, padx=10, pady=5, sticky="w")
        
        interval_entry = ttk.Entry(self.key_entry_frame, width=10)
        interval_entry.grid(row=len(self.key_entries), column=3, padx=10, pady=5, sticky="w")
        
        self.key_entries.append((key_entry, interval_entry))


    def start_auto(self):
        if not self.running:
            interval = float(self.interval_entry.get())
            auto_click = self.auto_click_var.get()
            auto_letter = self.auto_letter_var.get()
            keys_intervals = [(entry[0].get(), float(entry[1].get())) for entry in self.key_entries if entry[0].get()]
            if not keys_intervals:
                self.notify("No keys specified. Please add keys to press automatically.")
                return  # Don't start if no keys are specified
            self.notify("Starting auto tasks...")
            self.running = True
            self.stop_button.configure(state="normal")
            self.start_button.configure(state="disabled")
            threading.Thread(target=self.auto_tasks, args=(interval, keys_intervals, auto_click, auto_letter), daemon=True).start()
            self.root.iconify()  # Minimize the application window after starting
            # Focus Roblox window
            roblox_window = pygetwindow.getWindowsWithTitle("Roblox")
            if roblox_window:
                roblox_window[0].activate()
            else:
                self.notify("Roblox window not found.")

    def stop_auto(self):
        if self.running:
            self.notify("Stopping auto tasks...")
            self.running = False
            self.stop_button.configure(state="disabled")
            self.start_button.configure(state="normal")
            self.root.deiconify()  # Show the root window
            self.root.lift()  # Bring the root window to the front



    def auto_click(self, interval):
        while self.running:
            active_window = pygetwindow.getActiveWindow()
            if active_window and "Roblox" in active_window.title:
                if self.auto_click_coordinates:
                    # Move the cursor slightly before clicking
                    pyautogui.move(1, 1)  # Example: Move 1 pixel to the right and 1 pixel down
                    pyautogui.click(x=self.auto_click_coordinates[0], y=self.auto_click_coordinates[1])
                else:
                    pyautogui.click()
            time.sleep(interval)

    

    def auto_letter(self, keys_intervals):
        previous_window = None  # Initialize variable to store reference to previous window
        while self.running:
            for key, interval in keys_intervals:
                # Get the previously focused window before focusing Roblox
                previous_window = pygetwindow.getActiveWindow()
    
                roblox_window = pygetwindow.getWindowsWithTitle("Roblox")
                if roblox_window:
                    roblox_window[0].activate()  # Focus Roblox window
                else:
                    self.notify("Roblox window not found.")
                    continue
    
                pydirectinput.press(key)
    
                # Unfocus Roblox window after sending the key
                if previous_window:
                    previous_window.activate()  # Bring back the previously focused window
                else:
                    self.root.lift()  # If no previous window, bring the root window to the front

                time.sleep(interval)

    def auto_tasks(self, interval, keys_intervals, auto_click, auto_letter):
        if auto_click:
            self.notify("Auto clicking enabled.")
            threading.Thread(target=self.auto_click, args=(interval,), daemon=True).start()
        if auto_letter:
            self.notify("Auto typing enabled.")
            threading.Thread(target=self.auto_letter, args=(keys_intervals,), daemon=True).start()

    def choose_location(self):
        self.root.withdraw()  # Hide the root window temporarily
        time.sleep(2)  # Delay to allow the window to minimize properly
        
        # Use pyautogui to get mouse coordinates relative to the screen
        self.auto_click_coordinates = pyautogui.position()
        
        self.notify("Auto click location set at: {}".format(self.auto_click_coordinates))
        self.root.deiconify()  # Show the root window again

    def notify(self, message):
        # Function to display notification popup
        popup = tk.Toplevel(self.root)
        popup.title("Notification")
        label = ttk.Label(popup, text=message)
        label.pack(padx=10, pady=10)
        # Calculate y-coordinate to stack notifications
        y_offset = sum(p.winfo_height() for p in self.root.winfo_children() if isinstance(p, tk.Toplevel))
        popup.geometry(f"+{self.root.winfo_x()}+{self.root.winfo_y() + y_offset}")
        popup.after(2500, popup.destroy)  # Close the popup after 2.5 seconds
        # Ensure the application window gains focus over the notification
        self.root.focus_force()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()
