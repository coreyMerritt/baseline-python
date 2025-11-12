## Services
| Exceptions | When | Details |
|----------|----------|----------|
| Handling | Sometimes | If a meaningful fallback can occur, do it, otherwise translate the exception. |
| Translation | Often | If an exception is not handled, it should always be translated into a service-level exception. |

| Logging Level | When | Details |
|----------|----------|----------|
| Debug | Sometimes | If meaningful orchestration data can be logged, do it. |
| Info | Never | Reserved for interface layers. |
| Warning | Sometimes | Use your best judgement. |
| Error | Rarely | Typically when handling errors, you should either be using Warning or translating/raising the error, but exceptions can be made with good judgement. |
| Critical | Never | Reserved for interface layers. |
