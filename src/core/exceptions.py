class PaymentServiceException(Exception):
    """Base exception for Payment Service errors."""
    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.detail)
