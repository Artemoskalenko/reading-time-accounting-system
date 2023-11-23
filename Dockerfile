FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

RUN apt-get update -y

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

CMD ["./run.sh"]
