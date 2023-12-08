import ctypes
import sys

def run_as_admin():
    if sys.platform == 'win32':
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None,
                "runas",
                sys.executable,
                " ".join(sys.argv),
                None,
                1
            )
            return True
        except Exception as e:
            # Handle the case where the user cancels the UAC prompt
            print(f"Error: {e}")
            return False
    else:
        return False

if __name__ == "__main__":
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        # Not running as administrator, prompt for elevation
        if run_as_admin():
            # The script is now running with administrator privileges
            # Add your Tkinter code here
            import tkinter as tk

            root = tk.Tk()
            root.title("Administrator Window")
            label = tk.Label(root, text="This window is running with administrator privileges.")
            label.pack(padx=20, pady=20)
            root.mainloop()
        else:
            print("Failed to run with administrator privileges.")
    else:
        # Already running as administrator, add your Tkinter code here
        import tkinter as tk

        root = tk.Tk()
        root.title("Administrator Window")
        label = tk.Label(root, text="This window is running with administrator privileges.")
        label.pack(padx=20, pady=20)
        root.mainloop()
