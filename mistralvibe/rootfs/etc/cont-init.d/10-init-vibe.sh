#!/usr/bin/with-contenv bashio
set -e

VIBE_HOME="/data/vibe"
ENV_FILE="${VIBE_HOME}/.env"
CONFIG_FILE="${VIBE_HOME}/config.toml"
TRUST_FILE="${VIBE_HOME}/trusted_folders.toml"
LOG_DIR="${VIBE_HOME}/logs/session"

mkdir -p "${VIBE_HOME}/agents" "${VIBE_HOME}/prompts" "${LOG_DIR}"

MISTRAL_API_KEY="$(bashio::config 'mistral_api_key')"
ACTIVE_MODEL="$(bashio::config 'active_model')"
DEFAULT_AGENT="$(bashio::config 'default_agent')"
AUTO_APPROVE="$(bashio::config 'auto_approve')"
AUTO_UPDATE_CLI="$(bashio::config 'auto_update_cli')"
ENABLE_TELEMETRY="$(bashio::config 'enable_telemetry')"

if [ -z "${MISTRAL_API_KEY}" ] || [ "${MISTRAL_API_KEY}" = "null" ]; then
    bashio::log.fatal "No 'mistral_api_key' configured."
    exit 1
fi

cat > "${ENV_FILE}" <<EOF
MISTRAL_API_KEY=${MISTRAL_API_KEY}
HA_URL=http://supervisor/core
HA_TOKEN=${SUPERVISOR_TOKEN}
EOF
chmod 600 "${ENV_FILE}"

bashio::log.info "Resolving current Mistral model names via API..."
MODELS_JSON="$(curl -sf \
    -H "Authorization: Bearer ${MISTRAL_API_KEY}" \
    "https://api.mistral.ai/v1/models" || echo "")"

resolve_model() {
    local prefix="$1"
    local fallback="$2"
    if [ -n "${MODELS_JSON}" ]; then
        echo "${MODELS_JSON}" \
            | python3 -c "
import sys, json
data = json.load(sys.stdin)
prefix = sys.argv[1]
matches = [m['id'] for m in data.get('data', []) if m['id'].startswith(prefix)]
matches.sort()
print(matches[-1] if matches else sys.argv[2])
" "$prefix" "$fallback" 2>/dev/null || echo "$fallback"
    else
        echo "$fallback"
    fi
}

MODEL_DEVSTRAL_SMALL="$(resolve_model 'devstral-small-2' 'devstral-small-2512')"
MODEL_DEVSTRAL="$(resolve_model 'devstral-2' 'devstral-2512')"
MODEL_MAGISTRAL="$(resolve_model 'magistral-medium' 'magistral-medium-2506')"

bashio::log.info "Models: small=${MODEL_DEVSTRAL_SMALL} large=${MODEL_DEVSTRAL} magistral=${MODEL_MAGISTRAL}"

bashio::log.info "Writing Vibe config to ${CONFIG_FILE}"
sed \
    -e "s|__DEVSTRAL_SMALL__|${MODEL_DEVSTRAL_SMALL}|g" \
    -e "s|__DEVSTRAL__|${MODEL_DEVSTRAL}|g" \
    -e "s|__MAGISTRAL__|${MODEL_MAGISTRAL}|g" \
    /usr/share/vibe-defaults/config.toml.tpl > "${CONFIG_FILE}"

python3 - "$CONFIG_FILE" "$ACTIVE_MODEL" "$AUTO_UPDATE_CLI" "$ENABLE_TELEMETRY" <<'PY'
import sys, re, pathlib
path, model, auto_update, telemetry = sys.argv[1:]
text = pathlib.Path(path).read_text()

def upsert(key, value):
    global text
    pattern = re.compile(rf"^{key}\s*=.*$", re.MULTILINE)
    if pattern.search(text):
        text = pattern.sub(f"{key} = {value}", text)
    else:
        text += f"\n{key} = {value}\n"

upsert("active_model", f'"{model}"')
upsert("enable_update_checks", "true" if auto_update == "true" else "false")
upsert("enable_telemetry", "true" if telemetry == "true" else "false")
pathlib.Path(path).write_text(text)
PY

cat > "${TRUST_FILE}" <<'EOF'
trusted_folders = [
  "/config",
  "/share",
  "/data/vibe",
]
EOF

echo "${AUTO_APPROVE}" > "${VIBE_HOME}/.auto_approve"
echo "${DEFAULT_AGENT}" > "${VIBE_HOME}/.default_agent"

bashio::log.info "Mistral Vibe initialised – model: ${ACTIVE_MODEL}, agent: ${DEFAULT_AGENT}"
