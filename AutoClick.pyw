import tkinter as tk
import threading
import time
import ctypes
from pynput import mouse

class Autoclicker:
    def __init__(self, cps):
        self.cps = cps
        self.interval = 1.0 / cps
        self.running = False

    def start_clicking(self):
        self.running = True
        while self.running:
            ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0) # left mouse button down
            ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0) # left mouse button up
            time.sleep(self.interval)

    def stop_clicking(self):
        self.running = False

class AutoclickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Autoclicker")
        self.root.geometry("250x100")  # Set initial window size
        
        self.label = tk.Label(root, text="Clicks per second:")
        self.label.pack()

        self.cps_var = tk.StringVar()  # Variable to hold the value of cps entry
        self.cps_entry = tk.Entry(root, textvariable=self.cps_var)
        self.cps_entry.pack()

        self.start_button = tk.Button(root, text="Start Autoclicker", command=self.start_autoclicker, state=tk.DISABLED)
        self.start_button.pack()

        self.stop_button = tk.Button(root, text="Stop Autoclicker", command=self.stop_autoclicker, state=tk.DISABLED)
        self.stop_button.pack()

        self.autoclicker = None
        self.mouse_listener = mouse.Listener(on_click=self.middle_mouse_click)
        self.mouse_listener.start()

        self.cps_entry.bind("<KeyRelease>", self.validate_cps_entry)

    def middle_mouse_click(self, x, y, button, pressed):
        if button == mouse.Button.middle and pressed:
            if self.running:
                self.stop_autoclicker()
            else:
                self.start_autoclicker()

    def validate_cps_entry(self, event):
        cps_str = self.cps_var.get()
        if cps_str.strip() == '':
            self.start_button.config(state=tk.DISABLED)
            return
        
        try:
            cps = float(cps_str)
            if cps <= 0:
                raise ValueError
            self.start_button.config(state=tk.NORMAL)
        except ValueError:
            self.start_button.config(state=tk.DISABLED)

    def start_autoclicker(self):
        self.root.iconify()
        cps = float(self.cps_var.get())
        self.autoclicker = Autoclicker(cps)
        threading.Thread(target=self.autoclicker.start_clicking, daemon=True).start()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_autoclicker(self):
        if self.autoclicker:
            self.autoclicker.stop_clicking()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.root.deiconify()
        self.root.lift()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoclickerApp(root)
    root.mainloop()
