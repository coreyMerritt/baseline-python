## Interface->REST->Routes
| Exceptions | When | Details |
|----------|----------|----------|
| Handling | Never | There is no good reason to handle an exception at the routes-level. |
| Translation | Often | Non-HTTPExceptions should never make it to the routes-level. However, if one does, it always should be translated to a HTTPException at the routes-level. |

| Logging Level | When | Details |
|----------|----------|----------|
| Debug | Never | There is no appropriate debug info at the routes-level. |
| Info | Never | API info should have been logged at the controllers-level. |
| Warning | Never | Warnings should have been handled at the controllers-level. |
| Error | Never | Errors should have been logged at the controllers-level. |
| Critical | Always | Critical logging should always be done at the routes-level if a non-HTTPException ever bubbles up. |