from dataclasses import dataclass


@dataclass
class LogError:
  name: str
  message: str
  stack: str
