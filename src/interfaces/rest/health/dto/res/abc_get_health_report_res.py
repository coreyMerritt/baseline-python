from abc import ABC
from pydantic import BaseModel


class GetHealthReportRes(ABC, BaseModel):
  healthy: bool
