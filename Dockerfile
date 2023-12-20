FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY gd_traffic_proxy/ /app/gd_traffic_proxy/

CMD ["python", "/app/gd_traffic_proxy/main.py"]
