import csv
import datetime
import subprocess
import sys
from pathlib import Path
from tkinter import messagebox


def play_sound(sound_type: str):
    """Play a short sound depending on platform and chosen type."""
    if sys.platform == "darwin":  # macOS
        sound_map = {
            "Glass": "/System/Library/Sounds/Glass.aiff",
            "Pop": "/System/Library/Sounds/Pop.aiff",
            "Ping": "/System/Library/Sounds/Ping.aiff",
            "Funk": "/System/Library/Sounds/Funk.aiff",
        }
        path = sound_map.get(sound_type)
        if path:
            subprocess.Popen(
                ["afplay", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )

    elif sys.platform == "win32":  # Windows
        import winsound

        freq_map = {"Glass": 2000, "Pop": 1000, "Ping": 1500, "Funk": 400}
        freq = freq_map.get(sound_type, 880)
        winsound.Beep(freq, 60)

    else:  # Linux or other
        pass


def log_exercise_csv(section: str, exercise: str, minutes: int, status: str, bpm: int):
    """Append a log entry to practice_log.csv in the user's Documents folder."""
    documents = Path.home() / "Documents"
    log_file = documents / "practice_log.csv"
    exists = log_file.exists()

    with log_file.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["date", "section", "exercise", "minutes", "status", "bpm"])
        writer.writerow(
            [datetime.date.today().isoformat(), section, exercise, minutes, status, bpm]
        )


# --- Safe wrappers with error dialogs ---
def safe_play_sound(sound_type: str):
    try:
        play_sound(sound_type)
    except Exception as e:
        messagebox.showerror("Sound Error", f"Could not play sound: {e}")


def safe_log_exercise(section, exercise, minutes, status, bpm):
    try:
        log_exercise_csv(section, exercise, minutes, status, bpm)
    except Exception as e:
        messagebox.showerror("Logging Error", f"Could not log exercise: {e}")
