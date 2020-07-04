#!/usr/bin/python
import sqlite3
from beautifultable import BeautifulTable

def function_name(result):
    table=BeautifulTable()
    #table.column_headers["Title"]
    for row in result:
        table.append_row(row)
    print(table)

#connect to db
conn = sqlite3.connect('/home/ananchev/plexdb/com.plexapp.plugins.library.db')
c = conn.cursor()
c.execute('select * from metadata_items limit 10')
function_name(c)

