import logging
import os
import re
from datetime import date, timedelta

import requests
from bs4 import BeautifulSoup
from imap_tools import MailBox, AND
from urlextract import URLExtract

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def get_aurora_forecast():
    raw_data = requests.get('https://services.swpc.noaa.gov/text/3-day-forecast.txt').content.decode('utf-8')
    kp_lines = re.findall("^.*[0-9]{2}-[0-9]{2}UT.*$", raw_data, re.MULTILINE)

    kp_days = [
        date.today().strftime("%d/%m") + ': ',
        (date.today() + timedelta(days=1)).strftime("%d/%m") + ': ',
        (date.today() + timedelta(days=2)).strftime("%d/%m") + ': ']

    for kp_line in kp_lines:
        kp_numbers = re.findall(' [1-9] ', kp_line)
        kp_days[0] += kp_numbers[0].strip()
        kp_days[1] += kp_numbers[1].strip()
        kp_days[2] += kp_numbers[2].strip()

    logging.info(kp_days)
    return "Kp for 3hr blocks UTC time.\n" + "\n".join(kp_days)


def get_map_share_url(text):
    urls = URLExtract().find_urls(text)

    for url in urls:
        if re.search("txtmsg", url):
            logging.info('sending via ' + url)
            return url


def notify_map_share(garmin_url):
    soup = BeautifulSoup(requests.get(garmin_url).content, 'html.parser')
    message_id = soup.find("input", {"id": "MessageId"}).get('value')
    guid = soup.find("input", {"id": "Guid"}).get('value')
    reply_address = soup.find("input", {"id": "ReplyAddress"}).get('value')

    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {'ReplyAddress': reply_address,
               'ReplyMessage': get_aurora_forecast(),
               'MessageId': message_id,
               'Guid': guid}

    logging.info(payload)

    session = requests.Session()
    response = session.post(
        'https://eur.explore.garmin.com/TextMessage/TxtMsg',
        headers=headers,
        data=payload)

    logging.info(response.headers)
    logging.info(response.text)


with MailBox(os.environ['IMAP_URL']).login(os.environ['IMAP_LOGIN'], os.environ['IMAP_PASSWORD'], 'INBOX') as mailbox:
    for msg in mailbox.fetch(AND(from_=os.environ['IMAP_FROM'], new=True)):
        map_share_url = get_map_share_url(msg.text)
        notify_map_share(map_share_url)
