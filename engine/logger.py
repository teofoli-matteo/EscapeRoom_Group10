class Logger:
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
        save all logged lines to the file specified at initialization.Each line is separated by a newline.
        """
        with open(self.filename, "w") as f:
            f.write("\n".join(self.lines) + "\n")