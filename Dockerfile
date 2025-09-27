FROM python:3.13.2
WORKDIR /usr/telegram-warden/
COPY ./ ./
RUN pip install -r requirements.txt
CMD ["python3", "main.py"]