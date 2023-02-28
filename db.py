import mysql.connector as con

conn = con.connect(
    host="localhost",
    user="root",
    password="root",
    database="mydb"
)

cursor = conn.cursor()

cursor.execute("select time_out from attendance where firstname = 'King'")
c = cursor.fetchone()
print(c[0])
print(c)
if c[0] == '':
    print("True")
else:
    print("false")

print(cursor.rowcount)
