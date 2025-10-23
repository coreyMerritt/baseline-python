## Domain
| Exceptions | When | Details |
|----------|----------|----------|
| Handling  | Rarely  | Typically domain-level code shouldn't have a meaningful way to do exception handling. Exceptions may be made.  |
| Translation  | Often  | If an exception is not handled, it should always be translated into a domain-level exception.  |

| Logging Level | When | Details |
|----------|----------|----------|
| Debug  | Sometimes  | If meaningful technical data can be logged, do it.  |
| Info  | Never  | Reserved for interface layers.  |
| Warning  | Sometimes  | Use your best judgement. |
| Error  | Rarely  | Typically when handling errors, you should either be using Warning or translating/raising the error, but exceptions can be made with good judgement.  |
| Critical  | Never  | Reserved for interface layers.  |