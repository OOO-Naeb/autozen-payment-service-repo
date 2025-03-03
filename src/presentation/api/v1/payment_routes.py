from typing import Annotated
from fastapi import APIRouter, Body, Depends

from src.application.use_cases.add_bank_account import AddBankAccountUseCase
from src.application.use_cases.add_bank_card import AddBankCardUseCase
from src.core.dependencies import get_add_bank_card_use_case, get_add_bank_account_use_case
from src.domain.models.payment_methods import CardPaymentMethod, BankAccountPaymentMethod
from src.domain.schemas import AddBankCardDTO, AddBankAccountDTO
from src.presentation.schemas import AddBankCardRequest, AddBankAccountRequest, APIResponse

payment_router = APIRouter(
    tags=["Payment"],
    prefix="/api/v1/payment",
)

@payment_router.post('/bank_card', response_model=APIResponse[CardPaymentMethod], status_code=201)
async def add_bank_card(
        card_info: Annotated[AddBankCardRequest, Body(...)],
        use_case: Annotated[AddBankCardUseCase, Depends(get_add_bank_card_use_case)],
) -> APIResponse[CardPaymentMethod]:
    """
    CONTROLLER: Add a payment method to the user's account.
    Passes the query to the 'AddBankCardUseCase'.

    Args:
        card_info (AddBankCardRequest): The card information to add to the user's account.
        use_case (AddBankCardUseCase): The payment use_case to process the operation.

    Returns:
        APIResponse: A response schema containing status code, message and bank response.
    """
    bank_card_domain_dto = AddBankCardDTO(**card_info.model_dump())
    card_domain_model = await use_case.execute(bank_card_domain_dto)

    return APIResponse(
        success=True,
        message='Payment method added successfully.',
        content={
            **card_domain_model.to_dict()
        }
    )



@payment_router.post('/bank_account', response_model=APIResponse[BankAccountPaymentMethod], status_code=201)
async def add_bank_account(
        bank_account_info: Annotated[AddBankAccountRequest, Body(...)],
        use_case: Annotated[AddBankAccountUseCase, Depends(get_add_bank_account_use_case)],
) -> APIResponse[BankAccountPaymentMethod]:
    """
    CONTROLLER: Add a payment method to the company's account.
    Passes the query to the 'AddBankAccountUseCase'.

    Args:
        bank_account_info (AddBankAccountRequest): The bank account information to add.
        use_case (AddBankAccountUseCase): The use case to process the operation.

    Returns:
        APIResponse: A response schema containing status code, message and bank response.
    """
    bank_account_domain_dto = AddBankAccountDTO(**bank_account_info.model_dump())
    bank_account_domain_model = await use_case.execute(bank_account_domain_dto)

    return APIResponse(
        success=True,
        message='Payment method added successfully.',
        content={
            **bank_account_domain_model.to_dict()
        }
    )
