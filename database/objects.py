from loguru import logger
from pymongo import MongoClient

logger.add(
    "logs/errors.log",
    level="INFO",
    format="{time} - {message}",
)


class DataBase:
    def __init__(self, connection_string, db_name):
        self._cluster = MongoClient(connection_string)
        self._db = self._cluster[db_name]
        self._users_grades = self._db["grades"]
        self._users = self._db["users"]
        self._links = self._db["links"]
        self._db_name = db_name
        print("База данных создана.")

    def add_new_user(self, user_id):
        try:
            if self._users.count_documents({"user_id": user_id}) == 0:
                self._users.insert_one({"user_id": user_id})
                return True
            return False
        except Exception as exc:
            logger.error(exc)
            return False

    def add_new_grade(self, user_id, username, grade, tg_link):
        try:
            if (
                self._users_grades.count_documents(
                    {"tg_link": tg_link, "user_id": user_id}
                )
                == 0
            ):
                self._users_grades.insert_one(
                    {
                        "user_id": user_id,
                        "username": username,
                        "grade": grade,
                        "tg_link": tg_link,
                    }
                )
                return True
            return False
        except Exception as exc:
            logger.error(exc)
            return False

    def get_all_grades_data(self):
        try:
            return list(self._users_grades.find())
        except Exception as exc:
            logger.error(exc)

    def get_all_users_data(self):
        try:
            return list(self._users.find())
        except Exception as exc:
            logger.error(exc)

    def add_new_links(self, links):
        try:
            added_links = []
            for link in links:
                if self._links.count_documents({"tg_link": link}) == 0:
                    self._links.insert_one({"tg_link": link})
                    added_links.append(link)
            return added_links
        except Exception as exc:
            logger.error(exc)
            return []
