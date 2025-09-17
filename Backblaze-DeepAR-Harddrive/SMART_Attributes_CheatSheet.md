# SMART Attributes Cheat Sheet for Failure Risk

- **smart_197_raw (Current Pending Sector Count)**: Imminent failure signal; sectors awaiting reallocation. Backup immediately and plan replacement.
- **smart_1_raw (Read Error Rate)**: Rising read errors often precede unstable sectors; strong leading indicator.
- **smart_5_raw (Reallocated Sectors Count)**: Sectors already retired; increasing trend indicates surface degradation history.
- **smart_7_raw (Seek Error Rate)**: Head movement errors; can indicate mechanical instability.
- **smart_187_raw (Reported Uncorrectable Errors)**: Errors unrecoverable by ECC; severe reliability concern.
- **smart_188_raw (Command Timeout)**: Aborted operations due to timeouts; could be firmware or mechanical.
- **smart_198_raw (Uncorrectable Sector Count)**: Definitively bad sectors; critical indicator similar to 187.

Notes:
- Track both absolute values and rates of change.
- Combine with contextual signals (temperature, power-on hours, drive age) for better risk scoring.
