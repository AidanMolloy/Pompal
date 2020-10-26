#!/usr/local/bin/python3
#Import template file
from template import *

#Get form_data from the FieldStorage
form_data = FieldStorage()
if len(form_data) != 0:
    #Create note dictionary, timer list and note list
    note_dict = {}
    timer_list = """
        <section>
            <table>
                <tr>
                    <th>Title</th>
                    <th>Associated Note</th>
                    <th>Background Music</th>
                    <th>Time Left</th>
                </tr>
    """

    note_list = """
        <section>
            <table>
                <tr>
                    <th>Title</th>
                    <th>Created</th>
                    <th>Last Modified</th>
                </tr>
    """

    #Get userID
    user = escape(form_data.getfirst('user', '').strip())
    try:
        #Connect to database
        connection = db.connect('***', '***', '***', '***')
        cursor = connection.cursor(db.cursors.DictCursor)
        #Check if valid user
        cursor.execute("""
            SELECT * FROM users 
            WHERE username = %s
        """, (user))
        if cursor.rowcount == 0:
            errorMessage += "<h3>User does not exist</h3>"
        else:
            #Get the users notes
            cursor.execute("""
                SELECT * FROM notes 
                WHERE userID = %s
                ORDER BY updated_at DESC
            """, (user))
            #If no notes then say no notes avaiable
            if cursor.rowcount == 0:
                note_list += """
                    <tr>
                        <td colspan="3">No Notes Available</td>
                    </tr>
                """
            else:
                #List out the notes and link them
                for row in cursor.fetchall():
                    noteID = row['noteID']
                    title = row['title']
                    note = row['note']
                    created = row['created_at']
                    updated = row['updated_at']
                    note_list += """
                        <tr>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td><a href="https://cs1.ucc.ie/~am63/cgi-bin/viewNote.py?noteID=%s">Open</a></td>
                        </tr>
                    """ % (title, created, updated, noteID)
                    note_dict[noteID] = title

            #Close notes table
            note_list += """
                    </table>
                </section>
            """

            #Get all the users timers
            cursor.execute("""
                SELECT * FROM timers 
                WHERE userID = %s AND over_at > NOW()
            """, (user))
            #If none say that
            if cursor.rowcount == 0:
                timer_list += """
                    <tr>
                        <td colspan="4">No Active Timers Available</td>
                    </tr>
                """
            else:
                #Otherwise list all the timers they have active and link associated note and the timer
                for row in cursor.fetchall():
                    timerID = row['timerID']
                    title = row['title']
                    noteID = row['noteID']
                    noteToBeAdded = ""
                    #Link the associated note
                    if noteID in note_dict:
                        noteToBeAdded = """<a href="https://cs1.ucc.ie/~am63/cgi-bin/viewNote.py?noteID=%s">%s</a>""" % (noteID, note_dict[noteID])
                    musicID = row['musicID']
                    over = row['over_at']
                    timer_list += """
                        <tr>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td><a href="https://cs1.ucc.ie/~am63/cgi-bin/viewTimer.py?timerCode=%s">Open</a></td>
                        </tr>
                    """ % (title, noteToBeAdded, musicID, over, timerID)
            
            #Close the timer table
            timer_list += """
                    </table>
                </section>
            """
        #Close connection to server
        cursor.close()  
        connection.close()
    except (db.Error, IOError):
        #If there was an issue with the connection to the database
        errorMessage = '<p>Oh no! There was an issue with your request, please try again later!</p>'

    #Create content
    content = """
        <section>
            <!-- Profile Owner -->
            <h1>%s's Profile </h1>
            <h3>Active Timers</h3>
            %s
            <h3>Notes</h3>
            %s
        </section>
    """ % (user, timer_list, note_list)

#Of not a valid user
else:
    errorMessage += "Please enter a valid User ID"

create() # Create Page

head() # Create Head

nav() # Create Nav

main(errorMessage, content, False) # Create Main with errorMessage, content and anyone can view

footer() # Create Footer