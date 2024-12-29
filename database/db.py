import sqlite3

class Database:
    def __init__(self, path: str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS review(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    number_inst TEXT,
                    visit_date TEXT,
                    food_rating TEXT,
                    clean_rating TEXT,
                    extra_comments TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS dish(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name_dish TEXT,
                    cost_dish FLOAT,
                    description_dish TEXT,
                    category_dish TEXT,
                    image_dish TEXT
                )
                """
            )
            conn.commit()





    def execute(self, query: str, params: tuple = ()):
        try:
            with sqlite3.connect(self.path) as conn:
                conn.execute(query, params)
                conn.commit()
        except sqlite3.Error as e:
            print(f"ошибка: {e}")
            raise

    def fetch(self, query: str, params: tuple = ()):
        try:
            with sqlite3.connect(self.path) as conn:
                conn.row_factory = sqlite3.Row
                result = conn.execute(query, params)
                data = result.fetchall()
                return [dict(row) for row in data]
        except sqlite3.Error as e:
            print(f"ошибка: {e}")
            return []

