# ── Frontend Dockerfile ──────────────────────────────────────────
FROM node:22-alpine

WORKDIR /app

# Install dependencies first (better caching)
COPY package.json package-lock.json ./
RUN npm ci

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Run dev server (use `npm run build && npm run start` for production)
CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0", "--port", "3000"]
