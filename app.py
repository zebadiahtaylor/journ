"""
journ
a personal app for journaling
by zebadiah s. taylor dec 2020, for cs50
"""
from flask import Flask, flash, render_template, redirect, request, session
import helpers
from helpers import apology, connect_db, current_tags, find_tag_column
import re
import time
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

app = Flask(__name__)

# db = connect_db("journ.db")

# for development only
user_id = '1'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# home page after login. | emphasizes ease of entry-writing
@app.route("/", methods=["GET", "POST"])
def home():
    # retrieves user's tags data for use in either "POST" or "GET", and all_tag_column_pairs (key = tag, value = column#)
    tags, all_tag_column_pairs = current_tags(user_id)
    
    # user submits a post to be recorded
    if request.method == "POST":

        # a list of the user's selected tabs | currently, we only use 1
        selected_tabs = helpers.get_selected_tags(tags)

        # rejects blank entry   | move this to javascript on page. 
        if not request.form.get("entry"):
            return apology("No entry")
        
        # rejects multiple selected tabs. TODO: double-check to see if 2 would cause complications.
        elif not len(selected_tabs) == 1:
            return apology("this is beta; pick 1 tab & 1 only")

        # writes new entry and updates database
        else:
            # saves entry as a file | uses username + utc microseconds to create unique name
            entry_name = f"{user_id}_{time.time()}.txt"
            entry = request.form.get("entry")
            with open(fr"entries\{entry_name}", "w") as entry_writer:
                entry_writer.write(entry)
            
            # a list to put into SQL
            dataset = [user_id, entry_name, selected_tabs[0]]

            # stores the info in the database
            conn = connect_db("journ.db")
            c = conn.cursor()
            c.execute(f"INSERT into entries ('user_id', 'entry_url', {all_tag_column_pairs[selected_tabs[0]]}) VALUES (?, ?, ?)",
                        dataset)
            conn.commit()
            conn.close()

            return redirect("/")
    else:
        return render_template("index.html", tags=tags)

@app.route("/journal.html", methods=["GET", "POST"])
def journal():
    if request.method == "GET":
        # retrieves entries' urls, dates, & times
        entry_info, entry_tags = helpers.find_entry_info(user_id)

        return render_template("journal.html", entry_info=entry_info, entry_tags=entry_tags)

# User creates and manages tags
@app.route("/tags.html", methods=["GET", "POST"])
def tags():
    """
     user may see and change current tag information
    """
    # retrieves user's tags data for use in either "POST" or "GET"
    tags, all_tag_column_pairs = current_tags(user_id)

    # user may alter their tag-related data. || future project upgrade: javascript alerts to prevent needless reloading.
    if request.method == "POST":

        # user adds a new tag
        if request.form.get("newtag"):

            # converts to valid tags (spaces and letters)
            newtag = re.sub(r'[^A-Za-z0-9]+', '', request.form.get("newtag"))

            # checks to make sure tag limit hasn't been exhausted || upgrade: add alert in javascript.  
            if None not in tags:
                return apology("8 tag limit. try to change a tag instead.")

            # finds first empty spot and returns column name
            else:
                tag_column = helpers.find_free_tag_column(tags)

                # AND inserts the information into the databases
                db_info = [newtag, user_id]

                conn = connect_db("journ.db")
                c = conn.cursor()

                c.execute(f"UPDATE tags SET {tag_column} = ? WHERE user_id = ?", db_info)
                
                conn.commit()
                conn.close()
                return redirect("/tags.html")

        # replaces existing tag only
        # TODO clean this mess up
        # TODO prone to user error, use JS to disable buttons until submit
        elif request.form.get("newertag") and request.form.get("oldtag") and not request.form.get("replace_existing"):
            newertag = re.sub(r'[^A-Za-z0-9 ]+', '', request.form.get("newertag"))
            oldtag = request.form.get("oldtag")
            tag_column = str(find_tag_column(tags, oldtag))
            db_info = [newertag, user_id]

            conn = connect_db("journ.db")
            c = conn.cursor()
            c.execute(f"UPDATE tags SET {tag_column} = ? WHERE user_id = ?", db_info)

            conn.commit()
            conn.close()
            return redirect("/tags.html")

        # handles a user error
        elif request.form.get("newertag") and not request.form.get("oldtag"):
            return apology("choose a tag to replace")

        # TODO replaces existing tag AND updates tags for all previous entries
            # TODO

        else:
            return apology("entries required") 
        # insert into SQL database
        # update page
        # return render_template("tags.html")
    else:  
        return render_template("tags.html", tags=tags)


"""
etcetera. lifted from cs50 finance to help w/ debugging.  
"""
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)