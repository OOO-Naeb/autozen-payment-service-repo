class PaymentServiceException(Exception):
    """Base exception for Payment Service errors."""
    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.detail)


class InvalidPaymentMethodException(PaymentServiceException):
    """Exception for invalid payment method information."""
    def __init__(self, detail: str = "Invalid payment method information."):
        super().__init__(detail=detail, status_code=400)


class SourceUnavailableException(PaymentServiceException):
    """Exception for source service being unavailable."""
    def __init__(self, detail: str = "Source service is unavailable."):
        super().__init__(detail=detail, status_code=503)


class PaymentGatewayException(PaymentServiceException):
    """Exception for payment gateway errors."""
    def __init__(self, detail: str = "Payment gateway error."):
        super().__init__(detail=detail, status_code=400)
