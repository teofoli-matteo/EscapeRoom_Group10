class Logger:
    def __init__(self, filename):
        self.filename = filename
        self.lines = []
    def log(self, line):
        print(line)
        self.lines.append(line)
    def save(self):
        with open(self.filename, "w") as f:
            f.write("\n".join(self.lines) + "\n")