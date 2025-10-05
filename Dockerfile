# UML-MCP Dockerfile - Uses UV package manager
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies for diagram tools and UV
RUN apt-get update && apt-get install -y \
    graphviz \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install UV package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy project files
COPY pyproject.toml ./
COPY . .

# Install dependencies using UV
RUN uv pip install --system -e .

# Create output directory
RUN mkdir -p /app/output

# Expose port for API
EXPOSE 8000

# Set entrypoint for stdio mode
ENTRYPOINT ["python", "mcp_server.py", "--transport", "stdio"]