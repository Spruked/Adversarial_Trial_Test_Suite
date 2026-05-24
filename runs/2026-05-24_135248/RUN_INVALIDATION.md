# RUN INVALIDATION NOTICE

- run_id: 2026-05-24_135248
- status: ABORTED_INVALID_ENDPOINT_MODE
- timestamp: 2026-05-24T14:09:27-05:00
- reason: /api/query returned echo-mode responses ("Query processed: ..."), so adversarial adjudication criteria were not executable.
- classification: orchestration dry-run only (queue/logging/toolchain), not capability verdict.
- action_required:
  1) fix /api/query reasoning contract
  2) rerun from fresh run_id
