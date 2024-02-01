FROM python:3.9.17-slim
WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .
EXPOSE 8001

CMD ["gunicorn", "-b", "0.0.0.0:8001", "wsgi:app"]
