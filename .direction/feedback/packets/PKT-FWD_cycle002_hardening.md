# PKT-FWD — forward-tool fail-closed hardening (C1B-03/04/05; OWNER SIGNATURE — protected prefix tools/forward_)

Nov-2026-window relevance. Full evidence: rot2_C1B_2026-08-05.md.
1. forward_validate: enforce the FULL sealed-spec §6 record contract
   (currently a subset) + correct spec §4's false mechanism sentence.
2. forward_prepare: post-seal guard on PROTOCOL.md writes; fail-closed on
   pin-source drop and UNRESOLVED model pin.
3. forward_enumerate: fail-closed on fetch failure; bounded trailing
   window (fetch-date-independence for cycle_002).
Each is an S-sized fail-open→fail-closed conversion with a test; exact
shapes in the report. Signature converts this packet into a TASK for the
build harness (same pipeline as all cycles). Timing suggestion: before
any cycle_002 preparation begins.
