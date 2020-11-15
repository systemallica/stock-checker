import logging
import os

import requests
import yagmail
from bs4 import BeautifulSoup

from utils.stores import stores

logger = logging.getLogger()


def check_store_stock():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/80.0"
    }

    for store in stores:
        url = store.get("url")
        body = requests.get(url, headers=headers).content
        page_text = BeautifulSoup(body, "html.parser").text.lower()
        query_text = store.get("text").lower()
        if query_text in page_text:
            logger.info(f"PS5 NOT in stock at {store['name']}")
        else:
            logger.info(f"PS5 in stock at {store['name']}")
            send_email(store)


def send_email(store):
    PASSWORD = os.environ.get("PASSWORD")
    SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
    RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")
    if not PASSWORD or not SENDER_EMAIL or not RECEIVER_EMAIL:
        logger.error("Env variables must be set")
        raise NotImplementedError

    yag = yagmail.SMTP(user=SENDER_EMAIL, password=PASSWORD)
    yag.send(
        to=RECEIVER_EMAIL,
        subject=f"PS5 in stock at {store['name']}",
        contents=f"Hello, {store['name']} has PS5 in stock. Check it out: {store['url']}",
    )
