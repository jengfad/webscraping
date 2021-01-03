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
    password="password123",
    database="cp"
)


def insert_magician(name, email, location, index_letter_url, location_url, website):
    mycursor = mydb.cursor()

    sql = ("INSERT INTO magicians "
           "(name, email, location, index_letter_url, location_url, website) "
           "VALUES (%s, %s, %s, %s, %s, %s)")
    val = (name, email, location, index_letter_url, location_url, website)
    mycursor.execute(sql, val)

    mydb.commit()


def insert_error_logs(notes, error_message):
    mycursor = mydb.cursor()

    sql = ("INSERT INTO error_logs "
           "(notes, error_message) "
           "VALUES (%s, %s)")
    val = (notes, error_message)
    mycursor.execute(sql, val)

    mydb.commit()

def insert_finished_location(location):
    mycursor = mydb.cursor()
    sql = f"INSERT INTO finished_locations (location) VALUES ('{location}')"
    mycursor.execute(sql)
    mydb.commit()

def escape_text(text):
    return text.replace("'", "''")

def find_magician(name, location):
    name = escape_text(name)
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(
        f"SELECT * FROM magicians WHERE name = '{name}' AND location = '{location}'")
    return mycursor.fetchone()

def find_finished_location(location):
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(
        f"SELECT * FROM finished_locations WHERE location = '{location}'")
    return mycursor.fetchone()
