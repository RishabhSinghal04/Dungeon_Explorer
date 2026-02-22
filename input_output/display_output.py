from interfaces import IOutputHandler


class ConsoleOutputHandler(IOutputHandler):
    def display(self, text: str, end: str = "\n") -> None:
        print(text, end=end)
