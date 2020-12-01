# pubfacingDOMinatriXSS

Path after commit hash: 5ae5e597e7bf1f3f86d045a32723ab1b2cfda841

git log for context:
Author: REDACT <hollingum@google.com>
Date:   Mon Sep 28 07:28:28 2020 +0000

    Propagate ordinal motion to Exo clients (if it is available)

    On some platforms (including CrOS, as of crrev.com/c/2277694) ordinal
    motion will be available as part of mouse motion events.

    We use ordinal motion to provide unaccelerated motion in the
    zwp_relative_pointer interface. In the event that ordinal motion is not
    available, we default to the old behaviour (i.e. using accelerated
    motion).

    This behaviour is guarded by a flag, as the units it provides on CrOS
    are disproportionately small (compared with the standard cursor
