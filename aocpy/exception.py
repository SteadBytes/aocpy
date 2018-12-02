class AocpyException(Exception):
    pass


class SubmissionError(AocpyException):
    def __init__(self, msg, answer, level, year, day):
        super().__init__(msg)
        self.answer = answer
        self.level = level
        self.year = year
        self.day = day


class RepeatSubmissionError(SubmissionError):
    def __str__(self):
        return f"level {self.level} already submitted"


class IncorrectSubmissionError(SubmissionError):
    def __str__(self):
        return f"incorrect answer: {self.answer}"


class RateLimitError(SubmissionError):
    pass
