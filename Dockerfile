FROM python:3.5-alpine

WORKDIR /jiban_bot_root

ENV TZ 'Asias/Tehran'
RUN apk update && apk add tzdata  libffi-dev libpq postgresql-dev build-base jpeg-dev&& \
    pip install --upgrade pip && \
    cp /usr/share/zoneinfo/Asia/Tehran /etc/localtime && \
    echo $TZ > /etc/timezone

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

RUN cp /usr/share/zoneinfo/Asia/Tehran /etc/localtime && \
    echo $TZ > /etc/timezone


COPY ./ ./
CMD ["python", "starter.py"]
ENV PYTHONPATH /jiban_bot_root
