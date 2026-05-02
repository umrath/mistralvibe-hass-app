ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM ${BUILD_FROM}

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_INSTALL_DIR=/opt/uv-python \
    UV_TOOL_DIR=/opt/uv-tools \
    UV_TOOL_BIN_DIR=/usr/local/bin \
    VIBE_HOME=/data/vibe \
    PATH=/usr/local/bin:/usr/bin:/bin:/sbin

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]

# ---- system packages -------------------------------------------------------
# python3 is kept only as a scripting helper for the init script (small TOML
# patches). The actual CLIs (mistral-vibe, hass-mcp) run under a uv-managed
# Python 3.13 that we install in the next layer.
RUN apk add --no-cache \
        bash \
        ca-certificates \
        coreutils \
        curl \
        git \
        jq \
        nano \
        ncurses \
        openssh-client \
        py3-pip \
        python3 \
        ripgrep \
        tmux \
        ttyd \
        tzdata \
    && rm -rf /var/cache/apk/*

# ---- uv + managed Python + CLIs --------------------------------------------
RUN curl -LsSf https://astral.sh/uv/install.sh \
      | env UV_INSTALL_DIR=/usr/local/bin sh \
 && uv python install 3.13 \
 && UV_INDEX_STRATEGY=unsafe-best-match \
    uv tool install --python 3.13 \
    --index https://pypi.org/simple \
    mistral-vibe \
 && python3 -m pip install --break-system-packages --no-cache-dir fastmcp httpx \
 && rm -rf /root/.cache /tmp/*


ARG BUILD_ARCH=amd64
RUN case "${BUILD_ARCH}" in \
        amd64)   HA_ARCH="amd64" ;; \
        aarch64) HA_ARCH="aarch64" ;; \
        *)       HA_ARCH="amd64" ;; \
    esac && \
    curl -fsSL "https://github.com/home-assistant/cli/releases/latest/download/ha_${HA_ARCH}" \
        -o /usr/local/bin/ha && \
    chmod +x /usr/local/bin/ha

# ---- add-on rootfs ---------------------------------------------------------
COPY rootfs/ /

RUN chmod a+x \
        /usr/bin/vibe-launcher \
        /etc/cont-init.d/10-init-vibe.sh \
        /etc/services.d/vibe-terminal/run \
        /etc/services.d/vibe-terminal/finish

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -sf http://localhost:7681/ || exit 1

LABEL \
    io.hass.name="Mistral Vibe" \
    io.hass.description="Run Mistral Vibe CLI directly inside Home Assistant" \
    io.hass.type="app" \
    io.hass.version="1.7.9" \
    maintainer="umrath <thoralf@umrath.net>"
