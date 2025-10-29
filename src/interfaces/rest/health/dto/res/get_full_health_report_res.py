from pydantic import BaseModel


class GetFullHealthReportRes(BaseModel):
  healthy: bool
