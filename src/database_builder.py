import sqlite3

class UserListTableBuilder:
    """
    class responsible for building the user list table
    """

    def __init__(self):
        self.db_connection = sqlite3.connect("chat_db.db")
        pass

    def create_table(self) -> bool:
        try:
            self.db_connection.execute("CREATE TABLE `user_list` (\
                `phone_number`	INTEGER UNIQUE,\
                `user_name`	TEXT,\
                `region_code`	INTEGER,\
                `mail_id`	TEXT UNIQUE,\
                `sec_question`	TEXT,\
                `sec_answer`	TEXT,\
                PRIMARY KEY(`phone_number`)\
                );")
        except Exception:
            pass 