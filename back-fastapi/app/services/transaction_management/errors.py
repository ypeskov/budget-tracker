class InvalidTransaction(Exception):
    def __init__(self, detail: str):
        self.detail = detail
