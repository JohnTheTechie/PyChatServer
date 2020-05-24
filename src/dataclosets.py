########################################################################################################################
# author            :   Janakiraman Jothimony
# created date      :   24-05-2019
# modified date     :   24-05-2019
# version           :   1.0
# description       :   classes defining the database handlers
########################################################################################################################


import sqlite3
from random import randint
import time
from datetime import date
from enum import Enum
import os
from src.configuration_managers import *


class ChatDB:
    """
    class for referencing the db

    Whenever db operation is needed to be done, connection should be sought and once the operation is over,
    close_connection() function should be called
    """

    def __init__(self, **kwargs):
        if kwargs.keys().__contains__("mock") and kwargs["mock"]:
            self.database_name = "../db/test_chat_db.db"
        else:
            self.database_name = "../db/chat_db.db"
        self.db_connection = sqlite3.connect(self.database_name)

    def get_connection(self):
        """
        returns the db object

        :return: db
        """
        return self.db_connection

    def get_cursor(self):
        """
        returns the cursor object
        :return: sqlite3.Cursor
        """
        return self.db_connection.cursor()

    def close_connection(self):
        """
        close the existing connection and reinitializes a new connection
        :return: None
        """
        self.db_connection.close()
        self.db_connection = sqlite3.connect(self.database_name)


class DB_Keywords(Enum):
    """
    enumeration for the sqlite keywords
    """
    TEXT = "TEXT"
    NULL = "NULL"
    INTEGER = "INTEGER"
    REAL = "REAL"
    BLOB = "BLOB"


class DB_Executor:
    """
    class for executing the queries

    for running each query a new instace needs to be created.
    On initializing a reference to the db is to be passes. After execution, the call will take care of closing
    """

    def __init__(self, db: ChatDB):
        assert db is not None
        self.db = db

    def __execute(self, query):
        """
        runs the query and chandles connection. Private function.

        :param query: query to be run in string format
        :return: None
        """
        cursor = self.db.get_cursor()
        cursor.execute(query)
        self.db.get_connection().commit()
        self.db.close_connection()

    def create_table(self, table_name, parameter_list, primary_key=None):
        """
        function runs query for creating the table with specified column

        :param table_name: name of the table
        :param parameter_list: list of tuple pairs of column names and their type
        :param primary_key: TBD
        :return: None
        """
        query = f"CREATE TABLE {table_name} "
        columns_desription = "("

        for pair in parameter_list:
            columns_desription = columns_desription + pair[0] + " " + pair[1].value + ", "

        columns_desription = columns_desription[:-2] + " )"
        query = query + columns_desription
        self.__execute(query)

    def insert_data(self, table_name, parameter_list):
        """
        function runs a query to insert the supplied data

        :param table_name: name of the table
        :param parameter_list: list of values to push
        :return: None
        """
        query = f"INSERT INTO {table_name} VALUES "
        columns_desription = "("

        for value in parameter_list:
            columns_desription = columns_desription + "'" + value + "', "

        columns_desription = columns_desription[:-2] + " )"
        query = query + columns_desription
        self.__execute(query)

    def drop_table(self, table_name):
        """
        function runs a query to drop the specified table

        :param table_name: table name to be dropped
        :return: None
        """
        query = f"DROP table {table_name}"
        self.__execute(query)

    def fetch_row(self, table_name, conditions=None, base_operator="AND", verbose_condition=None):
        """
        function returns a row from the table which satisfies the given conditions

        :param table_name: name of the table
        :param conditions: pairs of column names and expected values
        :param base_operator: logical operator (AND or OR)
        :param verbose_condition: if condition is complex, full condition part of query
        :return: tuple of row values
        """
        query = f"SELECT * FROM {table_name} WHERE "
        columns_description = ""

        if verbose_condition is not None:
            query = query + verbose_condition
        else:
            for pair in conditions:
                columns_description = columns_description + pair[0] + "='" + pair[1] + "' " + base_operator + " "

        columns_description = columns_description[:-4]
        query = query + columns_description

        cursor = self.db.get_cursor()
        cursor.execute(query)
        data = cursor.fetchone()
        self.db.close_connection()

        return data

    def fetch_all(self, table_name, conditions=None, base_operator="AND", verbose_condition=None):
        """
        function returns all rows from the table which satisfies the given conditions

        :param table_name: name of the table
        :param conditions: pairs of column names and expected values
        :param base_operator: logical operator (AND or OR)
        :param verbose_condition: if condition is complex, full condition part of query
        :return: tuple of rows of values
        """
        query = f"SELECT * FROM {table_name} WHERE "
        columns_description = ""

        if verbose_condition is not None:
            query = query + verbose_condition
        else:
            for pair in conditions:
                columns_description = columns_description + pair[0] + "='" + pair[1] + "' " + base_operator + " "

        columns_description = columns_description[:-4]
        query = query + columns_description

        cursor = self.db.get_cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        self.db.close_connection()

        return data

    def delete_rows(self, table_name, conditions=None, base_operator="AND", verbose_condition=None):
        """
        function deletes all rows from the table which satisfies the given conditions

        :param table_name: name of the table
        :param conditions: pairs of column names and expected values
        :param base_operator: logical operator (AND or OR)
        :param verbose_condition: if condition is complex, full condition part of query
        :return: None
        """
        query = f"DELETE FROM {table_name} WHERE "
        columns_description = ""

        # if verbose_condition is defined, discard input from the conditions list
        if verbose_condition is not None:
            query = query + verbose_condition
        else:
            for pair in conditions:
                columns_description = columns_description + pair[0] + "='" + pair[1] + "' " + base_operator + " "

        # discard the unnecessary endings
        columns_description = columns_description[:-4] + " "
        query = query + columns_description

        self.__execute(query)

    def get_pragma(self, pragma_name):
        """
        reads the Pragma values of the DB

        :param pragma_name: name of the pragma
        :return: value of the pragma
        """
        query = "PRAGMA " + pragma_name

        cursor = self.db.get_cursor()
        cursor.execute(query)
        data = cursor.fetchone()
        self.db.close_connection()

        return data[0]

    def set_pragma(self, pragma_name, value):
        """
        set the pragma value

        :param pragma_name: name of the pragma
        :param value: value of the pragma
        :return: None
        """
        query = "PRAGMA " + pragma_name + " = '" + str(value) + "'"
        self.__execute(query)


