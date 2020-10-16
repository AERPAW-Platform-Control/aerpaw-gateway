#!/usr/bin/python

import sys
import mysql.connector
from mysql.connector import Error


sql_query = sys.argv[1]
if 'select' not in sql_query:
    print("Error: Query not allowed")
    exit()
try:
    connection = mysql.connector.connect(host='localhost',
                                         database='tbdb',
                                         user='mysql',
                                         password='',
                                         unix_socket='/tmp/mysql.sock')

    cursor = connection.cursor()
    cursor.execute(sql_query)
    records = cursor.fetchall()

    for row in records:
        print(row)

except Error as e:
    print("Error: ", e)
finally:
    if connection.is_connected():
        connection.close()
        cursor.close()
