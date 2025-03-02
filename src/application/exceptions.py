class ApplicationError(Exception):
    """Base class for application layer related errors."""
    def __init__(self, message: str, status_code: int = 401):
        self.status_code = status_code
        super().__init__(message)


class CompanyNotFoundError(ApplicationError):
    """Raised when company is not found."""
    def __init__(self, message: str = "Company not found."):
        super().__init__(message=message, status_code=404)

class InactiveCompanyError(ApplicationError):
    """Raised when company account is inactive."""
    def __init__(self, status_code: int = 403, message: str = "Company is inactive."):
        super().__init__(message=message, status_code=status_code)

class InvalidPaymentMethodError(ApplicationError):
    """Raised when payment method is invalid."""
    def __init__(self, message: str = "Invalid payment method."):
        super().__init__(message=message, status_code=400)


class UserNotActiveError(ApplicationError):
    """Raised when user account is inactive."""
    def __init__(self, status_code: int = 403, message: str = "User account is inactive."):
        super().__init__(message=message, status_code=status_code)
