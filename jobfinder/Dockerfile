FROM python:3.11.7

WORKDIR /app

# Requirements
COPY requirements.txt ./

RUN apt-get update && apt-get -y install cron vim \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2-binary 

RUN pip3 install --no-cache-dir -r requirements.txt


# Copy cron file to the cron.d directory
COPY ./orchestration/crontab_scrapy /etc/cron.d/crontab_scrapy

# Source code into the container.
COPY . .

# Execution rights on the cron job and script
RUN chmod 0644 /etc/cron.d/crontab_scrapy
RUN chmod +x /app/run_scrapy.sh
RUN crontab /etc/cron.d/crontab_scrapy


#CMD ["cron", "-f"]

CMD cd /app && sh /app/run_scrapy.sh > /proc/1/fd/1 2>/proc/1/fd/2 && cron -f 