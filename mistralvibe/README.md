# Mistral Vibe — Home Assistant App

Run [Mistral Vibe CLI](https://github.com/mistralai/mistral-vibe) (Mistral AI's
open-source agentic coding agent powered by Devstral 2) directly inside Home
Assistant. Browser terminal in the sidebar, full HA API access through
`hass-mcp`, persistent state under `/data/vibe`.

## Quick start

1. Add this repository to **Settings → Apps → Add-on Store → ⋮ →
   Repositories**.
2. Install **Mistral Vibe**, paste a Mistral API key into the **Configuration**
   tab, start the app, open the Web UI.
3. Type `vibe` and start asking things like *"What automations didn't run last
   night?"* or *"Add a sunset trigger to scene.evening_lights"*.

See [`DOCS.md`](./DOCS.md) for full configuration, architecture and security
details.

## Drop-in alternative to `claudecode`

This add-on is a fork of
[robsonfelix/claudecode](https://github.com/robsonfelix/robsonfelix-hass-addons),
adapted for Mistral Vibe instead of Claude Code. Same UX, same MCP-based HA
integration, different (open-weight) engine. Both apps can run side-by-side.

## License

Apache 2.0
