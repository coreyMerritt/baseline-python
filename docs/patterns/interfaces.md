# Interfaces

| Exceptions | When | Details |
|----------|----------|----------|
| Handling | Rarely | There should rarely be a meaningful way to perform fallbacks at the interface level. Exceptions may be made. |
| Translation | Never | Error translation should be complete by the time its in an interface. |

| Logging Level | When | Details |
|----------|----------|----------|
| Debug | Rarely | Typically, information at the interface-level should be Info. Exceptions may be made. |
| Info | Always | Every public method should contain at least 1 info log. |
| Warning | Sometimes | Use your best judgement. |
| Error | Often | If an error occured, it should always be logged at the interface-level. |
| Critical | Rarely | The use case for Critical is currently undefined. Use your judgement. |