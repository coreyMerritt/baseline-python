from infrastructure.logger.models.logs.raw_http_request_info import RawHTTPRequestInfo
from infrastructure.logger.models.logs.raw_http_response_info import RawHTTPResponseInfo
from interfaces.rest.models.foo_project_name_request import FooProjectNameRequest


class FooProjectNameRequestMapper:
  @staticmethod
  def to_raw_http_req_info(req: FooProjectNameRequest) -> RawHTTPRequestInfo:
    return RawHTTPRequestInfo(
      correlation_id=req.correlation_id,
      request_id=req.request_id,
      client_ip=req.client_ip,
      endpoint=req.endpoint,
      method=req.method,
      route=req.route,
      user_agent=req.user_agent
    )

  @staticmethod
  def to_raw_http_res_info(req: FooProjectNameRequest, status: int, duration_ms: float) -> RawHTTPResponseInfo:
    return RawHTTPResponseInfo(
      correlation_id=req.correlation_id,
      request_id=req.request_id,
      duration_ms=duration_ms,
      status=status
    )
