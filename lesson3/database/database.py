import sqlite3

from pathlib import Path
from typing import Optional


class Database:
    """ Класс работы с базой данных. Это MVP только для примера """

    def __init__(self, name):
        self.name = name + ".db"
        self.db_path = Path(__file__).parent.joinpath(self.name)
        self._conn = sqlite3.connect(self.db_path)

    def _query_fetch_one(self, query, param=None):
        with self._conn:
            cursor = self._conn.cursor()
            if param:
                cursor.execute(query, param)
            else:
                cursor.execute(query)
            rows = cursor.fetchone()
            cursor.close()
        return rows

    def get_lang(self, user_id: int) -> Optional[str]:
        select_query = "SELECT lang FROM user WHERE tg_id = {user_id}".format(user_id=user_id)
        record = self._query_fetch_one(select_query)
        return record[0] if record else None

    def set_lang(self, user_id: int, lang: str) ->Optional[tuple]:
        update_query = """UPDATE user SET lang=(?) WHERE tg_id=(?)"""
        record = self._query_fetch_one(update_query, (lang, user_id))
        return record

    def add_user(self, tg_id: int, username: str) -> Optional[tuple]:
        add_query = """INSERT INTO user (tg_id, username) VALUES (?, ?)"""
        data = (tg_id, username)
        record = self._query_fetch_one(add_query, data)
        return record

    def get_user(self, tg_id: int) -> Optional[tuple]:
        get_query = """SELECT * FROM user WHERE tg_id = (?)"""
        record = self._query_fetch_one(get_query, (tg_id,))
        return record