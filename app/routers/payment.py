from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from xrpl.models.transactions import Payment
from xrpl.wallet import Wallet

from app.models import PaymentRequest, XrplClient
from xrpledger.client import get_xrpl_rpc_client
from xrpledger.transaction import submit_transaction

router = APIRouter(
    prefix="/payment",
    tags=["payment"],
    dependencies=[Depends(get_xrpl_rpc_client)],
)


@router.post("/send")
async def send_token(request: PaymentRequest, client: XrplClient) -> JSONResponse:
    """
    Process a token send on the XRPL. Token is including XRP.

    send_max and destination token should be the same.

    Allows a user to send a specified amount of a token to another
    XRPL address.
    """
    if request.send_max and (request.send_max.token) != (request.amount.token):
        raise HTTPException(status_code=422, detail="send_max and destination tokens should be the same.")

    if request.account == request.destination:
        raise HTTPException(status_code=422, detail="source and destination should be the different.")

    transaction = Payment(
        account=request.account,
        destination=request.destination,
        amount=request.amount.to_xrpl_amount(),
        send_max=request.send_max.to_xrpl_amount() if request.send_max else None,
    )

    result = await submit_transaction(
        transaction=transaction,
        wallet=Wallet(public_key=request.public, private_key=request.secret),
        client=client,
    )

    status_code = 400 if "error" in result else 200

    return JSONResponse(content=result, status_code=status_code)


@router.post("/swap")
async def swap_token(
    request: PaymentRequest,
    client: XrplClient,
) -> JSONResponse:
    """
    Process a token purchase on the XRPL.

    Allows a user to buy a specified amount of a token by providing
    the send_max currency details, including the max value they are
    willing to spend.
    """
    if request.send_max and (request.send_max.token) == (request.amount.token):
        raise HTTPException(
            status_code=422, detail="send_max and destination tokens should be the different."
        )

    if request.account != request.destination:
        raise HTTPException(status_code=422, detail="source and destination should be the same.")

    transaction = Payment(
        account=request.account,
        destination=request.destination,
        amount=request.amount.to_xrpl_amount(),
        send_max=request.send_max.to_xrpl_amount() if request.send_max else None,
        deliver_min=request.deliver_min.to_xrpl_amount() if request.deliver_min else None,
    )

    result = await submit_transaction(
        transaction=transaction,
        wallet=Wallet(public_key=request.public, private_key=request.secret),
        client=client,
    )

    status_code = 400 if "error" in result else 200

    return JSONResponse(content=result, status_code=status_code)
