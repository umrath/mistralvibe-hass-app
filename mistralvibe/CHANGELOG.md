# Changelog

All notable changes to this app will be documented in this file.

## 1.0.0 — 2026-04-29

### Added
- Initial release.
- Mistral Vibe CLI (latest from PyPI) installed via `uv tool install`.
- `hass-mcp` MCP server pre-configured to talk to Home Assistant Core via the
  Supervisor API — no manual long-lived token needed.
- Browser terminal (ttyd) wired into HA ingress.
- Add-on options for API key, active model, default agent (incl. read-only
  `plan` mode), auto-approve, telemetry and CLI auto-update.
- Persistent state under `/data/vibe` (config, history, session logs).
- AppArmor profile.
- Multi-arch builds: `amd64`, `aarch64`, `armv7`, `armhf`, `i386`.
