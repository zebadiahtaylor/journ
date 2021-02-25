from flask import render_template, request
import sqlite3
from sqlite3 import Error
import re
import time
import urllib.parse

def apology(message, code=400):
    """
    Render message as an apology to user. || citation: cs50 staff, 2020
    """
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

def current_tags(user_id):
    """
    finds & returns list of user's tags
    """
    tags= []
    with sqlite3.connect("journ.db") as conn:
        dbtags = conn.execute("SELECT tag1, tag2, tag3, tag4, tag5, tag6, tag7, tag8 FROM tags WHERE user_id=?",
                            user_id
                            )
    for row in dbtags:
        for item in row:
            tags.append(item)

    return tags

def create_entry(user_id):
    """
    uses username + utc microseconds to create unique name & writes the entry.
    """
    entry_name = f"{user_id}_{time.time()}.txt"
    entry = request.form.get("entry")

    with open(fr"entries/{entry_name}", "w") as entry_writer:
        entry_writer.write(entry)

    return entry_name

def find_entry_info(user_id):
    """
    Queries databases regarding users' entries & returns a pair of dictionaries: entry_info & entry_tags
    """
    entry_info = {}
    entry_tags = {}

    # makes dict w/ {entry_url:[date, time]}
    with sqlite3.connect("journ.db") as conn:
        data_handler = conn.execute("SELECT entry_url,date,time FROM entries WHERE user_id=? ORDER BY date DESC, time DESC",
                    user_id)
    for row in data_handler:
        entry_info[row[0]]=[row[1], row[2]]

    # adds entry text to entry_info. It becomes {entry_url:[date,time,text]}
    missing_entries = [] # for handling FileNotFile errors for missing entries
    for each_entry in entry_info.keys():
        try:
            with open(fr"entries/{each_entry}") as reader:
                reader = reader.read()
                entry_info[each_entry].append(reader)

    # handles deleted or lost files
        except FileNotFoundError:
            missing_entries.append(each_entry)

    for each_entry in missing_entries:
        del entry_info[each_entry]

    # Makes dict called entry_tags: {entryname:[tags]}
    data_handler = conn.execute("SELECT entry_url,tag1,tag2,tag3,tag4,tag5,tag6,tag7,tag8 FROM entries WHERE user_id=? ORDER BY date DESC, time DESC",
                user_id)
    for row in data_handler:
        entry_tags[row[0]] = [i for i in row if i]
    for key in entry_tags.keys():
        del entry_tags[key][0]

    return entry_info, entry_tags

def find_free_tag_column(tags):
    """
    When user adds a new tag, identifies an empty db column 
    & returns the column's name.
    """
    that_tag_column = ""
    counter = 0
    for tag in tags:
        counter += 1
        if tag == None:
            that_tag_column = "tag" + str(counter)
            break
    return that_tag_column

# TODO combine with find free tag column() ??
def find_tag_column(tags, oldtag):
    """
    When user replaces a tag, identifies the old tag's column 
    & returns column's name.
    """
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
    Creates a dict, where k = the user-created tag names, like 'life',
    v = db column names, like 'tag1'}
    """
    all_tag_columns = {}
    counter = 0
    for tag in tags:
        counter += 1
        all_tag_columns[str(tag)] = "tag" + str(counter) 
    return all_tag_columns

def get_selected_tags(tags):
    """
    Checks what tags are selected/checked on journ's entry page.
    """
    users_tags = {}
    selected_tabs = []
    for tag in tags:
        users_tags[tag] = request.form.get(f"{tag}")
    for tag in tags:
        if users_tags[tag]: 
            selected_tabs.append(tag)
    return selected_tabs

def handle_newtag_request(tags, user_id):
    """
    new tag handler. returns True if successful
    """
    if request.form.get("newtag"):

        # Converts to valid tag (spaces and letters)
        newtag = re.sub(r'[^A-Za-z0-9]+', '', request.form.get("newtag"))

        # Checks if tag limit has been reached
        if None not in tags:
            return False
        
        # Finds first empty column and returns column name
        else:
            tag_column = find_free_tag_column(tags)

            # Then inserts user's newtag name into db
            db_info = [newtag, user_id]

            with sqlite3.connect("journ.db") as conn:
                conn.execute(f"UPDATE tags SET {tag_column} = ? WHERE user_id = ?",
                    db_info
                    )
            
            return True

def handle_replace_tag_request(user_id, tags):
    """
    User replaces an old tag with a new(er) tag. 
    """
    newertag = re.sub(r'[^A-Za-z0-9 ]+', '', request.form.get("newertag"))
    oldtag = request.form.get("oldtag")
    tag_column = str(find_tag_column(tags, oldtag))
    db_info = [newertag, user_id]

    with sqlite3.connect("journ.db") as conn:
        conn.execute(f"UPDATE tags SET {tag_column} = ? WHERE user_id = ?", db_info)

def insert_data(dataset, selected_tags, tag_column_pairs):
    """
    Writes a unique sql query/INSERT string based on tags
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
    with sqlite3.connect("journ.db") as conn:
        conn.execute(f"INSERT into entries ('user_id', 'entry_url'{query_string}) VALUES (?, ?{values})",
                dataset)

def write_new_entry(user_id, tags, tag_column_pairs):
    """
    creates a new entry and updates the database.
    """
    selected_tags = get_selected_tags(tags)
    entry_name = create_entry(user_id)
    dataset = [user_id, entry_name]
    insert_data(dataset, selected_tags, tag_column_pairs)