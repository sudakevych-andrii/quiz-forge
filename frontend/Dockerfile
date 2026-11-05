# ---------- base ----------
FROM node:24-slim AS base

ENV NEXT_TELEMETRY_DISABLED=1

WORKDIR /app
RUN chown node:node /app
USER node

# ---------- dev ----------
FROM base AS dev

COPY --chown=node:node package.json package-lock.json ./
RUN npm ci

COPY --chown=node:node . .
RUN mkdir -p .next

EXPOSE 3000
CMD ["npm", "run", "dev"]
