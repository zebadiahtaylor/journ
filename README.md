# journ

#### Video Demo: <https://youtu.be/zZbSvJnw9Iw>

### Description
journ is a basic journaling app with advanced organization options and scalability. 


#### Features
- Fast, no hassle entry.
- Stores all entries for future use.
- The user can create or modify up to 8 tags
- Offline access!
- Free!

#### Possible Upcoming Features:
- Multiple users and cloud-based availability
- Rich-text support.
- Night-mode | day mode options. 
- Organization of entries by tags and date. 
- Visual data representation of journal entries, based on tags and dates. 
- Ease of use and online access.
- More security. 




#### HOW TO USE
1. At the command line, navigate to the folder in which app.py is stored
2. type pip3 install flask
3. type ‘flask run’.
4. On the same computer, open a browser and navigate to 'localhost:5000'

###### Once in the app
1. Type in the given text area and submit. 
    - Optionally: click a checkbox to ‘tag’ the entry.
2. Optionally, use the navbar at the top to:
    - Manage tags: click on “tags” in the navigation bar at the top. 
    - See all previous entries: click on “journal” at the top.
    - Return to the entry-writing page: click “journ” at the top. 


#### WHY?

I’ve enjoyed journaling from a young age. Over the years, it has helped me mature and discover myself. Even now, I find it useful for processing what I’ve learned or accomplished as a coder, recording health information, unique experiences, or the quick ideas that don’t quite belong anywhere else. 

#### ... but why journ?

Sure, there are plenty of other journaling apps out there with great features, but few are as fast and snappy and “done!” as journ . . . also, the bones developed in journ should be useful in a future project I have planned.

#### Design Decisions

journ was designed to be simple, but some decisions were made to allow room for additional features in future iterations. 

For example, in its current implementation, journ stores the user’s entries as individual .txt files and tracks them through URLs stored in the database. While it may be faster and more efficient to store user’s input in the database itself, this decision will allow rich-text in future iterations, as well as photos and other sorts of files. 

To avoid possible repeated file names, all users’ entries have the following naming convention: {user_id}_{utc time in microseconds}.txt. My hope is that this would be sufficient to avoid accidental overwrites or loss data. However, multiple users using the same account COULD break this. Further development is required.

Currently, users’ entries are un-encrypted, which is a potential security risk, but the project couldn’t launch with this feature. Users should take care to protect their data and be conscious about what they choose to record. 

In its current state, although the database already allows for multiple users, the app is hardcoded to only have 1 user. This was initially a choice made to speed production, but this choice has changed the app's identity in the short term: it's an offline command line app that happens to use a browser/Flask. Eventually, however, I hope to expand upon this eventually and allow for multiple users. 

#### FOLDERS/FILES: DESCRIPTION

- \entries(folder) 
    - this stores the user’s entries. I have provided a few as examples. 
- \templates(folder): 
    - stores all templates
- \templates\apology.html
    - this page is lifted from cs50’s Finance assignment and will be removed during further development.
- \templates\index.html
    - the starting page of journ. The textarea has focus for ease of use. Available tags are ready to be checked. 
- \templates\journal.html
    - displays users’ previous entries. 
- \templates\layout.html
    - functions as a standard layout.html as per Flask/jinja2 conventions. Contains code from my ‘Homepage’ project for cs50, which in turn contains code adapted from w3schools.com.
- \templates\tags.html
    - displays users current tags, and allows them to add tags or modify existing tags. 
- \app.py 
    - flask app that processes the data and runs the app. Hooray for Python!
    - some code is adapted from cs50's 2020 Finance project 
- \helpers.py
    - keeps all the ugly functions out of app.py so that it’s clean and easy to understand. functions are organized alphabetically. 
- \journ.db 
    - contains user data in 3 tables: users, entries, tags.
- \README.md
    - a very helpful document. 
- \requirements.txt
    - lists requirements

#### Notes & Citations

journ was written by Zebadiah S. Taylor for the Final Project in cs50 2020. However, it was completed and turned in January, 2021.

Some code is taken from the given cs50 2020 Finance assignment, most egregiously the apology() function. Other snippets are taken from standard documentation and stackoverflow responses. More specific citations can be found in the FOLDERS/FILES: DESCRIPTION section.

Upon request, psuedocode and further notes can be provided.

Developed in VSCODE.

#### Thanks 

Thanks to David Malan and the cs50 staff, grumpy cat, Cameron M., Stackoverflow and its many contributors, Jace Browning, Al Sweigart, and most of all, my wife.
