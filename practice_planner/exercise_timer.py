# practice_planner/exercise_timer.py


class ExerciseTimer:
    def __init__(self, minutes):
        self.initial = minutes * 60
        self.remaining = self.initial
        self.running = False
        self.paused = False

    def start(self):
        self.running = True
        self.paused = False

    def pause(self):
        if self.running:
            self.paused = True

    def resume(self):
        if self.running:
            self.paused = False

    def reset(self, minutes):
        self.initial = minutes * 60
        self.remaining = self.initial
        self.running = False
        self.paused = False

    def tick(self):
        if self.running and not self.paused and self.remaining > 0:
            self.remaining -= 1
        return self.remaining
