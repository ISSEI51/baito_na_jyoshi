from logging import getLogger, FileHandler, DEBUG, INFO, WARNING, ERROR, CRITICAL
from logging import Formatter
import time
from datetime import datetime, timedelta
import sys

from bs4 import BeautifulSoup
import requests


def ip_check():
    url = "https://houjin-biz.com/ipinfo.php"
    with requests.get(url, timeout=5) as response:
        response.raise_for_status()
        data = response.json()
    ip_address = data.get("ip")
    print(ip_address)
    if ip_address == "36.3.117.80":
        sys.exit()


def access_url(url, filename="", defname=""):
    if not hasattr(access_url, "last_check_time"):
        access_url.last_check_time = datetime.min

    current_time = datetime.now()
    if current_time - access_url.last_check_time > timedelta(minutes=10):
        access_url.last_check_time = current_time
        ip_check()

    logger = getLogger(__name__)
    if not logger.hasHandlers():
        formatter = Formatter("[%(levelname)s]%(asctime)s-%(message)s (%(filename)s)")
        error_handler = FileHandler("error.txt", encoding="utf-8")
        error_handler.setLevel(ERROR)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)

    max_retries = 3
    wait_time = 3
    attempt = 0
    while attempt < max_retries:
        try:
            with requests.get(url, timeout=30) as response:
                response.raise_for_status()
                return BeautifulSoup(response.text, "lxml")

        except Exception as e:
            attempt += 1
            """logger.error(
                f"{url}: {e} (リトライ{attempt}回目, ファイル: {filename}, 関数名: {defname})"
            )"""
            if attempt < max_retries:
                time.sleep(wait_time)
            else:
                logger.error(f"{url}: {e}")
                return None
