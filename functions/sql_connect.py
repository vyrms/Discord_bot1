import os

from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode
import psycopg2.errorcodes
import psycopg2


class DBcon:
    def __init__(self, guild_id):
        # loads contents of .env into environment
        load_dotenv()

        # connect to mysql
        self.username = os.getenv('USER')
        self.password = os.getenv('PASSWORD')
        self.hostname = os.getenv('HOST')

        # try to connect to the database
        self.db = "db" + str(guild_id)
        self.cnx = None
        self.cur = None

    def db_connect(self):
        self.cnx = mysql.connector.connect(user=self.username, password=self.password,
                                           host=self.hostname,
                                           database=self.db)
        self.cur = self.cnx.cursor()

    def db_maker(self):
        # make database
        self.cnx = mysql.connector.connect(user=self.username, password=self.password,
                                           host=self.hostname)
        self.cur = self.cnx.cursor()

        print(f"making database {self.db}")
        self.cur.execute(f"CREATE DATABASE if not exists {self.db}")
        self.cur.execute(f"use {self.db}")

    def table_maker(self):
        senryu = "create table if not exists senryu (" \
                 "idx int auto_increment primary key," \
                 "ku varchar(255)," \
                 "author varchar(255)" \
                 ")"
        self.cur.execute(senryu)
        print("senryu table good")

        vocab = "create table if not exists vocab (" \
                "idx int auto_increment primary key," \
                "trig varchar(255)," \
                "resp varchar(255)" \
                ")"
        self.cur.execute(vocab)
        print("vocab table good")

    def close(self):
        self.cur.close()
        self.cnx.close()
