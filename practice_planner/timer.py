import tkinter as tk
from tkinter import ttk

from .exercise_timer import ExerciseTimer
from .metronome import Metronome
from .utils import safe_log_exercise, safe_play_sound


class TimerWindow(tk.Toplevel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.timer = None
        self.running = False
        self.paused = False

        self.title("Practice Timer + Metronome")
        self.geometry("520x420")

        # Exercise info
        self.exercise_label = ttk.Label(self, text="", font=("Arial", 14))
        self.exercise_label.pack(pady=10)

        self.timer_label = ttk.Label(
            self, text="", font=("Arial", 24), foreground="black"
        )
        self.timer_label.pack(pady=10)

        # Control buttons
        controls = ttk.Frame(self)
        controls.pack(pady=10)

        self.play_btn = ttk.Button(controls, text="Play", command=self.start_exercise)
        self.play_btn.pack(side="left", padx=5)

        self.pause_btn = ttk.Button(
            controls, text="Pause", command=self.toggle_pause, state="disabled"
        )
        self.pause_btn.pack(side="left", padx=5)

        self.skip_btn = ttk.Button(
            controls, text="Skip", command=self.skip_exercise, state="disabled"
        )
        self.skip_btn.pack(side="left", padx=5)

        # Logging checkbox
        self.log_var = tk.BooleanVar(value=True)
        self.log_chk = ttk.Checkbutton(
            self, text="Log this exercise", variable=self.log_var
        )
        self.log_chk.pack(pady=5)

        # Metronome controls
        self.metro_frame = ttk.LabelFrame(self, text="Metronome")
        self.metro_frame.pack(pady=10, fill="x")

        ttk.Label(self.metro_frame, text="BPM:").pack(side="left", padx=5)
        self.bpm_entry = ttk.Entry(self.metro_frame, width=6)
        self.bpm_entry.insert(0, "60")
        self.bpm_entry.pack(side="left")
        self.bpm_entry.bind("<Return>", self.on_bpm_enter)  # restart metronome on Enter

        self.metro_btn = ttk.Button(
            self.metro_frame, text="Start Metronome", command=self.toggle_metronome
        )
        self.metro_btn.pack(side="left", padx=5)

        self.sound_var = tk.BooleanVar(value=True)
        self.sound_chk = ttk.Checkbutton(
            self.metro_frame, text="Sound On", variable=self.sound_var
        )
        self.sound_chk.pack(side="left", padx=5)

        ttk.Label(self.metro_frame, text="Sound Type:").pack(side="left", padx=5)
        self.sound_choice = ttk.Combobox(
            self.metro_frame, values=["Glass", "Pop", "Ping", "Funk"], width=10
        )
        self.sound_choice.current(0)
        self.sound_choice.pack(side="left", padx=5)

        self.metro_label = ttk.Label(self.metro_frame, text="", font=("Arial", 16))
        self.metro_label.pack(side="left", padx=10)

        self.flash_rect = tk.Label(self.metro_frame, bg="yellow")
        self.flash_rect.place_forget()

        # Metronome instance
        self.metronome = Metronome(self, self.metronome_tick)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.prepare_next_exercise()

    def prepare_next_exercise(self):
        if self.controller.has_next():
            section, ex, minutes = self.controller.current()
            self.exercise_label.config(text=f"{section} - {ex}")
            self.timer = ExerciseTimer(minutes)
            self.timer_label.config(text=f"{minutes:02d}:00", foreground="black")
            self.play_btn.config(state="normal")
            self.pause_btn.config(state="disabled", text="Pause")
            self.skip_btn.config(state="disabled")
        else:
            self.exercise_label.config(text="All exercises complete!")
            self.timer_label.config(text="🎉 Done!", foreground="black")
            self.play_btn.config(state="disabled")
            self.pause_btn.config(state="disabled")
            self.skip_btn.config(state="disabled")

    def start_exercise(self):
        if self.timer:
            self.timer.start()
            self.running = True
            self.paused = False
            self.play_btn.config(state="disabled")
            self.pause_btn.config(state="normal", text="Pause")
            self.skip_btn.config(state="normal")
            self.update_timer()

    def update_timer(self):
        if not self.running or self.paused:
            return

        remaining = self.timer.tick()
        mins, secs = divmod(remaining, 60)
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}", foreground="black")

        if remaining > 0:
            self.after(1000, self.update_timer)
        else:
            self.running = False
            self.metronome.stop()
            self.pause_btn.config(state="disabled")
            self.skip_btn.config(state="disabled")
            self.play_btn.config(state="disabled")
            self.exercise_label.config(text="Exercise complete!")
            self.timer_label.config(text="00:00", foreground="black")
            if self.log_var.get():
                section, ex, minutes = self.controller.current()
                bpm = self.get_bpm_or_default()
                safe_log_exercise(section, ex, minutes, "done", bpm)
            self.controller.advance()
            self.prepare_next_exercise()

    def skip_exercise(self):
        if self.running:
            self.running = False
            self.metronome.stop()
            self.pause_btn.config(state="disabled")
            self.skip_btn.config(state="disabled")
            self.play_btn.config(state="disabled")
            self.exercise_label.config(text="Skipped!")
            self.timer_label.config(text="00:00", foreground="black")
            if self.log_var.get():
                section, ex, minutes = self.controller.current()
                bpm = self.get_bpm_or_default()
                safe_log_exercise(section, ex, minutes, "skipped", bpm)
            self.controller.advance()
            self.prepare_next_exercise()

    def toggle_pause(self):
        if self.running:
            if not self.paused:
                self.timer.pause()
                self.paused = True
                self.metronome.stop()
                self.pause_btn.config(text="Resume")
                self.timer_label.config(foreground="orange", text="Paused")
            else:
                self.timer.resume()
                self.paused = False
                self.pause_btn.config(text="Pause")
                self.timer_label.config(foreground="black")
                if self.metro_btn.cget("text") == "Stop Metronome":
                    self.metronome.start()
                self.update_timer()

    def toggle_metronome(self):
        if not self.metronome.running:
            bpm = self.get_bpm_or_default()
            self.metronome.set_bpm(bpm)
            self.metronome.start()
            self.metro_btn.config(text="Stop Metronome")
        else:
            self.metronome.stop()
            self.metro_btn.config(text="Start Metronome")
            self.metro_label.config(text="")
            self.flash_rect.place_forget()

    def metronome_tick(self):
        if not self.metronome.running:
            return
        self.metro_label.config(text="Tick")
        if self.sound_var.get():
            safe_play_sound(self.sound_choice.get())
        else:
            self.flash_rect.place(relx=0.05, rely=0.6, relwidth=0.9, relheight=0.3)
            self.after(150, self.flash_rect.place_forget)
        self.after(200, lambda: self.metro_label.config(text=""))

    def get_bpm_or_default(self):
        text = self.bpm_entry.get().strip()
        if text.isdigit():
            val = int(text)
            if 30 <= val <= 240:
                self.bpm_entry.config(foreground="black")
                return val
            else:
                self.bpm_entry.config(foreground="red")
                return 60
        else:
            self.bpm_entry.config(foreground="red")
            return 60

    def on_bpm_enter(self, event=None):
        bpm = self.get_bpm_or_default()
        if self.metronome.running:
            self.metronome.set_bpm(bpm)
            self.metronome.stop()
            self.metronome.start()

    def on_close(self):
        self.running = False
        self.metronome.stop()
        self.destroy()
