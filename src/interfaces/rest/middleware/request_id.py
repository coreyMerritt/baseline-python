import ulid


class RequestIDMiddleware:
  def __init__(self, app):
    self.app = app

  async def __call__(self, scope, receive, send):
    if scope["type"] != "http":
      return await self.app(scope, receive, send)
    headers = dict(scope.get("headers", []))
    incoming_corr = headers.get(b"x-correlation-id")
    correlation_id = (
      incoming_corr.decode() if incoming_corr else ulid.new().str
    )
    request_id = str(ulid.new().str)
    scope.setdefault("state", {})
    scope["state"]["request_id"] = request_id
    scope["state"]["correlation_id"] = correlation_id

    async def send_with_ids(message):
      if message["type"] == "http.response.start":
        message.setdefault("headers", [])
        message["headers"].append(
          (b"x-request-id", request_id.encode())
        )
        message["headers"].append(
          (b"x-correlation-id", correlation_id.encode())
        )
      await send(message)

    return await self.app(scope, receive, send_with_ids)
