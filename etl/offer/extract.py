from xrpl.asyncio.clients import AsyncJsonRpcClient

from xrpledger.models import Token
from xrpledger.request import get_orderbook


async def extract_offers(
    taker_gets: Token,
    taker_pays: Token,
    client: AsyncJsonRpcClient,
) -> dict[str, any]:
    """
    Retrieves the offer data for a given token pair.

    Args:
        taker_gets (Token): The token that the taker is willing to offer.
        taker_pays (Token): The token that the taker wants in exchange.
        client (AsyncJsonRpcClient): An asynchronous JSON RPC client used to fetch the data.

    Returns:
        dict[str, Any]: A dictionary containing the orderbook offers.
    """
    orderbook_info = await get_orderbook(taker_gets, taker_pays, client)

    return orderbook_info["offers"]
