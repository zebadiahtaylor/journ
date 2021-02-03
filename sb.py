import time
import sqlite3
from sqlite3 import Error
import random
import helpers
import re

user_id = '1'


# full_name = lambda fn, ln: fn.strip().title() + " " + ln.strip().title()

# print(full_name("   zEb", "TAtor"))

# def create_entry(user_id):
#     # uses username + utc microseconds to create unique name. TODO: improve for multiple simultaneous entries per user
#     entry_name = f"{user_id}_{time.time()}.txt"
#     entry = "fake fucking text. delete"
#     with open(fr"entries\{entry_name}", "w") as entry_writer:
#         entry_writer.write(entry)
#     return entry_name

# def save_to_db(dataset, all_tag_column_pairs):  
#     conn = helpers.connect_db("journ.db")
#     c = conn.cursor()
#     c.execute(f"INSERT into entries ('user_id', 'entry_url', {all_tag_column_pairs[selected_tabs[0]]}) VALUES (?, ?, ?)",
#             dataset)
#     conn.commit()
#     conn.close()
"""
figure out how to pass multiple tags to multiple tag column pairs over SQL. 
"""
"""
this lambda syntax works.
"""
dataset = [user_id, "fake name", "all_tag_column_pairs"]
def varied():
    return "uh oh"

g = lambda: varied()
print(f"all my love {g()}")

print(f"INSERT into entries ('user_id', 'entry_url', {varied()}) VALUES (?, ?, ?)",
             dataset)

# write function that generates tag column names as strings separated by commas for use in a sql string.
# challenge: the ?? after VALUES and the dataset itself must be flexible.
# dataset probably already is

#simulated vars
tag_column_pairs = {'dev':'tag4', 'life': 'tag1', 'journ':'tag8'}
selected_tags = ['dev', 'life', 'journ']
dataset = [user_id, "fake name"]  # WATCH OUT FOR

def insert_data(dataset, selected_tags, tag_column_pairs):
    # forms query's first variable part.
    query_string = ""
    for tag in selected_tags:
        if tag in tag_column_pairs:
            query_string += f", '{tag_column_pairs[tag]}'"
    # determines # of ?'s for place holders
    values = ""
    for tag in selected_tags:
        values += f", ?"
    # passes off variable tag values to dataset variable. MAKE SURE DATASET VAR CHANGED.
    for tag in range(len(selected_tags)):
        dataset.append(selected_tags.pop(0))
    print(f"INSERT into entries ('user_id', 'entry_url'{query_string}) VALUES (?, ?{values})",
             dataset)

insert_data(dataset, selected_tags, tag_column_pairs)