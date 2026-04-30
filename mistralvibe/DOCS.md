# Mistral Vibe — Home Assistant App

Run **Mistral Vibe CLI** (Mistral AI's open-source agentic coding agent powered
by Devstral 2) directly inside Home Assistant. Talk to your smart home in
natural language through a browser terminal that has full access to entities,
services, automations and YAML configs via the `hass-mcp` MCP server.

## What you get

- A web terminal in the HA sidebar (no SSH, no separate IDE)
- Multi-file editing across `/config`, `/share` and `/addon_config`
- Live entity & service inspection via the Supervisor API
- Persistent sessions, command history and conversation logs in `/data/vibe`
- Open-source, Apache 2.0 licensed CLI on top of open-weight Devstral models
- A read-only "plan" mode for exploration without any writes

## First-time setup

1. Create a Mistral API key at https://console.mistral.ai/.
2. Open this app, switch to the **Configuration** tab and paste your key
   into `mistral_api_key`. Save.
3. Start the app. Open the **Web UI** (or the sidebar entry).
4. The terminal opens directly in `/config` with Vibe ready to go. Try:
   - `List all my automations`
   - `Why did motion_sensor_hallway not trigger last night?`
   - `Create an automation to turn off all lights when nobody is home`

No long-lived HA token is required — the app uses the Supervisor token
internally to authenticate `hass-mcp` against Home Assistant Core.

## Configuration options

| Option | Default | Description |
| --- | --- | --- |
| `mistral_api_key` | *(required)* | Your Mistral API key. Stored in `/data/vibe/.env`, never sent anywhere except `api.mistral.ai`. |
| `active_model` | `devstral-2` | One of `devstral-2`, `devstral-small-2`, `magistral-medium`, `mistral-medium-latest`, `codestral-latest`. Switch on the fly inside Vibe with `/config`. |
| `default_agent` | `default` | `default` asks before every tool call. `plan` is a fully read-only agent — Vibe can look around but cannot edit, run shells or call services. |
| `auto_approve` | `false` | When `true`, Vibe skips the confirmation prompt before running tools. **Convenient but dangerous.** Leave off unless you really know what you're doing. |
| `auto_update_cli` | `true` | Lets Vibe self-update on launch when a newer release is on PyPI. Disable to pin the version that ships with the app. |
| `enable_telemetry` | `false` | Forwarded to Vibe as the `enable_telemetry` config flag. Off by default. |
| `log_level` | `info` | Controls the verbosity of the underlying `ttyd` server (`trace`, `debug`, `info`, `notice`, `warning`, `error`, `fatal`). |

Every option above maps 1:1 to a key the init script writes into
`/data/vibe/config.toml` or `/data/vibe/.env` — so you can also edit them
directly in a Vibe session if you want full control.

## File-system layout inside the app

| Path | Purpose |
| --- | --- |
| `/config` | Your Home Assistant configuration (mounted RW). Vibe's working dir. |
| `/share` | Shared data (mounted RW). |
| `/addon_config` | Configurable per-add-on data (mounted RW). |
| `/media` | Media folder (mounted RW). |
| `/ssl` | TLS certificates (mounted RO). |
| `/data/vibe` | Vibe state: `config.toml`, `.env`, `agents/`, `prompts/`, `logs/session/`, command history. Persists across restarts and updates. |

## Architecture

```
 ┌───────────────────┐ HTTP    ┌────────────────────────┐
 │  HA Frontend      │────────▶│  Supervisor Ingress    │
 │  (sidebar panel)  │◀────────│  (/api/hassio_ingress) │
 └───────────────────┘         └──────────┬─────────────┘
                                          │
                                          ▼
                              ┌──────────────────────────┐
                              │  ttyd  :7681             │
                              │  └─ bash                 │
                              │     └─ vibe-launcher     │
                              │        └─ mistral-vibe   │
                              └──────────┬───────────────┘
                                         │ stdio
                                         ▼
                              ┌──────────────────────────┐
                              │  hass-mcp (uvx)          │  ──REST──▶  HA Core
                              │  HA_URL, HA_TOKEN env    │   /api/states
                              └──────────────────────────┘   /api/services
```

`vibe-launcher` is the entry-point that loads the API key from `.env`,
applies the `auto_approve` / `default_agent` flags from app options and
execs the CLI. The hass-mcp server is started on demand by Vibe, as a stdio
child process, and inherits `HA_URL=http://supervisor/core` plus the
`SUPERVISOR_TOKEN`.

## Switching models on the fly

Inside a Vibe session, type `/config`. You'll see the list of models defined
in `/data/vibe/config.toml` — pick one and Vibe switches without restarting.

You can also add custom providers (Ollama, vLLM, on-prem Mistral) by editing
the `[[providers]]` and `[[models]]` blocks in that file. Local inference is
fully supported.

## Security notes

- The Mistral API key sits in `/data/vibe/.env` (mode `600`). Only this app
  can read it.
- The `SUPERVISOR_TOKEN` is the standard HA add-on token. The `hassio_role`
  is set to `manager`, the same level used by the official Studio Code Server
  add-on, so Vibe can manage entities, services, automations, snapshots, etc.
- AppArmor is **enabled by default**. The profile in `apparmor.txt` allows
  what the CLI needs (read/write under `/config`, `/share`, `/data` …) and
  denies the rest.
- For exploration without any side effects, set `default_agent: plan`.

## Differences vs. the Claude Code add-on

| Aspect | `claudecode` (robsonfelix) | `mistralvibe` (this) |
| --- | --- | --- |
| Engine | Claude Code (Anthropic, closed) | Mistral Vibe CLI (Apache 2.0, open) |
| Default model | Claude Sonnet | Devstral 2 (123B, open weights) |
| Auth | Anthropic OAuth (long URL flow) | Mistral API key in app options |
| Local inference | No | Yes (via Ollama / vLLM / on-prem) |
| HA bridge | hass-mcp via stdio | hass-mcp via stdio (same lib) |
| Web UI | ttyd terminal in ingress | ttyd terminal in ingress |
| State dir | `/data/claude` | `/data/vibe` |

The two apps can be installed side-by-side — they use different slugs and
different state directories.

## Troubleshooting

- **"No mistral_api_key configured" on start** — open the app's
  Configuration tab, paste a key, save, then restart.
- **Terminal opens but `vibe` says it can't reach `api.mistral.ai`** — check
  the host's outbound network. The app does not require any port forwards;
  it only needs HTTPS egress.
- **`hass` MCP tools fail with 401** — the `SUPERVISOR_TOKEN` is rotated
  whenever the app restarts. A simple app restart fixes it.
- **Want to start clean** — stop the app, delete `/data/vibe`, start again.
  Your app options will rebuild the config; only command history and
  session logs are lost.

## Credits

- [Mistral AI](https://mistral.ai) — Devstral 2 and Mistral Vibe CLI
- [voska/hass-mcp](https://github.com/voska/hass-mcp) — Home Assistant MCP server
- [tsl0922/ttyd](https://github.com/tsl0922/ttyd) — browser terminal
- [robsonfelix/robsonfelix-hass-addons](https://github.com/robsonfelix/robsonfelix-hass-addons) — the Claude Code add-on this is structurally based on
