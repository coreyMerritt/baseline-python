## Interface->REST->Routes
| Exceptions | When | Details |
|----------|----------|----------|
| Handling | Never | There is no good reason to handle an exception at the routes-level. |
| Translation | Never | Exceptions should be translated at the controller-level |

| Logging Level | When | Details |
|----------|----------|----------|
| Debug | Never | There is no appropriate debug info at the routes-level. |
| Info | Never | API info should have been logged at the controllers-level. |
| Warning | Never | Warnings should have been handled at the controllers-level. |
| Error | Never | Errors should have been logged at the controllers-level. |
| Critical | Never | Critical errors should have been logged at the controllers-level. |