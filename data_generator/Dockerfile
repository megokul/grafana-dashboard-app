FROM python:3.11-slim

WORKDIR /app

# Use the repository root as build context so we can copy requirements and app/sql
# (docker-compose will set the build context to project root)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application and SQL assets
COPY data_generator/app /app/app
COPY sql /app/sql

# default envs (overridden by compose/.env)
ENV DB_HOST=postgres \
    DB_PORT=5432 \
    DB_NAME=postgres \
    DB_USER=postgres \
    DB_PASSWORD=postgres \
    BATCH_SIZE=10 \
    SLEEP_SECONDS=15

# Run the generator module
CMD ["python", "-m", "app.main"]
