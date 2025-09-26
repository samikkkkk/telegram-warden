FROM python:3.13.2-slim

WORKDIR /usr/telegram-warden/

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /usr/telegram-warden/
USER botuser

CMD ["python3", "main.py"]