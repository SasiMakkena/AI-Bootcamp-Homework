"""
Utilities: lightweight step logger with numbered, indented output.
"""


class StepLogger:
    def __init__(self):
        self.level = 0
        self.counters = []

    def _prefix(self) -> str:
        if not self.counters:
            return ""
        return "[" + ".".join(str(c) for c in self.counters) + "] "

    def step(self, title: str):
        """
        Start a new top-level step or sub-step:
        - At level 0, increments first counter (1, 2, 3…)
        - For subsequent notes, use .note()
        """
        if self.level == 0:
            if not self.counters:
                self.counters = [1]
            else:
                self.counters[0] += 1
        else:
            # For simplicity, we just increment last counter
            self.counters[-1] += 1
        print(f"{self._prefix()}{title}")
        # Indent notes under the step
        self.level = 1

    def note(self, message: str):
        """
        Print an indented note under the current step.
        """
        indent = "  " * self.level
        print(f"{indent}{message}")
