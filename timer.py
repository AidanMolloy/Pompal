#!/usr/local/bin/python3
#Import template file
from template import *

#Import datetime
import datetime

#Initialise note dictionaryand list
note_dict = {}
note_list = ""
music_list = ""

#If logged in
if username:
    #Create timer table
    timer_list = """
    <section>
        <table>
            <tr>
                <th>Title</th>
                <th>Associated Note</th>
                <th>Background Music</th>
                <th>Over At</th>
            </tr>
    """
    #Try to connect to database
    try:
        connection = db.connect('***', '***', '***', '***')
        cursor = connection.cursor(db.cursors.DictCursor)
        cursor.execute("""SELECT * FROM notes 
            WHERE userID = %s
            ORDER BY updated_at DESC
        """, (username))
        # Add notes to list to be selected from in timer creation form
        for row in cursor.fetchall():
            noteID = row['noteID']
            title = row['title']
            note_list += """
                <option value="%s"></option>
            """ % (title)
            note_dict[title] = noteID
            note_dict[noteID] = title

        # Get list of background music to be used in timer creation form
        cursor.execute("""SELECT * FROM music 
            ORDER BY plays DESC
        """)
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
        #If there was an error with the Database
        errorMessage = '<p>Oh no! There was an issue with your request, please try again later!</p>'

    #Check if Timer created by getting form_data
    form_data = FieldStorage()
    if len(form_data) != 0:
        newTitle = escape(form_data.getfirst('title', '').strip())
        newNote = escape(form_data.getfirst('note', '').strip())
        newMusic = escape(form_data.getfirst('music', '').strip())
        #Get current time to offset timer by 25 minutes from now
        now = datetime.datetime.now()
        over_at = now + datetime.timedelta(minutes = 25)
        try:
            #Connect to database
            connection = db.connect('***', '***', '***', '***')
            cursor = connection.cursor(db.cursors.DictCursor)
            #If note exists
            if newNote in note_dict:
                noteToBeAdded = note_dict[newNote]
            else:
                noteToBeAdded = 0
            #Increase the plays of music when used
            cursor.execute("""
                UPDATE music
                SET plays = plays + 1
                WHERE musicID = %s;
            """, (newMusic))
            connection.commit()
            #Create timer
            cursor.execute("""
                INSERT INTO timers (userID, title, noteID, musicID, over_at)
                VALUES (%s, %s, %s, %s, %s);
            """, (username, newTitle, noteToBeAdded, newMusic, over_at))
            connection.commit()
            #Get ID of the new timer
            cursor.execute("""
                SELECT LAST_INSERT_ID();
            """)
            for row in cursor.fetchall():
                newTimerID = row['LAST_INSERT_ID()']
                #Redirect to the new timer
                errorMessage = """
                    <script>
                        window.location.replace("https://cs1.ucc.ie/~am63/cgi-bin/viewTimer.py?timerCode=%s");
                    </script>
                """ % (newTimerID)
            #Close connection to timer
            cursor.close()  
            connection.close()
        except (db.Error, IOError):
            #If error
            errorMessage = '<p>Oh no! There was an issue with your request, please try again later!</p>'

    #Get list of currently active timers
    try:
        #Connect to database
        connection = db.connect('***', '***', '***', '***')
        cursor = connection.cursor(db.cursors.DictCursor)
        cursor.execute("""SELECT * FROM timers 
                        WHERE userID = %s AND over_at > NOW()
                        ORDER BY created_at DESC
                        """, (username))
        
        #If no active timers display no active timers in the table
        if cursor.rowcount == 0:
            errorMessage += "<h3>No active timers</h3>"
            timer_list += """
                <tr>
                    <td colspan="4">No Active Timers Available</td>
                </tr>
            """
        else:
            #For each timer active and owned by user
            for row in cursor.fetchall():
                timerID = row['timerID']
                noteID = row['noteID']
                title = row['title']
                music = row['musicID']
                created = row['created_at']
                over = row['over_at']
                noteToBeAdded = ""
                if noteID in note_dict:
                    noteToBeAdded = """<a href="https://cs1.ucc.ie/~am63/cgi-bin/viewNote.py?noteID=%s">%s</a>""" % (noteID, note_dict[noteID])
                else:
                    noteToBeAdded = ""
                #Add to timer
                timer_list += """
                    <tr>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td><a href="https://cs1.ucc.ie/~am63/cgi-bin/viewTimer.py?timerCode=%s">Open</a></td>
                    </tr>
                """ % (title, noteToBeAdded, music, over, timerID)
        #Close connection
        cursor.close()  
        connection.close()
    except (db.Error, IOError):
        #If there is an error
        errorMessage = '<p>Oh no! There was an issue with your request, please try again later!</p>'
    
    #Close timer list
    timer_list += """
            </table>
        </section>
    """

    #Create Content with form for creating timer same as index.py
    content += """
        <section>
            <h2><i class="fas fa-stopwatch"></i> Create a Timer</h2>
            <form action="timer.py" method="post">
                <fieldset>
                    <legend>Optional</legend>
                    <label class="optional" for="title">Name </label>
                    <input class="optional" type="text" name="title" autocomplete="off">

                    <label class="optional" for="note">Associated Note:</label> 
                    <input class="optional" list="notes" name="note" placeholder="Search for note" autocomplete="off">
                    <datalist id="notes">
                        %s
                    </datalist>
                    <label class="optional" for="music">Add Background Music:</label>
                    <input class="optional" list="music" name="music" placeholder="Enter song name" autocomplete="off">
                    <datalist id="music">
                        %s
                    </datalist>
                </fieldset>
                <input type="hidden" name="create" value="True" autocomplete="off">
                <button type="submit"><i class="fas fa-hourglass-start"></i> Start Timer</button>
            </form>
        </section>
        <section><!-- Active Timers List -->
            <h2>Active Timers</h2>
            %s
        </section>
    """ % (note_list, music_list, timer_list)

#If not logged in
else:
    #Get form_data
    form_data = FieldStorage()
    if len(form_data) != 0:
        newTitle = escape(form_data.getfirst('title', '').strip())
        #Get current time to offset timer by 25 minutes from now
        now = datetime.datetime.now()
        over_at = now + datetime.timedelta(minutes = 25)
        try:
            #Connect to database
            connection = db.connect('***', '***', '***', '***')
            cursor = connection.cursor(db.cursors.DictCursor)
            #Create timer
            cursor.execute("""
                INSERT INTO timers (userID, title, musicID, over_at)
                VALUES (%s, %s, %s, %s);
            """, ('Guest', newTitle, "", over_at))
            errorMessage += "<h2>Timer Started</h2>"
            connection.commit()
            #Get Timer ID
            cursor.execute("""
                SELECT LAST_INSERT_ID();
            """)
            for row in cursor.fetchall():
                newTimerID = row['LAST_INSERT_ID()']
                #Redirect to new Timer
                errorMessage = """
                    <script>
                        window.location.replace("https://cs1.ucc.ie/~am63/cgi-bin/viewTimer.py?timerCode=%s");
                    </script>
                """ % (newTimerID)
            #Close Connection
            cursor.close()  
            connection.close()
        except (db.Error, IOError):
            #If error with connection
            errorMessage = '<p>Oh no! There was an issue with your request, please try again later!</p>'

create() # Create Page

head() # Create head

nav() # Create nav

main(errorMessage, content, False) # Create main with errormMessage, content and allow anyone to access the paage

footer() # Create footer