"""
Security subsystem.

Provides:
- SQL sanitization
- PII scrubbing
- Prompt-injection defense
- Schema enforcement
- Output validation

All untrusted input MUST pass through this layer.
"""
