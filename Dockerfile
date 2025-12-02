FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "doc_qa.wsgi:application", "--bind", "0.0.0.0:8000"]
