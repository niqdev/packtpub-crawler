FROM python:2.7

WORKDIR /packtpub-crawler

COPY script script
COPY config config
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "/packtpub-crawler/script/scheduler.py"]
