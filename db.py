#!/usr/bin/env python3
import psycopg2

# connect to the db 
con = psycopg2.connect(
        host = "igodlab-ROG-Zephyrus-G15-GA502IU-GA502IU",
        database = "dvdrental",
        user = "postgres",
        password = "postgres"
        )

# create cursor
cur = con.cursor()
#cur.execute("insert into employees (id, name) values (%s, %s)", (1,"John")
#cur.commit() # only if we are inserting something to the db

# execute the query
cur. execute("select first_name, last_name from actor")

# return the rows & close the cursor
rows = cur.fetchall()

for r in rows:
    print(f"first_name {r[0]} last_name {r[1]}")

cur.close()

# close the connection
con.close()
