import mysql.connector
from mysql.connector import Error

class Hospitals:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='cts.mysql.database.azure.com',
                database='hospitals',
                user='atheeq',
                password='@Super123'
            )
            self.cursor = self.connection.cursor()
            print("connected successfully")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.connection = None
            self.cursor = None

    def network_hospitals(self, table_name, pincode):
        if not self.connection or not self.cursor:
            print("No connection to the database.")
            return []

        try:
            query = f"SELECT hospital_name, city, address FROM {table_name} WHERE pin = %s;"
            self.cursor.execute(query, (pincode,))
            rows = self.cursor.fetchall()
            print("returning from database")
            return rows
        except Error as e:
            print(f"Error executing query: {e}")
            return []