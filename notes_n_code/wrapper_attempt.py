import functools
import sqlite3 
from sqlite3 import Error

"""
idea: use @ decorators and wrappers to cut out the tedious opening and closing of code.
reality as it stands: 
1. conn is a global variable 😤 
2. the wrapper can't close the database after returning something (unreachable code, see below),
which means conn.close() would have to be included in every function 🤷‍♂️ halfway defeating the purpose of the wrappers 🤬. 
"""

user_id = '1'
conn = None         # using a global that I hope to get rid of soon.  

def connect_db(function):
    """
    wrapper that opens db, performs function, then closes db
    """
    global conn
    try:
        conn = sqlite3.connect("journ.db")
        print("connected")
    except:
        print("problem")

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)
        # conn.close()  # unreachable code
    return wrapper

@connect_db
def find_entry_info(user_id):
    """
    Queries database regarding users' entries and returns a dictionary (k=entry_url, v=[date, time]).
    """
    entry_info = {}
    # entry_tags = {}
    db_handler = conn.execute("SELECT entry_url,date,time FROM entries WHERE user_id=? ORDER BY date DESC, time DESC",
                        user_id
                            )
    for row in db_handler:
        entry_info[row[0]]=[row[1], row[2]]
    return entry_info

entry_info = find_entry_info(user_id)