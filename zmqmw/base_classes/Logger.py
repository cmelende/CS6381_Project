class Logger:
    """
    This is a base class (although not abstract) that initially does nothing. It is fundamentally
    an interface that a user can override to provide more functionality.
    """
    def log(self, val: str):
        pass
