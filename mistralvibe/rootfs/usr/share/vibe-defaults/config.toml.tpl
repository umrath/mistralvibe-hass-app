active_model = "devstral-small-2"
vim_keybindings = false
textual_theme = "textual-dark"
auto_compact_threshold = 100000
context_warnings = true
include_model_info = true
include_project_context = true
enable_update_checks = true
enable_telemetry = false
api_timeout = 720.0
disable_welcome_banner_animation = true
system_prompt_id = "ha"

[project_context]
max_chars = 60000
default_commit_count = 5

[session_logging]
save_dir = "/data/vibe/logs/session"
enabled = true

[tools]
tool_paths = []
enabled_tools = []
disabled_tools = []

[[providers]]
name = "mistral"
api_base = "https://api.mistral.ai/v1"
api_key_env_var = "MISTRAL_API_KEY"
backend = "mistral"

[[models]]
name = "__DEVSTRAL_SMALL__"
provider = "mistral"
alias = "devstral-small-2"
input_price = 0.1
output_price = 0.3

[[models]]
name = "__DEVSTRAL__"
provider = "mistral"
alias = "devstral-2"
input_price = 0.4
output_price = 2.0

[[models]]
name = "__MAGISTRAL__"
provider = "mistral"
alias = "magistral-medium"
input_price = 2.0
output_price = 5.0

[[mcp_servers]]
name = "hass"
transport = "stdio"
command = "python3"
args = ["/usr/share/ha-mcp/server.py"]
startup_timeout_sec = 30

[mcp_servers.env]
HA_URL = "__HA_URL__"
HA_TOKEN = "__HA_TOKEN__"
