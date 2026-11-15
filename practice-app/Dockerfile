# The Bookshelf Practice App. Built and started by docker compose (see docker-compose.yml).
# The base image is pinned to an exact version and digest, and every Python package
# is checked against its SHA-256 hash, so the build never changes by surprise.
FROM python:3.13.18-slim-bookworm@sha256:a5a7017efc5969e00ae2b91c8eb0631049a569652aa4ffc4501769049ae45c72

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --require-hashes --no-deps -r requirements.txt

# Run as a normal user, never as root.
RUN useradd --create-home --uid 10001 bookshelf \
    && mkdir -p /app/data \
    && chown bookshelf:bookshelf /app/data
COPY --chown=bookshelf:bookshelf bookshelf ./bookshelf
USER bookshelf

EXPOSE 8080
CMD ["python", "-m", "bookshelf"]
