import logging
import os
import re
import requests

from datetime import date, timedelta
from bs4 import BeautifulSoup
from imap_tools import MailBox, AND
from urlextract import URLExtract

logging.basicConfig(stream=sys.stdout, format='%(levelname)s:%(message)s', level=logging.INFO)


def get_aurora_forecast():
    raw_data = requests.get('https://services.swpc.noaa.gov/text/3-day-forecast.txt').content.decode('utf-8')
    kp_lines = re.findall("^.*[0-9]{2}-[0-9]{2}UT.*$", raw_data, re.MULTILINE)

    kp_days = [
        date.today().strftime("%d/%m") + ': ',
        (date.today() + timedelta(days=1)).strftime("%d/%m") + ': ',
        (date.today() + timedelta(days=2)).strftime("%d/%m") + ': ']

    for kp_line in kp_lines:
        logging.info(kp_line)
        kp_numbers = re.findall(' [0-9] ', kp_line)
        kp_days[0] += kp_numbers[0].strip()
        kp_days[1] += kp_numbers[1].strip()
        kp_days[2] += kp_numbers[2].strip()

    logging.info(kp_days)
    return "Kp for 3hr blocks UTC time.\n" + "\n".join(kp_days)


def extract_map_share_url(text):
    urls = URLExtract().find_urls(text)

    for url in urls:
        if re.search("txtmsg", url):
            logging.info('sending via ' + url)
            return url


def create_map_share_payload(url, text):
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    message_id = soup.find("input", {"id": "MessageId"}).get('value')
    guid = soup.find("input", {"id": "Guid"}).get('value')
    reply_address = soup.find("input", {"id": "ReplyAddress"}).get('value')

    return {'ReplyAddress': reply_address,
            'ReplyMessage': text,
            'MessageId': message_id,
            'Guid': guid}


def notify_map_share(url, text):
    payload = create_map_share_payload(url, text)
    logging.info(payload)

    session = requests.Session()
    response = session.post(
        'https://eur.explore.garmin.com/TextMessage/TxtMsg',
        headers={'User-Agent': 'Mozilla/5.0'},
        data=payload)

    logging.info(response.headers)


with MailBox(os.getenv('IMAP_URL')).login(os.getenv('IMAP_LOGIN'), os.getenv('IMAP_PASSWORD'), 'INBOX') as mailbox:
    forecast_text = get_aurora_forecast()

    for msg in mailbox.fetch(AND(from_=os.getenv('IMAP_FROM', 'no.reply.inreach@garmin.com'), new=True)):
        map_share_url = extract_map_share_url(msg.text)
        notify_map_share(map_share_url, forecast_text)
