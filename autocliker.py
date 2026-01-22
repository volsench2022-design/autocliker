# pip install mouse
# pip install keyboard
import tkinter as tk
from tkinter import messagebox
import mouse
import keyboard
import time

# ========================================================
# Global variables
# ========================================================
running = False
paused = False
delay = 0
end_time_seconds = None

# ========================================================
# Functions
# ========================================================

def start_clicker():
    """Start or resume clicking."""
    global running, paused, delay, end_time_seconds
    if not running:
        try:
            interval_input = interval_entry.get()
            if interval_input:
                delay = int(interval_input)
                if delay <= 0:
                    messagebox.showerror("Помилка", "Інтервал має бути більше 0!")
                    return
            else:
                clicks_per_second = int(cps_entry.get())
                if clicks_per_second <= 0:
                    messagebox.showerror("Помилка", "Швидкість має бути більше 0!")
                    return
                delay = int(1000 / clicks_per_second)

            timer_input = timer_entry.get()
            if timer_input:
                total_seconds = int(timer_input)
                if total_seconds > 0:
                    end_time_seconds = time.time() + total_seconds
                else:
                    end_time_seconds = None
            else:
                end_time_seconds = None

            running = True
            paused = False
            schedule_click()
        except ValueError:
            messagebox.showerror("Помилка вводу", "Введіть числа у всіх полях!")
    else:
        # Resume if paused
        paused = False

def pause_clicker():
    """Pause the clicking."""
    global paused
    paused = True
    messagebox.showinfo("Auto Clicker", "Автоклікер призупинено.")

def stop_clicker():
    """Stop the clicking completely."""
    global running, paused
    running = False
    paused = False
    messagebox.showinfo("Auto Clicker", "Автоклікер зупинено.")

def schedule_click():
    """Perform a click and schedule next one."""
    global running, paused
    if running and not paused:
        if end_time_seconds and time.time() >= end_time_seconds:
            stop_clicker()
            return
        mouse.click()
    if running:
        root.after(delay, schedule_click)

def exit_app():
    stop_clicker()
    root.destroy()

# ========================================================
# GUI
# ========================================================

root = tk.Tk()
root.title("Auto Clicker")
root.geometry("350x300")
root.resizable(False, False)
root.configure(bg="#e0f7fa")

# Clicks per second
tk.Label(root, text="Кліків на секунду:", bg="#e0f7fa").pack(pady=5)
cps_entry = tk.Entry(root, font=("Arial", 12), width=10, justify='center')
cps_entry.pack(pady=5)
cps_entry.insert(0, "10")

# Interval between clicks (ms, optional)
tk.Label(root, text="Інтервал між кліками (мс, необов'язково):", bg="#e0f7fa").pack(pady=5)
interval_entry = tk.Entry(root, font=("Arial", 12), width=10, justify='center')
interval_entry.pack(pady=5)

# Timer in seconds (optional)
tk.Label(root, text="Таймер (секунди, необов'язково):", bg="#e0f7fa").pack(pady=5)
timer_entry = tk.Entry(root, font=("Arial", 12), width=10, justify='center')
timer_entry.pack(pady=5)

# Buttons: Start, Pause, Stop
button_frame = tk.Frame(root, bg="#e0f7fa")
button_frame.pack(pady=20)
tk.Button(button_frame, text="Start", command=start_clicker, bg="#4caf50", fg="white", width=10).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Pause", command=pause_clicker, bg="#ffc107", fg="white", width=10).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Stop", command=stop_clicker, bg="#f44336", fg="white", width=10).grid(row=0, column=2, padx=5)

# Hotkey ESC to stop
keyboard.add_hotkey('esc', exit_app)
root.protocol("WM_DELETE_WINDOW", exit_app)

root.mainloop()
