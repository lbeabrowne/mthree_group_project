#This is a module built for importing into the main script
#Make sure you have "ODBC Driver Version 17 for SQL Server" (not v18) downloaded and installed on your machinem, skip the configurtion, link:
#  https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

import pyodbc
from datetime import datetime

#user_log() is a prodcedure that bridges the main script with the Azure  SQL DB.
#It creates a one-way street sending fetched data(json/ py dict) to the Azure SQL DB, and return no values.
# Another scipt - logs_monitor.py is created to review the tables and values stored in DB. It simply runs in terminal without the need to use any SQl managament tool.

# "data" is the parameter set in the function(or prodcedure). In the main script, you would stuff it with the variable of the fetched data(json/ py dict).
def user_log(data):
    connection = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=temp-project.database.windows.net;"
    "DATABASE=weatherdb;"
    "UID=mthreeproject;"
    "PWD=m3m3MTHREE;",
    timeout=30
)

    cursor = connection.cursor()

#Automation for table creation. With IF NOT EXISTS error handling, table would be only created once without repeating when user_log runs again.
# Note that: column names are presumed. Needa modify later when the main script has been formed.
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='logHist')
        BEGIN
                              
            CREATE TABLE logHist (
                   
            id INT IDENTITY PRIMARY KEY,
            location NVARCHAR(100),
            temp_c FLOAT,
            wind_mph FLOAT,
            precip_mm FLOAT,
            humidity INT,
            cloud INT,
            timestamp DATETIME DEFAULT GETDATE() 
        )
        END                       
    """)

    connection.commit()
#automation for logs insertion
    cursor.execute("""
        INSERT INTO logHist (location, temp_c, wind_mph, precip_mm, humidity, cloud)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data.get("location"),
        data.get("temp_c"),
        data.get("wind_mph"),
        data.get("precip_mm"),
        data.get("humidity"),
        data.get("cloud"),
    ))

    connection.commit()
    connection.close()

#Completely disconnect from the DB server