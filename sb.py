import time
import sqlite3
from sqlite3 import Error
import random
import helpers
import re

user_id = '1'

"""
get DATETIME IN LOCALTIME NOT GREENWICH

https://sqlite.org/lang_datefunc.html
https://stackoverflow.com/questions/381371/sqlite-current-timestamp-is-in-gmt-not-the-timezone-of-the-machine
https://www.sqlite.org/lang_datefunc.html
"""

# do the math in python, or have it converted in sql?


# def find_entry_info(user_id):
#     """
#     WE ARE HERE. TRANSLATE UTC TO LOCALTIME. CONSIDER HOW TO MAKE JOURNAL.HTML PRETTIER WHILE YOU'RE AT IT.
#     Queries databases regarding users' entries and returns a pair of dictionaries.
#     """
#     entry_info = {}
#     entry_tags = {}

#     # makes dict w/ {entry_url:[date, time]}
#     conn = connect_db("journ.db")
#     c = conn.cursor()
#     data_handler = c.execute("SELECT entry_url,date,time FROM entries WHERE user_id=? ORDER BY date DESC, time DESC",
#                 user_id)
#     for row in data_handler:
#         entry_info[row[0]]=[row[1], row[2]]
    
#     # adds entry text to entry_info >> {entry_url:[date,time,text]}
#     for each_entry in entry_info.keys():
#         with open(fr"entries\{each_entry}") as reader:
#             reader = reader.read()
#             entry_info[each_entry].append(reader)

#     # makes dict w/ {entryname:[tags]}
#     data_handler = c.execute("SELECT entry_url,tag1,tag2,tag3,tag4,tag5,tag6,tag7,tag8 FROM entries WHERE user_id=? ORDER BY date DESC, time DESC",
#                 user_id)
#     for row in data_handler:
#         entry_tags[row[0]] = [i for i in row if i]
#     for key in entry_tags.keys():
#         del entry_tags[key][0]

#     conn.close()
#     return entry_info, entry_tags


entry_info = {}

conn = helpers.connect_db("journ.db")
c = conn.cursor()
data_handler = c.execute("SELECT entry_url,date('localtime'),time FROM entries WHERE user_id=? ORDER BY date DESC, time DESC",
            user_id)
for row in data_handler:
    entry_info[row[0]]=[row[1], row[2]]
    print(entry_info[row[0]])
conn.close()