class UnknownSettingsKeyError(Exception):
    def __init__(self, key: str):
        self.key = key
        self.message = f"Unknown settings key: {key}"
        super().__init__(self.message)


class MissingSettingsKeyError(Exception):
    def __init__(self, key: str):
        self.key = key
        self.message = f"Missing settings key: {key}"
        super().__init__(self.message)


class IncorrectSettingsTypeError(Exception):
    def __init__(self, key: str):
        self.key = key
        self.message = f"Incorrect settings type: {key}"
        super().__init__(self.message)
