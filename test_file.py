import tkinter as tk
import mysql.connector

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="thesis"
)

# Create a cursor object
mycursor = mydb.cursor()

# Create the main window
root = tk.Tk()
root.title("Search Function")

# Create the search bar
search_var = tk.StringVar()
search_bar = tk.Entry(root, textvariable=search_var)
search_bar.pack(padx=10, pady=10)


# Create the search button
def search():
    # Clear the table
    for widget in table_frame.winfo_children():
        widget.destroy()

    # Execute the search query
    query = "SELECT * FROM students WHERE firstname LIKE %s"
    value = ("%" + search_var.get() + "%",)
    mycursor.execute(query, value)
    result = mycursor.fetchall()

    # Create the table headers
    headers = ("ID", "firsname", "lastname", "course", "student id", "section", "course code", "time", "day", "lab room")
    for i, header in enumerate(headers):
        label = tk.Label(table_frame, text=header, font=("Arial", 12, "bold"), relief=tk.RIDGE)
        label.grid(row=0, column=i, sticky="nsew")

    # Create the table rows
    for i, row in enumerate(result):
        for j, item in enumerate(row):
            label = tk.Label(table_frame, text=item, font=("Arial", 12), relief=tk.RIDGE)
            label.grid(row=i + 1, column=j, sticky="nsew")

            # Create the update button for each row
            if j == 0:
                print("update")
                def update(id):
                    # Create the update window
                    update_window = tk.Toplevel(root)
                    update_window.title("Update Item")

                    # Create the text input
                    update_var = tk.StringVar(value=row[1:])
                    update_entry = tk.Entry(update_window, textvariable=update_var, width=30)
                    update_entry.pack(padx=10, pady=10)

                    # Create the update button
                    print("updating items")
                    def update_item():
                        update_query = "UPDATE students SET firstname = %s, lastname = %s, student_id = %s WHERE id = %s"
                        update_values = (update_var.get()[0], update_var.get()[1], update_var()[2], id)
                        mycursor.execute(update_query, update_values)
                        mydb.commit()
                        update_window.destroy()
                        search()

                    update_button = tk.Button(update_window, text="Update", command=update_item)
                    update_button.pack(padx=10, pady=10)

                update_button = tk.Button(table_frame, text="Update", command=lambda id=row[0]: update(id))
                update_button.grid(row=i + 2, column=j + 2, sticky="nsew")


# Create the search button
search_button = tk.Button(root, text="Search", command=search)
search_button.pack(padx=10, pady=10)

# Create the table frame
table_frame = tk.Frame(root)
table_frame.pack(padx=10, pady=10)

# Run the main loop
root.mainloop()
