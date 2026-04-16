FROM python:3.11-slim AS builder

# Install Node.js for frontend build
RUN apt-get update \
  && apt-get install -y --no-install-recommends curl ca-certificates \
  && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
  && apt-get install -y --no-install-recommends nodejs \
  && rm -rf /var/lib/apt/lists/*

# Copy uv
COPY --from=ghcr.io/astral-sh/uv:0.9.26 /uv /uvx /bin/

WORKDIR /app

# Install Python dependencies
COPY backend/pyproject.toml backend/uv.lock ./backend/
RUN cd backend && uv sync --frozen --no-dev

# Install Node dependencies and build frontend
COPY package.json package-lock.json ./
COPY frontend/package.json frontend/package-lock.json ./frontend/
RUN npm ci && npm ci --prefix frontend

COPY . .
RUN npm run build --prefix frontend

# ─── Runtime stage ────────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

# Install gunicorn
RUN pip install --no-cache-dir gunicorn

# Create non-root user
RUN useradd -m -u 1000 endora

WORKDIR /app

# Copy Python venv and source
COPY --from=builder /app/backend /app/backend
COPY --from=builder /app/.venv /app/.venv 2>/dev/null || true

# Copy built frontend (served as static files or by nginx)
COPY --from=builder /app/frontend/dist /app/frontend/dist

# Set ownership
RUN chown -R endora:endora /app

USER endora

EXPOSE 5001

ENV PATH="/app/backend/.venv/bin:$PATH"

# Run production WSGI server
CMD ["sh", "-c", "cd /app/backend && /app/backend/.venv/bin/gunicorn --workers=4 --bind=0.0.0.0:5001 --timeout=120 'app:create_app()'"]
