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

# ---- add-on rootfs ---------------------------------------------------------
COPY rootfs/ /

RUN chmod a+x \
        /usr/bin/vibe-launcher \
        /etc/cont-init.d/10-init-vibe.sh \
        /etc/services.d/vibe-terminal/run \
        /etc/services.d/vibe-terminal/finish

LABEL \
    io.hass.name="Mistral Vibe" \
    io.hass.description="Run Mistral Vibe CLI directly inside Home Assistant" \
    io.hass.type="addon" \
    io.hass.version="1.4.8" \
    maintainer="umrath <thoralf@umrath.net>"
