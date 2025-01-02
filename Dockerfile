FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

RUN apt-get update && apt-get install -y build-essential libpq-dev

RUN pip install --upgrade pip


EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]