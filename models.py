import dns.resolver

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ["8.8.8.8"]

from configuration.config import DB_URI
from database.objects import DataBase

from typing import List

import requests
import validators
from bs4 import BeautifulSoup

mongodb = DataBase(connection_string=DB_URI, db_name="blacklist_bot")


def get_vklader_links() -> List[str]:
    req = requests.get("https://vklader.com/blacklist-telegram/", timeout=5).text
    soup = BeautifulSoup(req, "html.parser")
    return get_telegram_links(
        [row for row in str(soup.find_all("p")).split(" ") if "t.me/" in row]
    )


def get_telltrue_links() -> List[str]:
    requests.get("https://telltrue.net/", timeout=5)
    req = requests.get("https://telltrue.net/blacklist-telegram/", timeout=5).text
    soup = BeautifulSoup(req, "html.parser")
    return get_telegram_links(
        [
            row
            for row in str(soup.find_all("div", class_="blacklist-row")).split(" ")
            if "t.me/" in row
        ]
    )


def get_telegram_links(blacklist_rows: List[str]) -> List[str]:
    telegram_links = []
    for row in blacklist_rows:
        for special_symbol in [
            "https://",
            ",",
            ".",
            "(",
            ")",
            "tme/",
            ":",
            "</p>",
            ";",
        ]:
            row = row.replace(special_symbol, "")
        row = f"t.me/{row}"
        if validators.url(f"https://{row}"):
            telegram_links.append(row)
    return telegram_links


def check_new_links(tg_links: List[str]) -> List[str]:
    return mongodb.add_new_links(tg_links)


def add_new_user(user_id: int) -> bool:
    return mongodb.add_new_user(str(user_id))


def add_new_grade(information) -> str:
    user_id = information.from_user.id
    username = information.from_user.username
    answer = str(information.data).split(":")
    grade, tg_link = answer[1], answer[2]
    new_grade = mongodb.add_new_grade(user_id, username, grade, tg_link)
    if new_grade:
        return "🟢 Вы успешно оценили телеграм канал."
    return "🟠 Вы ранее оценивали данный телеграм канал."


def get_users() -> List[int]:
    return [user["user_id"] for user in mongodb.get_all_users_data()]


def get_grades() -> List[dict]:
    return mongodb.get_all_grades_data()
