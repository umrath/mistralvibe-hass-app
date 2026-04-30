# Changelog

All notable changes to this app will be documented in this file.

## 1.7.2 — 2026-04-30

### Fixed
- Documentation: replaced outdated hass-mcp references with custom MCP server
- Removed addon_config from filesystem layout (not mounted)

## 1.7.1 — 2026-04-30

### Added
- Extended security documentation: token handling, hassio_role, AppArmor, auto_approve risks

## 1.7.0 — 2026-04-30

### Fixed
- resolve_model() now falls back to hardcoded defaults if model resolution returns empty string

## 1.6.9 — 2026-04-30

### Fixed
- SUPERVISOR_TOKEN guard with 5s timeout before HA version query in init script

## 1.6.8 — 2026-04-30

### Fixed
- ha_list_areas tool name corrected in system prompt
- Dockerfile label type: addon → app
- ha-logs and ha-errors aliases now use direct Supervisor API instead of missing ha CLI

## 1.6.7 — 2026-04-30

### Added
- Shell aliases: v (vibe-launcher), ha-config, ha-logs, ha-errors

## 1.6.6 — 2026-04-30

### Added
- ha.md system prompt generated dynamically at startup including HA version and path mapping

## 1.6.5 — 2026-04-30

### Added
- Configurable terminal_font_size (10-24px) and terminal_theme (dark/light)

## 1.6.4 — 2026-04-30

### Added
- Documentation: Le Chat Pro included budget and pay-as-you-go API key setup

## 1.6.3 — 2026-04-30

### Added
- ingress_stream: true for better streaming performance
- ttyd: scrollback=20000, --ping-interval 30, --max-clients 5
- Docker HEALTHCHECK

## 1.6.2 — 2026-04-30

### Fixed
- HA_TOKEN restored in mcp_servers.env — Vibe does not inherit shell environment to MCP child processes

## 1.6.0 — 2026-04-30

### Changed
- Documentation: renamed add-on to app throughout

## 1.5.9 — 2026-04-30

### Removed
- ha_get_vibe_usage MCP tool — session logs contain no token data

## 1.5.8 — 2026-04-30

### Fixed
- Removed duplicate entries in de.yaml translations

## 1.5.5 — 2026-04-30

### Fixed
- ha.md and VIBE.md copied correctly on startup
- reset_data and session_persistence options restored in config.yaml
- Removed duplicate entries in en.yaml translations

## 1.5.1 — 2026-04-29

### Security
- HA_TOKEN removed from config.toml template — passed via inherited environment only

## 1.4.8 — 2026-04-29

### Fixed
- py3-pip added to apk packages (required for fastmcp/httpx)
- Removed invalid --mouse flag from ttyd

## 1.4.0 — 2026-04-29

### Changed
- Replaced hass-mcp with custom FastMCP server (server.py)
- ha_get_error_log limited to max 200 lines
- ha_list_entities, ha_list_automations limited to 50 results by default

## 1.0.0 — 2026-04-29

### Added
- Initial release
- Mistral Vibe CLI installed via uv tool install
- Custom MCP server for Home Assistant Core API access via Supervisor token
- Browser terminal (ttyd) via HA ingress
- App options: API key, active model, default agent, auto-approve, telemetry, CLI auto-update
- Persistent state under /data/vibe (config, history, session logs)
- AppArmor profile
- Multi-arch builds: amd64, aarch64

## 1.7.4 — 2026-04-30

### Added
- ha CLI binary installed in Dockerfile (from github.com/home-assistant/cli)
- ha-logs and ha-errors aliases restored to use ha CLI

## 1.7.3 — 2026-04-30

### Changed
- CHANGELOG rewritten with full history

## 1.7.2 — 2026-04-30

### Fixed
- Documentation: replaced outdated hass-mcp references with custom MCP server
- Removed addon_config from filesystem layout (not mounted)
