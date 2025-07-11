import os
import shutil
import time
from pathlib import Path
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox


class DownloadClean:
    def __init__(self):
        self.download = Path.home() / "Downloads"

    def start_cleaning(self):
        for file in os.listdir(self.download):
            file_path = self.download / file
            if file_path.is_file():

                if self.is_file_old(file_path):
                    continue

                self.sort_file(file_path)

    @staticmethod
    def is_file_old(file):
        actual_time = time.time()
        file_time = os.path.getmtime(file)

        if actual_time - file_time > 7 * 24 * 60 * 60:
            os.remove(file)
            return True

        return False

    def sort_file(self, file):
        ext = file.suffix.lower().lstrip(".")
        if ext:
            target_dir = self.download / f"{ext}_files"
            target_dir.mkdir(exist_ok=True)
            new_file_path = target_dir / file.name

            if new_file_path.exists():
                ext = file.sufix
                base = file.stem
                i = 1

                while True:
                    new_file_name = f"{base}_{i}{ext}"
                    new_file_path = target_dir / new_file_name
                    if not new_file_path.exists():
                        break
                    i += 1

            shutil.move(str(file), str(new_file_path))


class Gui:
    def __init__(self):
        self.cleaner = DownloadClean()

        self.root = tk.Tk()
        self.root.title("Download cleaning agent")
        self.root.configure(background="white smoke")

        self.root.geometry("550x400")
        self.center_geometry(450, 300)

        self.img = Image.open("trash_can.jpg").resize((160, 160))
        self.tk_img = ImageTk.PhotoImage(self.img)

        self.label = tk.Label(self.root, image=self.tk_img)  # type: ignore
        self.label.pack(pady=30)

        self.btn = tk.Button(
            self.root,
            text="Start cleaning",
            height=2,
            width=20,
            font=("Arial", 16),
            command=self.cleaning_complete,
            cursor="hand2",
        )
        self.btn.pack(padx=30, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.mainloop()

    def on_closing(self):
        if messagebox.askyesno(title="Quit", message="Do you want to quit?"):
            self.root.destroy()

    def cleaning_complete(self):
        self.cleaner.start_cleaning()
        messagebox.showinfo(title="Success", message="Cleaning complete!")

    def center_geometry(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y - 100}")


if __name__ == "__main__":
    Gui()
