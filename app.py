"""
journ
a personal app for journaling
by zebadiah s. taylor dec 2020 / 2021
"""
from flask import Flask, flash, render_template, redirect, request, session
import helpers
from helpers import apology, current_tags, find_tag_column
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
    # retrieves user's tags data for use in either "POST" or "GET" 
    tags = current_tags(user_id)

    # finds tag_column_pairs (key = tag, value = column_name)
    tag_column_pairs = helpers.find_tag_column_pairs(tags)

    # user submits a post to be recorded
    if request.method == "POST":

        # rejects blank entry   | TODO move this to javascript on page. 
        if not request.form.get("entry"):
            return apology("You must type something to make an entry")

        # writes new entry and updates database
        else:
            helpers.write_new_entry(user_id, tags, tag_column_pairs)
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
    tags = current_tags(user_id)
    
    # finds tag_column_pairs (key = tag, value = column#)
    tag_column_pairs = helpers.find_tag_column_pairs(tags)

    # user may alter their tag-related data. || future project upgrade: javascript alerts to prevent needless reloading.
    if request.method == "POST":

        if request.form.get("newtag"):

            if helpers.handle_newtag_request(tags, user_id):
                return redirect("/tags.html")

            else: 
                return apology("8 tag limit. try to change a tag instead.")

        # replaces existing tag
        # TODO prone to user error, TODO use JS to disable buttons until submit
        elif request.form.get("newertag") and request.form.get("oldtag"):
            helpers.handle_replace_tag_request(user_id, tags)

            return redirect("/tags.html")

        # handles a user error
        elif request.form.get("newertag") and not request.form.get("oldtag"):
            return apology("choose a tag to replace")

        # TODO replaces existing tag AND updates tags for all previous entries
            # TODO
        else:
            return apology("entries required") 
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