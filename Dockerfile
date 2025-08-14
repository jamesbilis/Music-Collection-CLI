FROM python:3.12-slim

# Create app and data dirs
WORKDIR /data
RUN mkdir -p /app

# Copy application
COPY music_app.py /app/music_app.py

# Default command runs the interactive CLI; DB will be created in /data
CMD ["python", "/app/music_app.py"]
