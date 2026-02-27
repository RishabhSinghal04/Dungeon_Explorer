from core.interfaces import IOutputHandler


class ConsoleOutputHandler(IOutputHandler):
    def display(self, text: str, separator: str = "\n") -> None:
        print(text, end=separator)
