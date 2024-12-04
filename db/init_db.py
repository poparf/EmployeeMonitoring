import sqlite3
conn = sqlite3.connect('../../example2.db')
# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create a table for keystrokes



# Create table
cursor.execute('''CREATE TABLE IF NOT EXISTS stocks
             (date text, trans text, symbol text, qty real, price real)''')

# Insert a row of data
cursor.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
conn.commit()

# Close the connection
conn.close()

""""
check the latest commit to the main server
send the data that was not sent to the server

"""