#!/usr/local/bin/python3
#Import the template file
from template import *

#Create the page
create()

#Create the head
head()

#Create the navigation bar
nav()

#Add Welcome message to content
content += """
        <article>
            <h1 class="title">Welcome to PomPal</h1>
            <p><b>PomPal</b>, is the latest innovation in <strong>note taking</strong>, <strong>time keeping</strong> and <strong>task completion</strong>. 
            Inspired by productivity brought by the <strong>Pomodoro Technique</strong> I decided to create a website that allows users to complete tasks in 25 minute segments.
            You can <strong>link notes</strong> to these timers to keep track of where you are.
            You can also <strong>share timers</strong> with your friends to sync up your work schedule, to be productive together and take breaks together!</p>
        </article>
"""

#Check if logged in
if username:
    #Initialise note_list, music_list and note_dict
    note_list = ""
    music_list = ""
    note_dict = {}
    try:
        #Connect to database
        connection = db.connect('***', '***', '***', '***')
        cursor = connection.cursor(db.cursors.DictCursor)
        cursor.execute("""SELECT * FROM notes 
                        WHERE userID = %s
                        ORDER BY updated_at DESC
                        """, (username))
        #For each note owned by logged in user
        for row in cursor.fetchall():
            noteID = row['noteID']
            title = row['title']
            note_list += """
                <option value="%s"></option>
            """ % (title)
            note_dict[title] = noteID
    
        #Select all background music
        cursor.execute("""SELECT * FROM music 
                          ORDER BY plays DESC
                        """)
        #For each song
        for row in cursor.fetchall():
            musicID = row['musicID']
            plays = row['plays']
            music_list += """
                <option value="%s">Plays: %s</option>
            """ % (musicID, plays)
        
        #Close connection
        cursor.close()  
        connection.close()
    except (db.Error, IOError):
        #If there was an error
        errorMessage = '<p>Oh no! There was an issue with your request, please try again later!</p>'

    #Content for logged in users
    content += """
        <div class="col-2"> <!-- 2 Column layout using flexbox -->
            <section>
                <h2><i class="fas fa-stopwatch"></i> Create a Timer</h2>
                <form action="timer.py" method="post">  <!-- Form for creating timer -->
                    <fieldset>  <!-- Fielset for optional fields -->
                        <legend>Optional</legend>
                        <label class="optional" for="title">Name</label>
                        <input class="optional" type="text" name="title" placeholder="Name of timer" autocomplete="off"> <!-- Input for timer title -->
                        <label class="optional" for="note">Associated Note</label> 
                        <input class="optional" list="notes" name="note"  placeholder="Search for note" autocomplete="off"> <!-- Input for associated note -->
                        <datalist id="notes">
                            %s
                        </datalist>
                        <label class="optional" for="music">Add Background Music</label>
                        <input class="optional" list="music" name="music"  placeholder="Enter song name" autocomplete="off">  <!-- Input for background music -->
                        <datalist id="music">
                            %s
                        </datalist>
                    </fieldset>

                    <input type="hidden" name="create" value="True" autocomplete="off">  <!-- Form data to flag the creation of a timer -->
                    <button type="submit"><i class="fas fa-hourglass-start"></i> Start Timer</button>  <!-- Start timer -->
                </form>
            </section>
            <section>
                <h2 class="title"><i class="fas fa-sticky-note"></i> Create a Note</h2>
                <form action="notes.py" method="post">  <!-- Form for creating note -->
                    <label for="title">Name </label>
                    <input type="text" name="title" autocomplete="off">
                    <textarea name="note" rows="3" cols="40"></textarea>
                    <button type="submit"><i class="fas fa-edit"></i> Create Note</button>
                </form>
            </section>
        </div>
    """ % (note_list, music_list)
#If logged out
else:
    #Same as content above minus logged in only features
    content += """
        <div class="col-2">
            <section>
                <h2><i class="fas fa-stopwatch"></i> Create a Timer</h2>
                <form action="timer.py" method="post">
                    <fieldset>
                        <legend>Optional</legend>
                        <label class="optional" for="title">Name</label>
                        <input class="optional" type="text" name="title" autocomplete="off">
                    </fieldset>
                    <input type="hidden" name="create" value="True" autocomplete="off">
                    <button type="submit"><i class="fas fa-hourglass-start"></i> Start Timer</button>
                </form>
                    <div class="locked">
                        <p><i class="fas fa-lock"></i> Please login to access all features including</p>
                        <ul>
                            <li>Link timers with notes</li>
                            <li>Background music</li>
                            <li>Sync with friends</li>
                        </ul>
                    </div>
            </section>
            <section>
                <h2><i class="fas fa-sticky-note"></i> Create a Note</h2>
                <form action="notes.py" method="post">
                    <label for="title">Name </label>
                    <input type="text" name="title" autocomplete="off"><br>
                    <textarea name="note" rows="3" cols="40"></textarea>
                    <button type="submit"><i class="fas fa-edit"></i> Create Note</button>
                </form>
                <div class="locked">
                    <p class="title"><i class="fas fa-lock"></i> Please login to access this feature and more including</p>
                    <ul>
                        <li>Shareable Notes</li>
                        <li>Save and Edit Notes</li>
                        <li>Edit Notes with friends</li>
                    </ul>
                </div>
            </section>
        </div>
    """
#Latest news for all Users
content += """
    <div class="col-2">
        <section>
            <h2>Latest News</h2>
            <ul>
                <li><a href="https://cs1.ucc.ie/~am63/cgi-bin/viewNote.py?noteID=3">13/04/2020 - New Domain!</a></li>
                <li><a href="https://cs1.ucc.ie/~am63/cgi-bin/viewNote.py?noteID=2">12/04/2020 - Version 1.0</a></li>
                <li><a href="https://cs1.ucc.ie/~am63/cgi-bin/viewNote.py?noteID=1">12/04/2020 - Coming Soon</a></li>
            </ul>
        </section>
    </div>
"""

#Create main area passing in parameters for errorMessage, the content and allowing all users to access this page
main(errorMessage, content, False)

#Create footer
footer()