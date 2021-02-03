
from flask import render_template, request
import sqlite3
from sqlite3 import Error
import time
import urllib.parse

def apology(message, code=400):
    """Render message as an apology to user. || citation: cs50 staff, 2020"""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def connect_db(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("data_base accessed")
    except:
        print("problem connecting with database")
    return connection

# returns list of tags and dict w/ tags(keys) and columns (values)
def current_tags(user_id):
    
    # finds current tags and returns tags []
    tags= []
    conn = connect_db("journ.db")
    dbtags = conn.execute("SELECT tag1, tag2, tag3, tag4, tag5, tag6, tag7, tag8 FROM tags WHERE user_id=?",
                            user_id
                            )
    for row in dbtags:
        for item in row:
            tags.append(item)
    print(f"the tags are: {tags}")
    conn.close()

    return tags

def create_entry(user_id):
    # uses username + utc microseconds to create unique name. TODO: improve for multiple simultaneous entries per user
    entry_name = f"{user_id}_{time.time()}.txt"
    entry = request.form.get("entry")
    with open(fr"entries\{entry_name}", "w") as entry_writer:
        entry_writer.write(entry)
    return entry_name

def find_entry_info(user_id):
    """
    Queries databases regarding users' entries and returns a pair of dictionaries.
    """
    entry_info = {}
    entry_tags = {}
    conn = connect_db("journ.db")
    c = conn.cursor()

    # makes dict w/ {entry_url:[date, time]}
    data_handler = c.execute("SELECT entry_url,date,time FROM entries WHERE user_id=? ORDER BY date DESC, time DESC",
                user_id)
    for row in data_handler:
        entry_info[row[0]]=[row[1], row[2]]
    
    # adds entry text to entry_info >> {entry_url:[date,time,text]}
    for each_entry in entry_info.keys():
        with open(fr"entries\{each_entry}") as reader:
            reader = reader.read()
            entry_info[each_entry].append(reader)

    # makes dict w/ {entryname:[tags]}
    data_handler = c.execute("SELECT entry_url,tag1,tag2,tag3,tag4,tag5,tag6,tag7,tag8 FROM entries WHERE user_id=? ORDER BY date DESC, time DESC",
                user_id)
    for row in data_handler:
        entry_tags[row[0]] = [i for i in row if i]
    for key in entry_tags.keys():
        del entry_tags[key][0]

    conn.close()
    return entry_info, entry_tags

def find_free_tag_column(tags):
    that_tag_column = ""
    counter = 0
    for tag in tags:
        counter += 1
        # names it, for insertion into the databases
        if tag == None:
            that_tag_column = "tag" + str(counter)
            break
    return that_tag_column

# TODO combine with find free tag column()
def find_tag_column(tags, oldtag):
    that_tag_column = ""
    counter = 0
    for tag in tags:
        counter += 1
        if tag == oldtag:
            that_tag_column = "tag" + str(counter)
            break
    return that_tag_column

def find_tag_column_pairs(tags):
    """
    creates a dict w/ tags (keys) and columns (values)
    """
    all_tag_columns = {}
    counter = 0
    for tag in tags:
        counter += 1
        all_tag_columns[str(tag)] = "tag" + str(counter) 
    print(f"all_tag_columns = {all_tag_columns}")
    return all_tag_columns

# checks what tags are turned on
def get_selected_tags(tags):
    users_tags = {}
    selected_tabs = []
    for tag in tags:
        users_tags[tag] = request.form.get(f"{tag}")
    print(f"selected tags as a dict:__ {users_tags}")
    for tag in tags:
        if users_tags[tag]: 
            selected_tabs.append(tag)
    print(f"these are the selected tabs as a list:{selected_tabs}")
    return selected_tabs

def insert_data(dataset, selected_tags, tag_column_pairs):
    """
    Writes a unique sql query/INSERT string depeneding on tag# numbers
    """
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

    # inserts entry/tag info into the database for later retrieval
    conn = connect_db("journ.db")
    c = conn.cursor()
    c.execute(f"INSERT into entries ('user_id', 'entry_url'{query_string}) VALUES (?, ?{values})",
             dataset)
    conn.commit()
    conn.close()