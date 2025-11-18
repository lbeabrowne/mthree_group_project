import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

SQL_SERVER = os.getenv("SQL_SERVER")       # e.g. "temp-project.database.windows.net"
SQL_DATABASE = os.getenv("SQL_DATABASE")   # e.g. "weatherdb"
SQL_USER = os.getenv("SQL_USER")           # e.g. "mthreeproject"
SQL_PASSWORD = os.getenv("SQL_PASSWORD")   # e.g. "your_password_here"

def user_log(city: str, temp_c: float | None, user_id: str | None = None) -> None:
    """
    Log a search into Azure SQL.

    Stores:
    - user_id (optional)
    - city name
    - temperature in °C
    - timestamp (handled by DB default GETDATE())
    """

    # Build connection string
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={SQL_SERVER};"
        f"DATABASE={SQL_DATABASE};"
        f"UID={SQL_USER};"
        f"PWD={SQL_PASSWORD};"
    )

    # Connect to DB
    connection = pyodbc.connect(conn_str, timeout=30)
    cursor = connection.cursor()

    # Create table if it does not exist yet
    cursor.execute(
        """
        IF NOT EXISTS (
            SELECT * FROM sysobjects 
            WHERE name='logHist' AND xtype='U'
        )
        BEGIN
            CREATE TABLE logHist (
                id INT IDENTITY PRIMARY KEY,
                user_id NVARCHAR(100) NULL,
                city NVARCHAR(100),
                temp_c FLOAT NULL,
                timestamp DATETIME DEFAULT GETDATE()
            )
        END
        """
    )
    connection.commit()

    # Insert a row for this search
    cursor.execute(
        "INSERT INTO logHist (user_id, city, temp_c) VALUES (?, ?, ?)",
        (user_id, city, temp_c),
    )

    connection.commit()
    connection.close()