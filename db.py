import pymysql
import os
from dotenv import load_dotenv
load_dotenv()
mydb = pymysql.connect(
    host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
)
my_cursor = mydb.cursor()
my_cursor.execute("CREATE DATABASE data")
my_cursor.execute("SHOW DATABASES")
for data in my_cursor:
    print(data)