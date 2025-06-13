import time

class Timer:
    def __init__(self, filename="timing_log.txt"):
        self.start_time = time.time()
        self.last_checkpoint = self.start_time
        self.filename = filename
        with open(self.filename, 'w') as f:
            pass  # Clear file at start

    def checkpoint(self, label):
        now = time.time()
        elapsed = now - self.last_checkpoint
        self._log(f"{label}: {elapsed:.3f}")
        self.last_checkpoint = now

    def total(self):
        total_elapsed = time.time() - self.start_time
        message = f"\nTotal runtime: {total_elapsed:.3f} seconds\n"
        self._log(message)
        print(message)  # <-- Printed to the user

    def _log(self, message):
        with open(self.filename, 'a') as f:
            f.write(message + "\n")