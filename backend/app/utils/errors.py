"""Custom error classes for business logic validation"""


class TokenExpiredError(Exception):
    """Raised when JWT token has expired"""
    pass


class InvalidTokenError(Exception):
    """Raised when JWT token is invalid or malformed"""
    pass


class ActiveSessionExistsError(Exception):
    """Raised when trying to create a session but an active session already exists"""
    pass


class SessionNotFoundError(Exception):
    """Raised when session is not found"""
    pass


class SessionAlreadyEndedError(Exception):
    """Raised when trying to end a session that is already ended"""
    pass


class InvalidTipRateError(Exception):
    """Raised when tip rate is not in allowed values (0, 5, 10, 15, 20)"""
    pass


class SessionNotActiveError(Exception):
    """Raised when trying to create order for inactive session"""
    pass


class MenuNotAvailableError(Exception):
    """Raised when trying to order unavailable menu"""
    pass


class InvalidQuantityError(Exception):
    """Raised when order quantity is less than or equal to 0"""
    pass


class OrderNotFoundError(Exception):
    """Raised when order is not found"""
    pass


class InvalidStatusError(Exception):
    """Raised when order status value is invalid"""
    pass
