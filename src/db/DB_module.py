#Make sure you have "ODBC Driver 17 for SQL Server" installed on your machinem link:
#  https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

import pyodbc
from datetime import datetime

#user_log is a prodcedure created for main scripts that returns no value back
#It is a one-way street that send the data to the Azure SQL DB. The way to review the data is writen to logs_monitor.py

#assume the placeholder containing the weather info from the main script is called "data" 
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

#Automation for table creation. With IF NOT EXISTS error handling. It would only create once in first run, avoding repeat creation.
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

#Completely disconnect to the DB server