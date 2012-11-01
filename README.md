gr-kx3
======

A trivial gnuradio project for use with the Elecraft KX3, under the GPLv3. 

It works.  Just about.  At the moment it doesn't track the VFO on the radio.  It
can, but there's a memory leak of about 1MB per second when it does, which is
very bad. In the short-term I'm going to add a button to sync with the VFO on
demand until I can resolve the problem with the polling method.

You can click in the waterfall (not in the spectrum plot) to re-tune the radio 
to that frequency.

Regarding frequency offsets from PBT settings and IF offset configurations, all
bets are off for now, until the support for the FI command is added to the
KX3.
