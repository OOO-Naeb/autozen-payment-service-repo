from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette import status

from src.application.exceptions import InactiveCompanyError, ExistingBankAccountError, UserNotActiveError
from src.core.exceptions import PaymentServiceError
from src.infrastructure.exceptions import CompanyServiceError, UserServiceError


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except PaymentServiceError as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={"success": False, "message": exc.detail},
            )
        except CompanyServiceError as exc:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": str(exc)}
            )
        except InactiveCompanyError as exc:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": str(exc)}
            )
        except ExistingBankAccountError as exc:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"detail": str(exc)}
            )
        except UserServiceError as exc:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": f"User service error occurred: {exc}"}
            )
        except UserNotActiveError as exc:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": str(exc)}
            )
        except ValueError as exc:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": f"Error while adding the payment method: {exc}"}
            )
        except Exception as exc:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": f"Unhandled error occurred in the Payment Service: {exc}"}
            )
