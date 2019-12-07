class AocpyException(Exception):
    pass


class SubmissionError(AocpyException):
    pass


class RepeatSubmissionError(SubmissionError):
    pass


class IncorrectSubmissionError(SubmissionError):
    pass


class RateLimitError(SubmissionError):
    pass
