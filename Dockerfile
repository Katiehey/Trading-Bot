# Stage 1: builder
FROM python:3.12-slim AS builder

WORKDIR /app

# Force apt to run noninteractive 
ENV DEBIAN_FRONTEND=noninteractive

# Install build tools only in builder stage
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install using prebuilt wheels when possible
COPY requirements.txt .
RUN pip install --no-cache-dir --prefer-binary --prefix=/install -r requirements.txt \
    && rm -rf /root/.cache/pip

# Stage 2: runtime
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy source code
COPY . .

# Non-root user setup (create before chown)
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID trader && \
    useradd -m -u $UID -g $GID trader

# Create runtime directories and clean up pyc/test files
RUN mkdir -p /app/logs /app/runtime /app/backups && \
    chown -R trader:trader /app/logs /app/runtime && \
    chmod +x /app/docker/healthcheck.sh && \
    find /usr/local/lib/python3.12 -name '*.pyc' -delete && \
    rm -rf /usr/local/lib/python3.12/site-packages/numpy/tests \
           /usr/local/lib/python3.12/site-packages/scipy/tests \
           /usr/local/lib/python3.12/site-packages/pandas/tests

# Switch to non-root user
USER trader

# Environment hygiene
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY docker/healthcheck.sh /app/docker/healthcheck.sh
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD /app/docker/healthcheck.sh

# Entrypoint
CMD ["python", "-m", "src.live.live_paper_trader"]
