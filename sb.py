import time
import sqlite3
from sqlite3 import Error
import random
import helpers
import re

user_id = '1'

oldtag = "cs50"

newertag = "not_cs50"

db_info = [newertag, user_id]

tags = helpers.current_tags(user_id)

print(tags)

# tag_column = helpers.find_tag_column(tags, oldtag)
tag_column = 'tag7'

print(tag_column)

conn = helpers.connect_db("journ.db")
c = conn.cursor()
c.execute(f"UPDATE tags SET {tag_column} = ? WHERE user_id = ?", db_info)

conn.commit()

tags = helpers.current_tags(user_id)

print(tags)
conn.close()