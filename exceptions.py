class JotterError(Exception):
    pass

class ResourceNotFoundError(JotterError):
    pass

class DatabaseError(JotterError):
    pass

class InvalidInputError(JotterError):
    pass