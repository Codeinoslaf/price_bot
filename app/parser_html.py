from curl_cffi import requests
from bs4 import BeautifulSoup
from pathlib import Path
from dotenv import load_dotenv

import re
import os

load_dotenv()

CA_FILE = Path(os.getenv("CA_FILE", "cacert.pem"))
POOL_URL = os.getenv("POOL_URL")


def get_mcap_number() -> float | None:
    if not CA_FILE.is_file():
        print(f"[!] Не найден файл: {CA_FILE}")
        return None

    try:
        response = requests.get(
            POOL_URL,
            impersonate="chrome124",
            verify=str(CA_FILE),
            timeout=12
        )

        if response.status_code != 200:
            print(f"[!] HTTP {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        for span in soup.find_all("span", class_="body-2 text-secondary"):
            if span.get_text(strip=True) == "MCAP":
                prev = span.find_previous("span")
                if prev and "тыс." in prev.get_text():
                    text = prev.get_text(strip=True)
                    match = re.search(r'([\d\s,]+)', text)
                    if match:
                        val = match.group(1).replace(" ", "").replace(",", ".")
                        return float(val)

        print("[!] MCAP не найден в HTML")
        return None

    except Exception as e:
        print(f"[!] Ошибка парсинга: {e}")
        return None


if __name__ == "__main__":
    print("Тест MCAP:", get_mcap_number())
