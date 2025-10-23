## Interface->REST->Controllers
| Exceptions | When | Details |
|----------|----------|----------|
| Handling  | Rarely  | There should rarely be a meaningful way to perform fallbacks at the controller level. Exceptions may be made.  |
| Translation  | Always  | If an exception is not handled, it should always be translated into an HTTPException for Routes.  |

| Logging Level | When | Details |
|----------|----------|----------|
| Debug  | Rarely  | Typically, information at the controllers-level should be Info. Exceptions may be made.  |
| Info  | Always  | Every public method should contain at least 1 info log.  |
| Warning  | Sometimes  | Use your best judgement. |
| Error  | Often  | If an error occured, it should always be logged at the controllers-level.  |
| Critical  | Rarely  | Typically reserved for Routes layer.  |