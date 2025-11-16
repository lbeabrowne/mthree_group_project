# Run this py script to review all existing search logs stored in Azure SQL DB
import pyodbc

try:
    connection = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=temp-project.database.windows.net;"
    "DATABASE=weatherdb;"
    "UID=mthreeproject;"
    "PWD=m3m3MTHREE;",
    timeout=30
)
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM logHist")

    print("\n Logs - Users' browsing history for weather info \n")

    columns = [column[0] for column in cursor.description]

    while True:
        row = cursor.fetchone()
        if not row:
            break

        for col_name, value in zip(columns, row):
            print(f"{col_name} | {value}")

    cursor.close()
    connection.close()
    print("\nConnection closed.")

except pyodbc.Error as ex:
    print("\nException:", ex)
    print("Closing program...")

    try:
        cursor.close()
    except:
        pass
    try:
        connection.close()
    except:
        pass

    exit()
