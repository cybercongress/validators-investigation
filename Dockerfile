FROM python:3.6 

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1
WORKDIR /  

COPY requirements.scraper.txt ./
RUN pip install -r requirements.scraper.txt

COPY parallel_scraper.py ./
COPY config.py ./

CMD celery -A parallel_scraper purge -f && \ 
    python ./parallel_scraper.py && \
    celery -A parallel_scraper worker