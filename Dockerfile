# Use Python 3.11 slim image
FROM python:3.11-slim

# Install system dependencies for Playwright Chromium
# Install manually instead of using playwright install-deps due to Debian Trixie compatibility
RUN apt-get update && apt-get install -y \
    # Core dependencies
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libatspi2.0-0 \
    libxshmfence1 \
    # Additional dependencies
    fonts-liberation \
    libwayland-client0 \
    xdg-utils \
    wget \
    ca-certificates \
    # GTK and display
    libgtk-3-0 \
    # Cleanup
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright Chromium browser only (skip install-deps)
RUN python -m playwright install chromium

# Copy application code
COPY . .

# Run the bot
CMD ["python", "bot.py"]
