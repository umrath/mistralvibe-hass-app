# Disclaimer

No warranties whatsoever that the code in this repository is doing anything meaningful, is free of harm or may cause serious damage.
It's your sole responsibility to check the code thoroughly before running/using it.

If it fries your Home Assistant setup, burns your servers, eats your cats or buys bitcoins with all your money - it's your own fault.

You have been warned!

# Mistral Vibe – Home Assistant Add-ons

Home Assistant add-on that runs **Mistral Vibe CLI** (Mistral AI's open-source
agentic coding assistant powered by Devstral 2) directly inside Home Assistant.
It is a drop-in alternative to the
[robsonfelix/claudecode](https://github.com/robsonfelix/robsonfelix-hass-addons)
add-on, with the same browser-based terminal experience and MCP-based access to
the full Home Assistant API – just running on Mistral models instead of
Anthropic's Claude.

## What's inside

| Add-on | Description |
| --- | --- |
| **Mistral Vibe** (`./mistralvibe`) | Browser terminal running Mistral Vibe CLI with full Home Assistant integration via the `hass-mcp` MCP server. |

## Installation

In Home Assistant:

1. Go to **Settings → Add-ons → Add-on Store**.
2. Open the menu (⋮) in the top right and select **Repositories**.
3. Add the URL of this repository.
4. Install the **Mistral Vibe** add-on, configure your Mistral API key, start it,
   and open the web UI.

## Why a fork?

The original `claudecode` add-on is excellent but locks you into Anthropic's
ecosystem. Mistral's Devstral 2 family is open-weight (modified MIT / Apache
2.0), substantially cheaper per token, and can be run locally. This fork keeps
the same UX while swapping the engine.

## License

This repository is licensed under the Apache License 2.0 – the same license
that Mistral Vibe CLI uses. See `LICENSE` for details.