class DB_AuthPipelineBuilder:
    """
    class to build the pipeline database
    """
    table_name = "authpipeline"
    mail = "email_id"
    keycode = "keycode"
    registration_time = "registration_time"
    registration_date = "registration_date"

    def __init__(self, **kwargs):
        if kwargs.keys().__contains__("mock"):
            self.is_mock = kwargs["mock"]
        else:
            self.is_mock = False
        self.db = ChatDB(mock=self.is_mock)

    def create_table(self):
        """
        the function calls the executor and runs the query for building the table
        :return: None
        """
        parameters = ((DB_AuthPipelineBuilder.mail, DB_Keywords.TEXT),
                      (DB_AuthPipelineBuilder.keycode, DB_Keywords.TEXT),
                      (DB_AuthPipelineBuilder.registration_time, DB_Keywords.TEXT),
                      (DB_AuthPipelineBuilder.registration_date, DB_Keywords.TEXT))
        DB_Executor(self.db).create_table(DB_AuthPipelineBuilder.table_name, parameters)
        return self

    def drop_table(self):
        """
        function to drop the table

        :return: None
        """
        DB_Executor(self.db).drop_table(DB_AuthPipelineBuilder.table_name)


class DB_RegisteredUsersBuilder:
    """
    class to build a table for storing the user registration details
    """
    table_name = "users_list_table"
    MAIL_ID = "mailid"
    PHONE_NO = "phone"
    REGISTRATION_DATE = "regdate"

    def __init__(self, **kwargs):
        if kwargs.keys().__contains__("mock"):
            self.is_mock = kwargs["mock"]
        else:
            self.is_mock = False
        self.db = ChatDB(mock=self.is_mock)

    def create_table(self):
        """
        runs the query to create the table

        :return: None
        """
        parameters = ((DB_RegisteredUsersBuilder.MAIL_ID, DB_Keywords.TEXT),
                      (DB_RegisteredUsersBuilder.PHONE_NO, DB_Keywords.TEXT),
                      (DB_RegisteredUsersBuilder.REGISTRATION_DATE, DB_Keywords.TEXT))
        DB_Executor(self.db).create_table(DB_RegisteredUsersBuilder.table_name, parameters)
        return self

    def drop_table(self):
        """
        runs the query for dropping thetable

        :return: None
        """
        DB_Executor(self.db).drop_table(DB_RegisteredUsersBuilder.table_name)


