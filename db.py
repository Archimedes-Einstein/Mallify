import pymysql
mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="astroworld@19",
)
my_cursor = mydb.cursor()
my_cursor.execute("CREATE DATABASE data")
my_cursor.execute("SHOW DATABASES")
for data in my_cursor:
    print(data)