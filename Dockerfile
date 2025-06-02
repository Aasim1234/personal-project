FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy HTML files
COPY . .

# Use Python's built-in HTTP server to serve the HTML
EXPOSE 8082
CMD ["python", "-m", "http.server", "8080"]
