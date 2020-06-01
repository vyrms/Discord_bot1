import os

from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode


class DBcon:
    def __init__(self, guild_id):
        # loads contents of .env into environment
        load_dotenv()

        # connect to mysql
        username = os.getenv('USER')
        password = os.getenv('PASSWORD')
        hostname = os.getenv('HOST')

        # try to connect to the database
        try:
            db = "db" + str(guild_id)
            self.cnx = mysql.connector.connect(user=username, password=password,
                                               host=hostname,
                                               database=db)
            print("db connected")
            self.cur = self.cnx.cursor()

        except mysql.connector.Error as err:
            # if the database doesn't exist
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                print("db not found. making db")
                self.cnx = mysql.connector.connect(user=username, password=password,
                                                   host=hostname)
                self.cur = self.cnx.cursor()
                self.cur.execute(f"CREATE DATABASE {db}")
                self.cur.execute(f"use {db}")
            else:
                print(err)

    def table_maker(self):
        senryu = "create table if not exists senryu (" \
                 "idx int auto_increment primary key," \
                 "ku varchar(255)," \
                 "author varchar(255)" \
                 ")"
        self.cur.execute(senryu)
        print("table good")

