# Domain

| Exceptions | When | Details |
|----------|----------|----------|
| Handling | Rarely | Typically domain-level code shouldn't have a meaningful way to do exception handling. Exceptions may be made. |
| Translation | Sometimes | If an exception could potentially be handled at the service/interface-levels, it should be translated into a domain-level exception. |

| Logging Level | When | Details |
|----------|----------|----------|
| Debug | Never | Domain object should not get a logger. |
| Info | Never | Domain object should not get a logger. |
| Warning | Never | Domain object should not get a logger. |
| Error | Never | Domain object should not get a logger. |
| Critical | Never | Domain object should not get a logger. |