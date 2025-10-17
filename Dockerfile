# Simple production image
FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default: stdio server (works when launched by an Apps runtime that binds stdio)
CMD ["python", "server.py"]
