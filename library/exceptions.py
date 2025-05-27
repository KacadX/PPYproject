"""GENERAL EXCEPTIONS"""

class ReaderOrBookNotFound(Exception):
    pass

"""READER EXCEPTIONS"""

class InvalidPhoneNumber(Exception):
    """Raised when phone number is invalid."""
    pass

class NoReader(Exception):
    """Raised when there's no reader of specific ID"""
    pass

"""BOOK EXCEPTIONS"""

class PageCountException(Exception):
    """Raised when value of page count is invalid"""
    pass

class BookLentToSomeone(Exception):
    """Raised when book is not available to lend"""
    pass

class BookReserved(Exception):
    """Raised when book is reserved by someone else"""
    pass
