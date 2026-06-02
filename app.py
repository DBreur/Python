import mysql.connector as mysql

date = input("Datum (YYYY-MM-DD): ")
note = input("Notities: ")

connection = mysql.connect(
    host="localhost",
    username="root",
    password="",
    database="sambo"
)

cursor = connection.cursor()
cursor.execute("INSERT INTO log (datum, note) VALUES (%s, %s)", (date, note))

connection.commit()

cursor.close()
connection.close()
print("log opgeslagen")
