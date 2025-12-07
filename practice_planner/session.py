class PracticeSessionController:
    def __init__(self, exercise_plan):
        self.plan = exercise_plan
        self.index = 0

    def has_next(self):
        return self.index < len(self.plan)

    def current(self):
        return self.plan[self.index] if self.has_next() else None

    def advance(self):
        self.index += 1
        return self.has_next()
