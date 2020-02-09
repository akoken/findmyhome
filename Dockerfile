FROM python:3.4-alpine

ENV SLACK_WEBHOOK_URL <slack webhook url>
ENV SEARCH_URL <search url>

WORKDIR /app

ADD /src /app

RUN pip3 install -r requirements.txt

ENTRYPOINT python app.py