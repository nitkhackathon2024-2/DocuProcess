import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect(r'D:\Nitk_Hackathon_new\Nitk_Hackathon\flask-backend\structured_data.db')

cursor = conn.cursor()

# Execute a query to retrieve data
cursor.execute("SELECT * FROM documents")
data = cursor.fetchall()

# Process the data
for row in data:
    print(row)

# Close the connection
conn.close()