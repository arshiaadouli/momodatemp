import mysql.connector

# Establish the connection
cnx = mysql.connector.connect(
    host="sql992.main-hosting.eu",
    user="u528062626_prd",
    password="1fqr;AG;",
    database="u528062626_prd"
)

# Create a cursor object to interact with the database
cursor = cnx.cursor()

# Execute a sample query
query = "SELECT * FROM kpdata"
cursor.execute(query)

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the cursor and the connection
cursor.close()
cnx.close()