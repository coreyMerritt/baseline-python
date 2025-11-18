# Infrastructure

| Exceptions | When | Details |
|----------|----------|----------|
| Handling | Sometimes | If a fallback can preserve correctness and business intent, do it. |
| Translation | Sometimes | If an exception could be handled at the service layer, it should always be translated into an infrastructure-level exception. |

| Logging Level | When | Details |
|----------|----------|----------|
| Debug | Sometimes | If meaningful technical data can be logged, do it. |
| Info | Never | Reserved for interface layers. |
| Warning | Rarely | Use your best judgement. |
| Error | Rarely | Typically when handling errors, you should either be using Warning or translating/raising the error, but exceptions can be made with good judgement. |
| Critical | Never | Reserved for interface layers. |