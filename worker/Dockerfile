FROM python:3.9-slim

WORKDIR /app

# Αντιγράφουμε μόνο τον κώδικα
COPY worker.py .

# Εγκαθιστούμε τις βιβλιοθήκες ΑΠΕΥΘΕΙΑΣ (χωρίς requirements.txt)
RUN pip install pika minio

# Περιμένουμε λίγο και ξεκινάμε
CMD ["sh", "-c", "sleep 20 && python -u worker.py"]