FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY gen_session.py ./

COPY keyword_monitor/ ./keyword_monitor

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "keyword_monitor.run"]
