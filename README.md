# rcv
Maine Congressional District 2 (2018) Ranked Choice Voting Replication
by Nathan Tefft, Ph.D., 11/29/2018

This notebook uses an open source platform to replicate the Maine Congressional District 2 ranked choice voting results certified to the Governor on 11/26/18 (obtained from https://www.maine.gov/sos/cec/elec/results/results18.html#Nov6).

The replication implements the rank-choiced voting rules as provided in 21-A M.R.S.A. Chapter 723-A, sub-chapter 1, described at https://www.maine.gov/sos/cec/elec/upcoming/pdf/250rcvnew.pdf.

Although the rules allow for a "batch elimination" based on mathematical impossibility (used by the Secretary of State's office), I simply run subsequent instant runoffs to demonstrate the equivalence of the two approaches.

The replication was specifically written for the Maine Congressional District 2 race (2018), so it would need to be modified to replicate other races.

The code may not be particularly efficient, and I hope to one day improve its efficiency, but it transparently implements the process for those familiar with the Python language.
