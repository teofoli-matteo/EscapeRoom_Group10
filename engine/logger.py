"""
logger.py
Defines the Logger class used to record and save gameplay transcripts
for the Cyber Escape Room game.
"""
class Logger:
    """Handles writing to the final log file"""
    def __init__(self, filename):
        """
        args: the filename to save the log to
        """
        self.filename = filename
        self.lines = []
    def log(self, line):
        """
        log a line : print and store
        args: the message to log
        """
        print(line)
        self.lines.append(line)
    def save(self):
        """
        save all logged lines to the file specified at initialization.
        Each line is separated by a newline.
        """
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write("\n".join(self.lines) + "\n")