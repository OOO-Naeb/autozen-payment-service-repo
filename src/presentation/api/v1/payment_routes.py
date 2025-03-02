from typing import Annotated
from fastapi import APIRouter, Body, Depends

from src.application.exceptions import UserNotActiveError, InactiveCompanyError
from src.application.use_cases.add_bank_account import AddBankAccountUseCase
from src.application.use_cases.add_bank_card import AddBankCardUseCase
from src.core.dependencies import get_add_bank_card_use_case, get_add_bank_account_use_case, get_logger
from src.core.logger import LoggerService
from src.domain.models.payment_methods import CardPaymentMethod, BankAccountPaymentMethod
from src.domain.schemas import AddBankCardDTO, AddBankAccountDTO
from src.infrastructure.exceptions import UserServiceError, CompanyServiceError
from src.presentation.schemas import AddBankCardRequest, AddBankAccountResponse, \
    AddBankAccountRequest

payment_router = APIRouter(
    tags=["Payment"],
    prefix="/api/v1/payment",
)


from fastapi import HTTPException, status

@payment_router.post('/bank_card', response_model=CardPaymentMethod, status_code=201)
async def add_bank_card(
        card_info: Annotated[AddBankCardRequest, Body(...)],
        use_case: Annotated[AddBankCardUseCase, Depends(get_add_bank_card_use_case)],
        logger: Annotated[LoggerService, Depends(get_logger)]
) -> CardPaymentMethod:
    try:
        bank_card_domain_dto = AddBankCardDTO(**card_info.model_dump())
        card_domain_model = await use_case.execute(bank_card_domain_dto)

        return card_domain_model
    except ValueError as exc:
        logger.critical(f"Error while adding the bank card: {exc}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error while adding the bank card: {exc}"
        )
    except UserServiceError as exc:
        logger.warning(f"User not found: {exc}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found: {exc}"
        )
    except UserNotActiveError as exc:
        logger.warning(f"User is not active: {exc}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{exc}"
        )
    except Exception as exc:
        logger.critical(f"Unhandled error: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unhandled error: {exc}"
        )



@payment_router.post('/bank_account', response_model=BankAccountPaymentMethod, status_code=201)
async def add_bank_account(
        bank_account_info: Annotated[AddBankAccountRequest, Body(...)],
        use_case: Annotated[AddBankAccountUseCase, Depends(get_add_bank_account_use_case)],
        logger: Annotated[LoggerService, Depends(get_logger)]
) -> BankAccountPaymentMethod:
    """
    CONTROLLER: Add a payment method to the company's account.
    Passes the query to the 'AddBankAccountUseCase'.

    Args:
        bank_account_info (AddBankAccountRequest): The bank account information to add.
        use_case (AddBankAccountUseCase): The use case to process the operation.
        logger (LoggerService): The logger service.

    Returns:
        AddBankAccountResponse: A response schema for the added bank account.
    """
    try:
        bank_account_domain_dto = AddBankAccountDTO(**bank_account_info.model_dump())
        bank_account_domain_model = await use_case.execute(bank_account_domain_dto)

        return bank_account_domain_model
    except ValueError as exc:
        logger.critical(f"Error while adding the bank card: {exc}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error while adding the bank card: {exc}"
        )
    except CompanyServiceError as exc:
        logger.warning(f"Company not found: {exc}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company not found: {exc}"
        )
    except InactiveCompanyError as exc:
        logger.warning(f"Company is not active: {exc}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{exc}"
        )
    except Exception as e:
        logger.error(f"Error occurred while adding the bank account: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occurred while adding the bank account: {str(e)}"
        )
