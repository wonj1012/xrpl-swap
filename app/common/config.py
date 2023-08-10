import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from app.models.types import Wallet

load_dotenv()

ENV = os.getenv("XRPL_ENV", "dev")


class CommonSettings(BaseSettings):
    """
    Common settings for the API.
    """

    PROJECT_NAME: str = "XRPL Swap API"
    API_VERSION: str = "0.0.1"
    API_PREFIX: str = "/api/v1"

    DEBUG_MODE: bool = False

    json_rpc_url: str
    websocket_url: str
    wallet: Wallet

    class Config:
        """
        Configuration for the settings.
        """

        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


class DevSettings(CommonSettings):
    """
    Development settings for the API.
    """

    DEBUG_MODE: bool = True

    json_rpc_url: str = "https://s.altnet.rippletest.net:51234"  # Testnet
    websocket_url: str = "wss://s.altnet.rippletest.net:51233"  # Testnet
    wallet: Wallet = Wallet(
        address="rnwjHhgiNQSYfJndh1AiRBmcRKmPu2qzGs",
        public_key="ED08DEED03322A7BB4C33FEDF6B416E37E45B3927ABDAE54FF6BCFCCB7A9C33C78",
        private_key="ED98B5A858F1BCD5F7A0F2306521E57044385CC342D3DAB604C6CCBAF01EDE63AE",
    )


class AmmDevSettings(CommonSettings):
    """
    AMM-Devnet settings for the API.
    """

    DEBUG_MODE: bool = True

    json_rpc_url: str = "https://amm.devnet.rippletest.net:51234"  # AMM-Devnet
    websocket_url: str = "wss://amm.devnet.rippletest.net:51233"


class ProdSettings(CommonSettings):
    """
    Production settings for the API.
    """

    DEBUG_MODE: bool = False

    json_rpc_url: str = "https://s1.ripple.com:51234"  # Mainnet
    websocket_url: str = "wss://s1.ripple.com"


def get_settings() -> CommonSettings:
    """
    Get the settings for the API.

    Returns:
        CommonSettings: The settings for the API.
    """
    if ENV == "prod":
        return ProdSettings()  # type: ignore
    if ENV == "amm-dev":
        return AmmDevSettings()  # type: ignore
    if ENV == "dev":
        return DevSettings()  # type: ignore
    return CommonSettings()  # type: ignore


settings = get_settings()