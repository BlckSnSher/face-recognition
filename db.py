import mysql.connector as con

conn = con.connect(
    host="localhost",
    user="root",
    password="root",
    database="mydb"
)

cursor = conn.cursor()

# cursor.execute("DROP TABLE IF EXISTS students")
# conn.commit()

# std_id = input("Enter student ID: ")
# cursor.execute(f"SELECT * FROM students WHERE student_id = '{std_id}'")
# r = cursor.fetchone()

# for i in range(len(r)):
#     fname = r[1]
#     lname = r[2]

# print(fname, lname)
name = input("Enter name: ")
cursor.execute(f"select * from students where firstname like '%{name}%'")
for x in cursor:
    print(x)
