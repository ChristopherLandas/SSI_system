import tkinter as tk
import winsound  # For playing a sound (Windows-specific)

def flash_window():
    root.attributes("-alpha", 0.2)
    root.after(300, lambda: root.attributes("-alpha", 1))

def play_sound():
    root.lift()
    root.focus_force()
    root.grab_set()
    sound_file = "path_to_your_sound_file.wav"
    winsound.PlaySound(sound_file, winsound.SND_FILENAME)

root = tk.Tk()
root.title("Focus Reminder")
root.bind("<FocusOut>", lambda _: play_sound())
root.wm_attributes("-topmost", True)

root.geometry("300x100")
root.mainloop()