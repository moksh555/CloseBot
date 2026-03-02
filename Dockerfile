# STAGE 1: Build environment
FROM python:3.10-slim AS builder

RUN apt-get update && apt-get install -y curl tar git

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install GitHub CLI
RUN curl -fsSL https://github.com/cli/cli/releases/download/v2.45.0/gh_2.45.0_linux_amd64.tar.gz -o gh.tar.gz \
    && tar -xf gh.tar.gz \
    && mv gh_2.45.0_linux_amd64/bin/gh /usr/local/bin/gh

WORKDIR /app

COPY uv.lock pyproject.toml ./
RUN uv sync --frozen --no-install-project --no-dev

COPY . .
RUN rm -rf .venv && uv sync --frozen --no-dev

# MANUAL EXTENSION INSTALL (Bypasses 'gh auth' check)
RUN mkdir -p /root/.local/share/gh/extensions/gh-copilot && \
    git clone https://github.com/github/gh-copilot /root/.local/share/gh/extensions/gh-copilot

# Stage 2: Final Runtime Image
FROM python:3.10-slim
WORKDIR /app

RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /usr/local/bin/gh /usr/local/bin/gh
COPY --from=builder /root/.local/share/gh /root/.local/share/gh
COPY --from=builder /app /app

# Ensure these point to the right places
ENV GH_CONFIG_DIR=/root/.config/gh
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8080

# RUNTIME: Create the config file using the token from ECS environment variables
CMD ["sh", "-c", "mkdir -p /root/.config/gh && printf 'github.com:\n    oauth_token: %s\n    git_protocol: https\n' \"$GH_TOKEN\" > /root/.config/gh/hosts.yml && uvicorn main:app --host 0.0.0.0 --port 8080"]