FROM python:2.7
ADD requirements.txt /app/requirements.txt
ADD ./test_celery/ /app/
WORKDIR /app/
RUN pip install -r requirements.txt
ENV C_FORCE_ROOT=1
ENTRYPOINT celery -A test_celery worker --concurrency=20 --loglevel=info
#RUN celery -A test_celery worker --concurrency=20 --loglevel=info
#ENTRYPOINT ["celery", "-A", "test_celery", "worker","--concurrency","20","--loglevel","info"]