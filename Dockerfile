FROM python:3.11-slim

WORKDIR /app
COPY alert_relay.py .

RUN pip install Flask requests

CMD ["python", "alert_relay.py"]
