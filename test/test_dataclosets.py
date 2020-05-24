from unittest import TestCase
from src.dataclosets import DB_AuthPipelineBuilder, DB_AuthPipeline
from src.dataclosets import *
import sqlite3
import time
from datetime import date
import os

class Test_DB_Executor(TestCase):

    def setUp(self) -> None:
        if os.path.exists("../db/test_chat_db.db"):
            os.remove("../db/test_chat_db.db")
        self.db = ChatDB(mock=True)

    def test_executor(self):
        DB_Executor(self.db).create_table("reg", (("name", DB_Keywords.TEXT), ("token", DB_Keywords.TEXT)))
        DB_Executor(self.db).insert_data("reg", ("janaki", "1234"))
        print(DB_Executor(self.db).fetch_row("reg", (("name","janaki"),)))
        DB_Executor(self.db).drop_table("reg")

class test_AuthPipeline(TestCase):

    def setUp(self) -> None:
        '''
        if os.path.exists("../db/test_chat_db.db"):
            os.remove("../db/test_chat_db.db")
        DB_AuthPipelineBuilder(mock=True).create_table()
        self.pipeline = DB_AuthPipeline(mock=True)
        '''
        DB_Builder().build()
        self.pipeline = DB_AuthPipeline()

    def test_auth(self):
        mail_id = "janakiraman3394@gmail.com"
        token = self.pipeline.add_user_to_pipeline(mail_id)
        self.assertTrue(self.pipeline.fetch_user(mail_id) is not None)
        self.assertEqual(self.pipeline.get_auth_token(mail_id), token)
        self.assertTrue(self.pipeline.check_if_authentication_successful(mail_id, token))
        self.assertFalse(self.pipeline.check_if_authentication_successful("img", token))
        self.pipeline.delete_user(mail_id)
        self.assertTrue(self.pipeline.fetch_user(mail_id) is None)
