from dataclasses import dataclass


@dataclass(frozen=True)
class TokenIssuerConfig():
  time_to_live: float
