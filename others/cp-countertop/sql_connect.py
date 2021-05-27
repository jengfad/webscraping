import mysql.connector

# mydb = mysql.connector.connect(
#     host="localhost",
#     user="admin",
#     password="password123",
#     database="cp"
# )

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="cp"
)


def insert_data(email, location, phone, website):
    mycursor = mydb.cursor()

    sql = ("INSERT INTO ct_countertop "
           "(email, location, phone, website) "
           "VALUES (%s, %s, %s, %s)")
    val = (email, location, phone, website)
    mycursor.execute(sql, val)

    mydb.commit()


def insert_error_logs(notes, error_message):
    mycursor = mydb.cursor()

    sql = ("INSERT INTO ct_error_logs "
           "(notes, error_message) "
           "VALUES (%s, %s)")
    val = (notes, error_message)
    mycursor.execute(sql, val)

    mydb.commit()


def escape_text(text):
    return text.replace("'", "''")


def find_data(website):
    website = escape_text(website)
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(
        f"SELECT * FROM ct_countertop WHERE website = '{website}'")
    return mycursor.fetchone()
