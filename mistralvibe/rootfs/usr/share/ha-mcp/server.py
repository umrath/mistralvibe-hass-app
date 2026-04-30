import os
import json
import httpx
from typing import Optional
from fastmcp import FastMCP

HA_URL = os.environ.get("HA_URL", "http://supervisor/core")
HA_TOKEN = os.environ.get("HA_TOKEN", "")

mcp = FastMCP("home-assistant")

def _headers() -> dict:
    return {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }

def _get(path: str) -> dict | list:
    with httpx.Client(timeout=10) as client:
        r = client.get(f"{HA_URL}/api{path}", headers=_headers())
        r.raise_for_status()
        return r.json()

def _post(path: str, data: dict) -> dict:
    with httpx.Client(timeout=10) as client:
        r = client.post(f"{HA_URL}/api{path}", headers=_headers(), json=data)
        r.raise_for_status()
        return r.json()

@mcp.tool
def ha_get_config() -> dict:
    """Get Home Assistant core configuration (version, location, units)."""
    return _get("/config")

@mcp.tool
def ha_list_entities(domain: Optional[str] = None, search: Optional[str] = None, limit: int = 50) -> list:
    """List entities, optionally filtered by domain (light, switch, sensor, etc.) or search term. Max 50 by default."""
    states = _get("/states")
    if domain:
        states = [s for s in states if s["entity_id"].startswith(f"{domain}.")]
    if search:
        search_lower = search.lower()
        states = [s for s in states if search_lower in s["entity_id"].lower()
                  or search_lower in str(s.get("attributes", {}).get("friendly_name", "")).lower()]
    states = states[:limit]
    return [{"entity_id": s["entity_id"],
             "state": s["state"],
             "friendly_name": s.get("attributes", {}).get("friendly_name", "")}
            for s in states]

@mcp.tool
def ha_get_entity(entity_id: str) -> dict:
    """Get the full state and attributes of a specific entity."""
    return _get(f"/states/{entity_id}")

@mcp.tool
def ha_call_service(domain: str, service: str, data: Optional[dict] = None) -> str:
    """Call a Home Assistant service. Examples: domain='light', service='turn_on', data={'entity_id': 'light.kitchen'}"""
    _post(f"/services/{domain}/{service}", data or {})
    return f"Service {domain}.{service} called successfully."

@mcp.tool
def ha_list_automations(search: Optional[str] = None, limit: int = 50) -> list:
    """List automations, optionally filtered by name. Max 50 by default."""
    states = _get("/states")
    automations = [s for s in states if s["entity_id"].startswith("automation.")]
    if search:
        search_lower = search.lower()
        automations = [a for a in automations
                       if search_lower in a["entity_id"].lower()
                       or search_lower in str(a.get("attributes", {}).get("friendly_name", "")).lower()]
    automations = automations[:limit]
    return [{"entity_id": a["entity_id"],
             "state": a["state"],
             "friendly_name": a.get("attributes", {}).get("friendly_name", "")}
            for a in automations]

@mcp.tool
def ha_list_areas() -> list:
    """List all areas defined in Home Assistant."""
    try:
        result = _post("/template", {"template": "{{ areas() | tojson }}"})
        if isinstance(result, str):
            return json.loads(result)
        return result
    except Exception:
        return []

@mcp.tool
def ha_get_error_log(lines: int = 50) -> str:
    """Get the last N lines of the Home Assistant error log. Default 50, maximum 200 lines."""
    lines = min(lines, 200)
    with httpx.Client(timeout=15) as client:
        r = client.get(f"{HA_URL}/api/error_log", headers=_headers())
        r.raise_for_status()
        log_lines = r.text.splitlines()
        return "\n".join(log_lines[-lines:])

@mcp.tool
def ha_get_history(entity_id: str, hours: int = 2) -> list:
    """Get state history for an entity for the last N hours. Default 2 hours, maximum 24."""
    hours = min(hours, 24)
    from datetime import datetime, timedelta, timezone
    start = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
    result = _get(f"/history/period/{start}?filter_entity_id={entity_id}&minimal_response=true")
    if result and isinstance(result, list) and result[0]:
        return result[0][-50:]
    return []

@mcp.tool
def ha_restart() -> str:
    """Restart Home Assistant. Use only when necessary."""
    with httpx.Client(timeout=10) as client:
        r = client.post(f"{HA_URL}/api/services/homeassistant/restart", headers=_headers(), json={})
        r.raise_for_status()
    return "Home Assistant restart initiated."

@mcp.tool
def ha_get_vibe_usage() -> dict:
    """Get accumulated token usage and estimated costs from all Vibe sessions stored in /data/vibe/logs/session/."""
    import pathlib as _pathlib

    try:
        import tomllib
    except ImportError:
        import tomli as tomllib

    config_path = _pathlib.Path("/data/vibe/config.toml")
    prices = {}
    if config_path.exists():
        try:
            cfg = tomllib.loads(config_path.read_text())
            for m in cfg.get("models", []):
                name = m.get("name", "")
                alias = m.get("alias", name)
                price_in = m.get("input_price", 0.4)
                price_out = m.get("output_price", 2.0)
                prices[name] = (price_in, price_out)
                prices[alias] = (price_in, price_out)
        except Exception:
            pass

    logs_dir = _pathlib.Path("/data/vibe/logs/session")
    if not logs_dir.exists():
        return {"error": "No session logs found", "sessions": []}

    total_input = total_output = total_cost = 0
    sessions = []

    for session_dir in sorted(logs_dir.iterdir()):
        if not session_dir.is_dir():
            continue
        for f in session_dir.glob("*.json"):
            try:
                data = json.loads(f.read_text())
                usage = data.get("usage", {})
                inp = usage.get("prompt_tokens", 0)
                out = usage.get("completion_tokens", 0)
                model = data.get("model", "unknown")
                price_in, price_out = prices.get(model, (0.4, 2.0))
                cost = (inp * price_in + out * price_out) / 1_000_000
                sessions.append({"session": session_dir.name, "model": model, "input_tokens": inp, "output_tokens": out, "cost_usd": round(cost, 6)})
                total_input += inp
                total_output += out
                total_cost += cost
            except Exception:
                continue

    return {
        "sessions": sessions,
        "total_input_tokens": total_input,
        "total_output_tokens": total_output,
        "total_cost_usd": round(total_cost, 6),
        "note": "Estimates based on prices in /data/vibe/config.toml. For exact billing see console.mistral.ai"
    }

if __name__ == "__main__":
    mcp.run()
