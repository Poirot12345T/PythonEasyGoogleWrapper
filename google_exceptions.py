class UnableToConnect(Exception):
    def __init__(self, message="something went wrong"):
        super().__init__(message)

class UnknownFileType(Exception):
    pass

class BadInputType(Exception):
    pass
