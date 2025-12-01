# Build stage: Node dependencies
FROM node:18-alpine AS node-builder
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install --production

# Final stage: Python + Node runtime
FROM python:3.11-slim
WORKDIR /app

# Install Node runtime (lightweight)
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy Node modules from builder
COPY --from=node-builder /app/node_modules ./node_modules
COPY package.json ./

# Copy application code
COPY app/ ./app/
COPY src/ ./src/
COPY demo/ ./demo/

EXPOSE 3000
ENV PORT=3000
CMD ["node", "src/server.js"]
