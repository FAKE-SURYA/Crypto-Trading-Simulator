# Multi-stage Dockerfile for Python backend with C++ module
# Stage 1: Build C++ module
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /build

# Copy C++ core source
COPY cpp_core/ ./cpp_core/

# Install Python build dependencies
RUN pip install --no-cache-dir scikit-build cmake pybind11

# Build C++ module
WORKDIR /build/cpp_core
RUN pip install .

# Stage 2: Runtime
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python dependencies file
COPY backend/requirements.txt ./backend/

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy compiled C++ module from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages/trade_engine* /usr/local/lib/python3.11/site-packages/

# Copy backend code
COPY backend/ ./backend/

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
