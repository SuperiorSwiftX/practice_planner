# practice_planner/metronome.py


class Metronome:
    def __init__(self, root, on_tick):
        """
        Metronome runs its own loop based on BPM.
        :param root: Tk root or Toplevel for scheduling
        :param on_tick: callback function to fire on each beat
        """
        self.root = root
        self.on_tick = on_tick
        self.running = False
        self.bpm = 60
        self._after_id = None

    def set_bpm(self, bpm: int):
        """Clamp BPM and update value only."""
        self.bpm = max(30, min(bpm, 240))

    def start(self):
        if not self.running:
            self.running = True
            self._schedule()

    def stop(self):
        self.running = False
        if self._after_id:
            self.root.after_cancel(self._after_id)
            self._after_id = None

    def _schedule(self):
        if not self.running:
            return
        interval_ms = int(60000 / self.bpm)
        self.on_tick()
        self._after_id = self.root.after(interval_ms, self._schedule)
