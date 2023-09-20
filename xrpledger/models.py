from pydantic import BaseModel
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.models.currencies import XRP, IssuedCurrency

XrplAmount = IssuedCurrencyAmount | str


class Wallet(BaseModel):
    """
    A model representing a XRP Ledger wallet.
    """

    address: str
    public_key: str
    private_key: str


class Token(BaseModel):
    """
    A model representing a token on the XRP Ledger.
    """

    currency: str
    issuer: str

    def to_xrpl_currency(self) -> IssuedCurrency | XRP:
        """
        Convert the Token model to an IssuedCurrency or XRP model.

        Returns:
            IssuedCurrency | XRP: Token instances of xrpl
        """
        if self.currency == "XRP" and self.issuer == "":
            return XRP()
        return IssuedCurrency(
            currency=self.currency,
            issuer=self.issuer,
        )

    def to_xrpl_amount(self, value: str) -> XrplAmount:
        """
        Convert the Token model to an IssuedCurrencyAmount or XRP amount (=string).

        Returns:
            XrplAmount: An instance of XrplAmount representing the amount details of a token or XRP.
        """
        if self.currency == "XRP" and self.issuer == "":
            return value
        return IssuedCurrencyAmount(
            currency=self.currency,
            issuer=self.issuer,
            value=value,
        )

    def __str__(self) -> str:
        return f"{self.currency}.{self.issuer}"


class Amount(BaseModel):
    """
    A model representing the amount details of a token or XRP.
    """

    token: Token
    value: str

    def to_xrpl_amount(self) -> XrplAmount:
        """
        Convert the Amount model to an XrplAmount model.

        Returns:
            XrplAmount: An instance of XrplAmount representing the amount details of a token or XRP.
        """
        return self.token.to_xrpl_amount(self.value)
