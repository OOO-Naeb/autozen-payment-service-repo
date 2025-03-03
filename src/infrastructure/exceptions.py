from src.core.exceptions import PaymentServiceError


class InvalidPaymentMethodError(PaymentServiceError):
    """Exception for invalid payment method information."""
    def __init__(self, detail: str = "Invalid payment method information."):
        super().__init__(detail=detail, status_code=400)


class RabbitMQError(PaymentServiceError):
    """Exception for RabbitMQ service being unavailable."""
    def __init__(self, detail: str = "RabbitMQ is unavailable."):
        super().__init__(detail=detail, status_code=503)


class PaymentGatewayError(PaymentServiceError):
    """Exception for payment gateway errors."""
    def __init__(self, detail: str = "Payment gateway error."):
        super().__init__(detail=detail, status_code=500)


class UserServiceError(Exception):
    """Exception for User Service's responses errors."""
    def __init__(self, detail: str = "An error occurred in the User Service.", status_code: int = 500):
        self.status_code = status_code
        super().__init__(detail)


class CompanyServiceError(Exception):
    """Exception for Company Service's responses errors."""
    def __init__(self, detail: str = "An error occurred in the Company Service.", status_code: int = 500):
        self.status_code = status_code
        super().__init__(detail)
