FROM python:3

WORKDIR /src

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y cron
RUN crontab crontab.txt

RUN ["chmod", "+x", "/src/entrypoint.sh"]

CMD ["/src/entrypoint.sh"]