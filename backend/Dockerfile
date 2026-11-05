# ---------- base ----------
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

ARG UID=1000
ARG GID=1000
RUN groupadd --gid ${GID} app \
 && useradd --uid ${UID} --gid ${GID} --create-home app

# ---------- dev ----------
FROM base AS dev

COPY requirements/ requirements/
RUN pip install -r requirements/dev.txt

COPY --chown=app:app . .

USER app
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
