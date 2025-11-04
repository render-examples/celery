FROM python:3.12-slim

# 1. Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 2. Copy and install Python dependencies
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 3. (Multi-steps) Install and immediately uninstall the spaCy model
RUN python -m spacy download fr_core_news_sm

# 4. Copy the rest of your application code
COPY . /app

# 5. Optional CMD
# CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]