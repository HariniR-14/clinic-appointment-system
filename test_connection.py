import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Harini@14",
    database="crud"
)

cursor = conn.cursor()
cursor.execute("SHOW TABLES")

for table in cursor:
    print(table)

conn.close()