class DB_AuthPipeline:
    """
    class to handle the user details waiting for authentication flow completion

    when a user requests registration, the user is paused to db and token generated and returned
    When the authentication token is confirmed, the entry to be deleted
    """
    def __init__(self, **kwargs):
        if kwargs.keys().__contains__("mock"):
            self.is_mock = kwargs["mock"]
        else:
            self.is_mock = False
        self.db = ChatDB(mock=self.is_mock)

    def add_user_to_pipeline(self, mail_id) -> str:
        """
        adds the email id of the user to the pipeline with random token
        returns the token for confirmation

        :param mail_id: user id
        :return: token generated for user confirmation
        """
        token = randint(1111, 9999)
        registration_time = time.asctime(time.localtime())
        registration_date = date.today().strftime("%Y-%m-%d")

        parameters = (mail_id, str(token), registration_time, registration_date)

        DB_Executor(self.db).insert_data(DB_AuthPipelineBuilder.table_name, parameters)
        return str(token)

    def fetch_user(self, mail_id):
        """
        returns the row containing the user registration data

        :param mail_id: users email id
        :return: row if exist or None
        """
        results: (str, str, str, str) = DB_Executor(self.db).fetch_row(DB_AuthPipelineBuilder.table_name,
                                                                       ((DB_AuthPipelineBuilder.mail, mail_id),))
        if results is not None:
            return results
        else:
            return None

    def get_auth_token(self, mail_id):
        """
        returns the token generated for the user

        :param mail_id: users mail id
        :return: token if exist or None
        """
        results = DB_Executor(self.db).fetch_row(DB_AuthPipelineBuilder.table_name,
                                                 ((DB_AuthPipelineBuilder.mail, mail_id),))
        if results is not None:
            return results[1]
        else:
            return None

    def check_if_authentication_successful(self, mail_id, token):
        """
        checks if the requested users authentication is successful

        return true if success
        if failed returns False
        if not exist return False

        :param mail_id: user id
        :param token: token from user
        :return: return true if success | if failed returns False | if not exist return False
        """
        result = self.fetch_user(mail_id)

        if result is not None and token == result[1]:
            return True
        else:
            return False

    def delete_user(self, mail_id):
        """
        deletes the user entry from the pipeline table

        :param mail_id: user email id to be deleted
        :return: None
        """
        DB_Executor(self.db).delete_rows(DB_AuthPipelineBuilder.table_name, ((DB_AuthPipelineBuilder.mail, mail_id),))


class DB_Builder:
    """
    Builder for the applications DB

    The builder is run only once when the application is started
    If DB does not exist prior, DB is created
    If already existing, version shall be compared and decision shall be taken if update should be run
    At each schema update new update function should be defined, and invoked from __update_schema function
    """
    def __init__(self):
        db_path = ConfigManager(ConfigClass.DATABASE).get_parameter("db_address")
        self.db_exists = os.path.exists(db_path)
        self.db_existing_version = -1
        if self.db_exists:
            self.db_existing_version = int(DB_Executor(ChatDB()).get_pragma("user_version"))
        self.db_new_version = ConfigManager(ConfigClass.DATABASE).get_parameter("version")

    def build(self):
        if not self.db_exists:
            self.__build_fresh_databse()
            DB_Executor(ChatDB()).set_pragma("user_version", self.db_new_version)
        elif self.db_existing_version < self.db_new_version:
            self.__update_schema(self.db_existing_version, self.db_new_version)
            DB_Executor(ChatDB()).set_pragma("user_version", self.db_new_version)
        elif self.db_existing_version > self.db_new_version:
            raise ValueError("Nasama pochu..... evanda lower version schema vechu SW integrate pannavan?")

    def __build_fresh_databse(self):
        DB_AuthPipelineBuilder().create_table()

    def __update_schema(self, from_version, to_version):
        pass

    def __update_x_to_y(self):
        """example def only"""
        pass

