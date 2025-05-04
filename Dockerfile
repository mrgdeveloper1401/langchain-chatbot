FROM python:3.12-alpine

WORKDIR /home/app

COPY . .

RUN apk update && \
    apk upgrade && \
    apk add py3-pip && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    adduser -D -H chain && \
    chown -R 755 chain:chain /home/app

USER chain

ENTRYPOINT ["./start.sh"]