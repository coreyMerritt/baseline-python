from dataclasses import dataclass

from shared.models.configs.base_config import Config

@dataclass(frozen=True)
class TypicodeConfig(Config):
  placeholder: str
