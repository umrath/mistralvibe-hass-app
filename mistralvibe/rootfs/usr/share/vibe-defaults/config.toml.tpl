active_model = "devstral-small-2"
vim_keybindings = false
textual_theme = "textual-dark"
auto_compact_threshold = 200000
context_warnings = true
include_model_info = true
include_project_context = true
enable_update_checks = true
enable_telemetry = false
api_timeout = 720.0
disable_welcome_banner_animation = true

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

[[mcp_servers]]
name = "hass"
transport = "stdio"
command = "hass-mcp"
args = []
startup_timeout_sec = 30
