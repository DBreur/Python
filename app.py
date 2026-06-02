import requests
import json
import mysql.connector as mysql

connection = mysql.connect(
    host="localhost",
    username="root",
    password="",
    databast="escaperoom"
)

cursor = connection.cursor()
cursor.execute("SELECT * FROM questions")

data = cursor.fetchall()

cursor.close()
connection.close()
print(data)
