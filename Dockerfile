# FastMCP Endpoint Toolsets — one server, one port, many scoped MCP endpoints.
FROM python:3.11-slim

WORKDIR /app

# Install dependencies first for better layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app.
COPY . .

# One exposed port for every scoped endpoint.
EXPOSE 8001

# Inside a container we must bind 0.0.0.0, not 127.0.0.1.
CMD ["python", "server.py", "--host", "0.0.0.0", "--port", "8001"]

# Liveness via the built-in /health route (no curl needed in slim image).
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8001/health').status==200 else 1)"
