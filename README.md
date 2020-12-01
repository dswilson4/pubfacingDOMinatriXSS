# This repository includes

1. DOMinatriXSS JavaScript library
2. DOMinatriXSStatic JavaScript library
3. git patch to be applied to Chromium project (targeting Blink browser engine specifically)
4. Fiddler Script used for testing of DOMinatriXSS performance overhead, could be used for future compatibility studies and extended testing

# Patch instructions
The patch included in this repository was applied after the below commit hash.  The below git hash is included in the event that someone would like to test the disable-dynamic functionality and is having trouble with merge conflicts at commit later than that of the below git hash in the Chromium repo:

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
